# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\Programming\\JPHACKS2021\\F_2103-master','C:\\Users\\kitsu\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\cv2'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
a.datas += [('click.png', '.\\click.png', 'DATA'),
                ('move.png', '.\\move.png', 'DATA'),
                ('scroll.png', '.\\scroll.png', 'DATA'),
                ('shape_predictor_68_face_landmarks.dat', '.\\shape_predictor_68_face_landmarks.dat', 'DATA'),
                ('ML\\gesture_classifier.tflite', '.\\ML\\gesture_classifier.tflite', 'DATA'),
                ('Blicky.ico', '.\\Blicky.ico', 'DATA'),
                ('C:\\Users\\kitsu\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\mediapipe\\modules', '.\\mediapipe\\modules', 'DATA'),
                ]
exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Blicky',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='Blicky.ico',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
