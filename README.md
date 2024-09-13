# 实时聊天应用

这是一个基于 Flask 和 Socket.IO 的实时聊天应用。它提供了用户注册、登录、实时消息交换和在线用户管理等功能。

## 主要功能

1. 用户认证（注册、登录、登出）
2. 实时聊天
3. 在线用户管理
4. 用户头像上传
5. IP 地址定位
6. 日志记录

## 技术栈

- 后端：Flask, Flask-SocketIO, Flask-SQLAlchemy, Flask-Login
- 数据库：SQLite
- 前端：HTML, CSS, JavaScript (Socket.IO 客户端)

## 执行流程

1. 从远程仓库克隆项目：
```
git clone https://gitee.com/guangxuejian/chat_-site.git
cd chat_-site
```

2. 创建并激活虚拟环境：
```
python -m venv .venv
source .venv/bin/activate 
# 在 Windows 上使用 
.venv\Scripts\activate
```

3. 安装依赖包：
```
pip install -r requirements.txt
```
4. 启动服务：
```
python run.py
```
现在，您可以在浏览器中访问 `http://localhost:5000` 来使用该应用。

## 项目结构
```
- `app/`: 主应用目录
  - `__init__.py`: 应用初始化
  - `config.py`: 配置文件
  - `models.py`: 数据库模型
  - `routes.py`: 路由处理
  - `sockets.py`: WebSocket 事件处理
- `templates/`: HTML 模板
- `static/`: 静态文件（CSS、JavaScript、头像等）
- `logs/`: 日志文件
- `run.py`: 应用入口点
```
## 配置
```

主要配置在 `app/config.py` 文件中。请确保在部署到生产环境时更改 `SECRET_KEY` 和其他敏感设置。
```
## 注意事项
```
- 本项目使用 SQLite 数据库，适合小规模使用。对于大规模部署，请考虑使用更强大的数据库系统。
- 确保 `logs` 目录存在并可写，否则日志记录可能会失败。
- 在生产环境中部署时，请使用 WSGI 服务器（如 Gunicorn）来运行应用。
```
## 贡献
```
欢迎提交 Issue 或 Pull Request 来改进这个项目！

## 许可证

[MIT License](LICENSE)
```