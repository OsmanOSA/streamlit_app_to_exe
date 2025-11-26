import streamlit as st




class SessionConfig:
    """Configuration centralisée des variables de session"""

    DEFAULT_VALUES = {
        "date_start": "2025-01-01", 
        "date_end": "2025-02-01"
    }

    @classmethod
    def _init_dict(cls, defaults: dict):
        """Initialise un dict de valeurs par défaut"""
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
                print(f"[CONFIG] Initialized {key} = {default_value}")

    @classmethod
    def initialize_all(cls):
        """Initialise toutes les variables de session (tous les dicts)"""
        cls._init_dict(cls.DEFAULT_VALUES)

    @classmethod
    def get(cls, key, default=None):
        """Récupère une valeur du session_state avec fallback"""
        return st.session_state.get(
            key,
            default or
            cls.DEFAULT_VALUES.get(key))

    @classmethod
    def set(cls, key, value):
        """Met à jour une valeur dans session_state"""
        st.session_state[key] = value

    @classmethod
    def reset_all(cls):
        """Remet toutes les variables à leur valeur par défaut"""
        for key, default_value in {**cls.DEFAULT_VALUES}.items():
            st.session_state[key] = default_value
    @classmethod
    def get_radio_index(cls, key, options):
        """Récupère l'index pour un radio button"""
        try:
            current_value = cls.get(key)
            return options.index(current_value)
        except (ValueError, TypeError):
            return 0

def create_radio_widget(label, options, session_key, widget_key, **kwargs):
    """Crée un radio widget connecté au session_state"""
    current_index = SessionConfig.get_radio_index(session_key, options)
    
    choice = st.radio(
        label,
        options=options,
        index=current_index,
        key=widget_key,
        **kwargs
    )
    
    # Mettre à jour automatiquement la session 
    SessionConfig.set(session_key, choice)
    return choice

def create_number_input(label, session_key, widget_key, 
                        side_bar: bool = False,
                        **kwargs):
    """Crée un number_input connecté au session_state"""
    current_value = SessionConfig.get(session_key)

    if side_bar:
    
        value = st.sidebar.number_input(
            label,
            value=current_value,
            key=widget_key,
            **kwargs
        )
    
    else: 
        value = st.number_input(
        label,
        value=current_value,
        key=widget_key,
        **kwargs)

    SessionConfig.set(session_key, value)
    return value


def create_text_input(label, session_key, widget_key,
                      side_bar: bool = False,
                    **kwargs):
    """Crée un text_input connecté au session_state"""
    current_value = SessionConfig.get(session_key)
    
    if side_bar:
        value = st.sidebar.text_input(
            label,
            value=current_value,
            key=widget_key,
            **kwargs
        )
    
    else:
        value = st.text_input(
            label,
            value=current_value,
            key=widget_key,
            **kwargs
        )
    
    SessionConfig.set(session_key, value)
    return value
