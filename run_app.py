import sys
from pathlib import Path
from streamlit.web import cli

if __name__=="__main__":
    cli._main_run_clExplicit(file='app.py')