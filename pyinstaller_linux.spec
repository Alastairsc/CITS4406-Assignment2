# -*- mode: python -*-

block_cipher = None


a = Analysis(['application.py'],
             pathex=['/home/alastair/Documents/CITS4406-Assignment2'],
             binaries=[],
             datas=[('*.py','.')],
             hiddenimports=['csv','statistics','xlrd', 'tkinter'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Data-oracle_Linux',
          debug=False,
          strip=False,
          upx=True,
          console=True )
