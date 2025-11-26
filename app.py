import warnings
import streamlit as st

from frontend.vue_ensemble_page import vue_ensemble
from frontend.accueil_page import Home
from pathlib import Path
from backend.session_config import SessionConfig

warnings.simplefilter(action="ignore", category=FutureWarning)

# Configuration de la page
st.set_page_config(
    page_title="Application simple", 
    layout="wide",
    initial_sidebar_state="auto")

# Charger le CSS personnalisé
def load_custom_css():
    try:
        with open("./.streamlit/styles.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_custom_css()
SessionConfig.initialize_all()

class MultiApp:
    """ Gére plusieurs pages Streamlit"""
    
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """ Ajoute une nouvelle page à l'application"""
        self.apps.append({"title": title, "function": func})

    def run(self):
        """ Affiche la page sélectionnée dans la barre latérale et ajoute un pied de page avec navigation"""
        
        # Initialisation de l'index de page dans la session state si nécessaire
        if 'page_index' not in st.session_state:
            st.session_state.page_index = 0
        
        # Barre latérale
        with st.sidebar:
            st.markdown("## Menu Principal")
            
            st.markdown("---")
            
            # Sélection d'application via radio buttons
            selected_app_index = st.radio(
                "Page", 
                range(len(self.apps)),
                format_func=lambda i: self.apps[i]["title"],
                index=st.session_state.page_index
            )
            
            # Si l'utilisateur sélectionne une page différente via le sidebar
            if selected_app_index != st.session_state.page_index:
                st.session_state.page_index = selected_app_index
                st.rerun()
            
            st.markdown("---")
        
        # Obtenir l'application sélectionnée basée sur l'index de page
        selected_app = self.apps[st.session_state.page_index]
        
        # Exécuter l'application sélectionnée
        selected_app["function"]()
        
        # Création d'un espace vide pour pousser le footer vers le bas
        for _ in range(5):
            st.write("")
        
        # Pied de page avec navigation
        footer_container = st.container()
        
        with footer_container:
            # HTML pour le pied de page
            current_page = self.apps[st.session_state.page_index]["title"]
            footer_html = f"""
            <div class="footer">
                <div class="page-indicator">
                    Page {st.session_state.page_index + 1} sur {len(self.apps)} : <strong>{current_page}</strong>
                </div>
                <div class="footer-content">
            """
            st.markdown(footer_html, unsafe_allow_html=True)
            
            # Fermeture des balises HTML
            st.markdown("</div></div>", unsafe_allow_html=True)

app = MultiApp()
app.add_app("Page Vue d'ensemble", vue_ensemble)
app.run()



