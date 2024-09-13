# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['run.py'],
             pathex=['.'],
             binaries=[],
             datas=[('templates', 'templates'), 
                    ('app/static', 'app/static'),
                    ('instance', 'instance'),
                    ('app/config.py', 'app')],
             hiddenimports=['engineio.async_drivers.threading', 'flask_socketio', 'eventlet', 'dns', 'engineio', 'flask_sqlalchemy', 'flask_login', 'flask_limiter', 'flask_migrate'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')