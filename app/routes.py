from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from . import db
from .models import User
import requests

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
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            current_app.logger.info(f'用户 {username} 登录成功')
            return redirect(url_for('main.chat'))
        current_app.logger.warning(f'用户 {username} 登录失败')
        flash('用户名或密码错误', 'error')
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        avatar = request.files.get('avatar')
        ip = request.remote_addr
        city = get_city_from_ip(ip)

        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('register.html')

        new_user = User(username=username, ip=ip, city=city)
        new_user.set_password(password)

        if avatar:
            filename = f"{username}.jpg"
            avatar.save(f"app/static/avatars/{filename}")
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
    return render_template('chat.html', username=session['username'])

def get_city_from_ip(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        data = response.json()
        return data.get('city', 'Unknown')
    except:
        return 'Unknown'

def init_app(app):
    app.register_blueprint(bp)