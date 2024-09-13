from flask import current_app, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user
from collections import defaultdict

socketio = SocketIO()
from flask import current_app

online_users = defaultdict(int)

def init_app(app):
    socketio.init_app(app)

@socketio.on('connect')
def handle_connect():
    username = session.get('username', 'Anonymous')
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
    emit('message', {'username': username, 'message': data['message']}, broadcast=True)

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