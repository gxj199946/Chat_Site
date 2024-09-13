from app import get_app

from app.sockets import socketio

app = get_app()


if __name__ == '__main__':
    socketio.run(app, debug=True)
    #flask run --host=0.0.0.0 暴露外网访问
    #flask run --debug 