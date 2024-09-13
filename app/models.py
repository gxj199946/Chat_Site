from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#数据库更新后迁移
#   flask db init 初始化迁移,这将创建一个 migrations 文件夹
#   flask db migrate -m "Initial migration" 创建初始迁移
#   flask db upgrade  最后，应用迁移
#重置数据库
# flask db downgrade base
# flask db upgrade
#处理迁移报错
#1.首先，让我们尝试将数据库标记为最新版本：
# flask db stamp head
# 如果上述命令成功，再次检查当前状态：
#flask db current
#2.如果这解决了问题，您应该能看到当前版本是 xxxxxxx。

#user用户表
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    avatar = db.Column(db.String(200))
    city = db.Column(db.String(100))
    ip = db.Column(db.String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
#message消息表
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('messages', lazy='dynamic'))