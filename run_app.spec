# run_app.spec

# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata

datas = [('D:/streamlit_app_to_exe/.venv/Lib/site-packages/streamlit/static', 'streamlit/static'),
         ('D:/streamlit_app_to_exe/.venv/Lib/site-packages/streamlit/runtime', 'streamlit/runtime'),
         ("D:/streamlit_app_to_exe/.venv/Lib/site-packages/altair/vegalite/v5/schema/vega-lite-schema.json",
         "./altair/vegalite/v5/schema/"), 
         ('D:/streamlit_app_to_exe/.streamlit', '.streamlit')]

datas += copy_metadata('streamlit')


a = Analysis(
    ['run_app.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=['encodings'],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
