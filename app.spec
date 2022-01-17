# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['app.py'],
             pathex=['/usr/lib/x86_64-linux-gnu/'],
             binaries=[("/usr/lib/x86_64-linux-gnu/vlc/plugins/*", "vlc/plugins")],
             datas=[('/home/sidhu/Desktop/Sidhu/venv/lib/python3.9/site-packages/eel/eel.js', 'eel'), ('web', 'web')],
             hiddenimports=['bottle_websocket'],
             hookspath=[],
             hooksconfig={},
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
          a.binaries + [("libvlc.so.5", "/usr/lib/x86_64-linux-gnu/libvlc.so.5", "BINARY")],
          a.zipfiles,
          a.datas,  
          [],
          name='Sidhu',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='icon.png')
