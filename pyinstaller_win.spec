# -*- mode: python -*-

block_cipher = None

a = Analysis(['application.py'],
             pathex=['E:\\Documents\\Github\\django_env\\mysite\\common\\analyser'],
             binaries=[],
             datas=[('*.py','.')],
             hiddenimports=['csv','statistics','scipy.stats'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib','IPython','sphinx','sqlalchemy','Cython','OpenSSL','PIL','asyncio', 'babel','backports',
              'boto','bottleneck', 'cffi', 'cloudpickle', 'Crypto','PyQt5','bs4','colorama','concurrent','future','gevent',
              'ipykernel','jinja2','jupyter_client','jupyter_core','lib2to3','libfuturize','markupsafe','multiprocessing',
              'numpy','nose', 'numexpr', 'openpyxl','pandas', 'past', 'patsy', 'pygments', 'pywin', 'setuptools', 'sqlite3',
               'scipy','statsmodels', 'tables', 'tornado', 'xlswriter', 'xlwt', 'xlwt'],
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
          name='Data-oracle_win',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='1488810372_analysis.ico')
