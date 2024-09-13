from app import get_app
from app.sockets import socketio
import sys
import traceback
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = get_app()


if __name__ == '__main__':
    # socketio.run(app, debug=True) #本地调试模式
    # socketio.run(app, host='0.0.0.0', debug=False) #生产模式
    #flask run --host=0.0.0.0 暴露外网访问
    #flask run --debug 
    #pyinstaller app.spec 打包成app.exe命令
    #使用无控制台的打包选项：
    #如果使用 PyInstaller，可以使用 --noconsole 或 -w 选项：
    # pyinstaller --noconsole your_script.py
    #打开 app.spec 文件，找到 EXE() 函数调用。将 console=True 改为 console=False。
    # 然后运行 PyInstaller，但不要加任何额外的选项 yinstaller app.spec
    try:
        socketio.run(app, host='0.0.0.0', debug=app.config['DEBUG'], allow_unsafe_werkzeug=True) 
    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n"
        error_message += traceback.format_exc()
        with open('error_log.txt', 'w',encoding='utf-8') as f:
            f.write(error_message)
        print(error_message)
        input("Press Enter to exit...")
        sys.exit(1)