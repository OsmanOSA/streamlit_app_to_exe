# hooks/hook-streamlit.py
from PyInstaller.utils.hooks import copy_metadata, collect_submodules

# Récupère automatiquement toutes les métadonnées de Streamlit et les packages utilisés dans ton projet
datas = copy_metadata('streamlit')

# Inclut tous les sous-modules de Streamlit (évite les erreurs d'import dynamique)
hiddenimports = collect_submodules('streamlit')
hiddenimports = collect_submodules('encodings')