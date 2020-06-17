# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None


a = Analysis(['cli.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[
                ('app/storage/settings/settings.yaml', 'app/storage/settings/'),
                ('app/storage/settings/settings.dev.yaml', 'app/storage/settings/')
                ],
             hiddenimports=[],
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
          name='askue-rs-balance',
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
               name='cli')
