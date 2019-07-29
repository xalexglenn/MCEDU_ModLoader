# -*- mode: python -*-

block_cipher = None


a = Analysis(['ModManager.py'],
             pathex=['/Users/zaniacmacbook1/PycharmProjects/Mod Loader'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          exclude_binaries=True,
          name='Mod Loader',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Mod Loader')
app = BUNDLE(coll,
             name='Mod Loader.app',
             icon='icon.icns',
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': 'True'
        },)
