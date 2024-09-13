from flask import current_app, request, session,url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user
from collections import defaultdict
from datetime import datetime
from .models import User, Message
from app import db
from .utils import get_location_from_coords
socketio = SocketIO()
from flask import current_app

online_users = defaultdict(int)

def init_app(app):
    socketio.init_app(app)

@socketio.on('connect')
def handle_connect():
    username = session.get('username', 'Anonymous')
    user = User.query.filter_by(username=username).first()
    if user:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        if latitude and longitude:
            address_info = get_location_from_coords(latitude, longitude)
            if address_info:
                state = address_info.get('state', '')
                city = address_info.get('city', '')
                location = state or city  # 优先使用state，如果没有则使用city
                user.city = location
                db.session.commit()
    
    if username not in online_users:
        online_users[username] = 1
        emit('user_joined', {'username': username, 'count': len(online_users)}, broadcast=True)
        current_app.logger.info(f'用户 {username} 连接到聊天室')
    else:
        online_users[username] += 1
        emit('update_count', {'count': len(online_users)}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    user = User.query.filter_by(username=username).first()
    location = "未知"
    avatar_url = url_for('static', filename='default_avatar.jpg', _external=True)

    if user:
        location = user.city or "未知"
        avatar_url = user.avatar or avatar_url
        message = Message(content=data['message'], user=user)
        db.session.add(message)
        db.session.commit()

    # emit('message', {
    #     'username': username,
    #     'message': data['message'],
    #     'timestamp': datetime.utcnow().isoformat(),
    #     'avatar': avatar_url,
    #     'location': location
    # }, broadcast=True)
    #转为北京时间，不需要就注释掉，根据当地时区自动获取
    from datetime import datetime, timedelta
    beijing_time = datetime.utcnow() + timedelta(hours=8)
    emit('message', {
        'username': username,
        'message': data['message'],
        'timestamp': beijing_time.isoformat(),
        'avatar': avatar_url,
        'location': location
    }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username', 'Anonymous')
    online_users[username] -= 1
    if online_users[username] <= 0:
        del online_users[username]
        emit('user_left', {'username': username, 'count': len(online_users)}, broadcast=True)
        current_app.logger.info(f'用户 {username} 离开聊天室')
    else:
        emit('update_count', {'count': len(online_users)}, broadcast=True)
    current_app.logger.info(f'用户 {username} 断开连接')

#清除所有用户的历史纪录
@socketio.on('clear_chat')
def handle_clear_chat():
    Message.query.delete()
    db.session.commit()
    emit('chat_cleared', broadcast=True)
    current_app.logger.info('聊天记录已被清除')

#清除当前用户的历史纪录
@socketio.on('clear_user_chat')
def handle_clear_user_chat():
    username = session.get('username')
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            Message.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            emit('user_chat_cleared', {'username': username}, room=request.sid)

