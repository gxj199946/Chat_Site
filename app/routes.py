from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from . import db
from .models import User,Message
import pydenticon
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename
from .utils import get_location_from_coords

bp = Blueprint('main', __name__, template_folder='templates')

from flask import current_app
from app import limiter

@bp.route('/')
def index():
    if 'username' in session:
        return render_template('chat.html', username=session['username'])
    return redirect(url_for('main.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        # 获取用户 IP 地址和主机信息
        user_ip = request.remote_addr
        user_host = request.host
        # 获取地理位置
        address_info = get_location_from_coords(latitude, longitude)
        state = address_info.get('state', '') if address_info else ''
        city = address_info.get('city', '') if address_info else ''
        location = f"{state}".strip()
        current_app.logger.info(f"登录尝试 - 用户名: {username}, IP: {user_ip}, 主机: {user_host}, 经度: {longitude}, 纬度: {latitude}, 位置: {location}")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            #获取ip方法1
            # ip = request.remote_addr
            # city = get_city_from_ip(ip)
            # user.ip = ip
            # user.city = city
            user.ip = user_ip
            user.city = location
            db.session.commit()
            current_app.logger.info(f'用户 {username} 登录成功')
            return redirect(url_for('main.chat'))
        current_app.logger.warning(f'用户 {username} 登录失败')
        flash('用户名或密码错误', 'error')
    return render_template('login.html')


def generate_identicon(username, size=200):
    generator = pydenticon.Generator(5, 5)
    padding = int(size * 0.1)  # 将浮点数转换为整数
    identicon = generator.generate(username, size, size, padding=(padding, padding, padding, padding))
    
    image = Image.open(io.BytesIO(identicon))
    return image

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        avatar = request.files.get('avatar')

        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('register.html')

        new_user = User(username=username)
        new_user.set_password(password)

        if avatar and avatar.filename:
            # 确保文件名安全
            filename = secure_filename(f"{username}_avatar.png")
            avatar_path = os.path.join(current_app.root_path, 'static', 'avatars', filename)
            os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
            
            # 保存上传的文件
            avatar.save(avatar_path)
            new_user.avatar = f"/static/avatars/{filename}"
        else:
            # 生成默认头像
            identicon = generate_identicon(username)
            filename = secure_filename(f"{username}_default_avatar.png")
            avatar_path = os.path.join(current_app.root_path, 'static', 'avatars', filename)
            os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
            identicon.save(avatar_path)
            new_user.avatar = f"/static/avatars/{filename}"

        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        return redirect(url_for('main.index'))
    return render_template('register.html')

@bp.route('/logout')
def logout():
    username = session.pop('username', None)
    if username:
        current_app.logger.info(f'用户 {username} 退出登录')
    return redirect(url_for('main.login'))

@bp.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('main.login'))
    messages = Message.query.order_by(Message.timestamp.desc()).limit(50).all()
    messages.reverse()  # 反转消息顺序，使最早的消息在前
    return render_template('chat.html', username=session['username'], messages=messages)


def init_app(app):
    app.register_blueprint(bp)