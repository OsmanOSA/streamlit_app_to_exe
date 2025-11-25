import streamlit as st

st.set_page_config(
    page_title="Application simple", 
    layout="wide",
    initial_sidebar_state="auto")

st.markdown(f"<h1 class='main-title'>Bonjour, comment ça va ?</h1>", unsafe_allow_html=True)