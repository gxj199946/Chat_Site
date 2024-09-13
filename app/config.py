import os
# 基本配置
DEBUG = False #调试模式 #生产模式为False
SECRET_KEY = 'j84h2f9d7s3g1k5p6r0w7q9b4a5c2e1z'  # 请更改为一个随机的字符串
#本地环境变量模式
#DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
#SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

#数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'your_database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 其他配置项...