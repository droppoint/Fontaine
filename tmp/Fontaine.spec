# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'D:\\Aptana_Workspace\\Fontaine\\src\\Fontaine.py'],
             pathex=['D:\\Aptana_Workspace\\Fontaine\\tmp'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'Fontaine.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name=os.path.join('dist', 'Fontaine.exe.app'))
