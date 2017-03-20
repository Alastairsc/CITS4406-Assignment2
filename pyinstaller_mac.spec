# -*- mode: python -*-
#For use on mac systems
#Problems occur with tkinter
#Move Tcl and Tk from system files to dist file before using
#Virtualenv recommended

block_cipher = None


a = Analysis(['application.py'],
             pathex=['/Users/chine16/Documents/CITS4406-Assignment2'],
             binaries=[],
             datas=[('*.py','.'),('dist/Tk','.'),('dist/Tcl','.')],
             hiddenimports=['csv','statistics','xlrd','tkinter'],
             hookspath=['hooks'],
             runtime_hooks=['hooks/pyi_rth__tkinter.py'],
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
          name='Data-oracle_mac',
          debug=False,
          strip=False,
          upx=True,
          console=False,
	  icon='1488810372_analysis.ico' )
