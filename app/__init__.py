from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
limiter = None

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object('app.config')

    db.init_app(app)
    login_manager.init_app(app)
    limiter = Limiter(key_func=get_remote_address)
    limiter.init_app(app)
    migrate = Migrate(app, db)
    # 配置日志
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10,encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('应用启动')

    with app.app_context():
        db.create_all()

    from . import routes
    from . import sockets
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    routes.init_app(app)
    sockets.init_app(app)

    return app

app = None

def get_app():
    global app
    if app is None:
        app = create_app()
    return app