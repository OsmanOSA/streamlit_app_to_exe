import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from backend.session_config import create_text_input

def resource_path(relative_path):
    """Compatible .py normal et .exe PyInstaller."""
    # Mode PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    
    # Mode normal → reprendre ton comportement EXACT
    CURRENT = Path(__file__).resolve()
    ROOT = CURRENT.parent.parent
    
    return ROOT / relative_path

FILE_PATH = resource_path("datasets/data.csv")

@st.cache_data
def read_data():
    data = pd.read_csv(FILE_PATH, sep=None, engine="python", 
                        parse_dates=["timestamp"], index_col="timestamp")
    st.success("Données chargée !")
    return data 

def vue_ensemble():

    st.markdown(f"<h1 class='main-title'> Surveillance de la performance énergétique</h1>", unsafe_allow_html=True)

    data = read_data()

    create_text_input(
        label="Date du début",
        session_key="date_start", 
        widget_key="date_start1",
        side_bar=True)

    create_text_input(
        label="Date de fin",
        session_key="date_end", 
        widget_key="date_end1",
        side_bar=True)

    try: 
        data = data.loc[st.session_state.date_start:st.session_state.date_end]
    except Exception as e:
        raise ValueError(e)


    # Consommation moyenne 
    conso = data['consommation_totale'] / 1_000
    conso_moy = conso.mean()

    # Production moyenne de toutes les sources 
    prods= data[['SOLAR', 'BIOMASS', 'WIND_ONSHORE', 'NUCLEAR']].sum(axis=1) / 1_000
    prods = pd.DataFrame(prods, columns=["Production_totale"])
    prod_moy = prods.mean().values

    # Taux de couverture moyen
    taux_couv_moy = (conso_moy / prod_moy) * 100

    # Déficit énergétique moyen
    deficit_energ_moy = (prod_moy - conso_moy)

    # Température moyenne 
    temp_moy = data["temp"].mean()

    # Concaténation de prod et conso
    df_prod_conso = pd.concat([prods, conso], axis=1)

    col_conso, col_prod, col_taux_couv, col_deficit, col_temp = st.columns(spec=5, gap="small")

    with col_conso:
        st.markdown(f"""<div class="card">
                <h5 style="color: var(--main-title-color);">Consommation moyenne</h5>
                <p class="description" style"text-align: justify;">
                    {round(conso_moy, 1)} GW
                </p>
                </div>""",
                unsafe_allow_html=True)

    with col_prod:
        st.markdown(f"""<div class="card">
                <h5 style="color: var(--main-title-color);">Production moyenne</h5>
                <p class="description" style"text-align: justify;">
                    {np.round(prod_moy[0], 1)} GW
                </p>
                </div>""",
                unsafe_allow_html=True)
        
    with col_taux_couv:
        st.markdown(f"""<div class="card">
                <h5 style="color: var(--main-title-color);">Taux de couverture</h5>
                <p class="description" style"text-align: justify;">
                    {np.round(taux_couv_moy[0], 1)} %
                </p>
                </div>""",
                unsafe_allow_html=True)
        
    with col_deficit:
        st.markdown(f"""<div class="card">
                <h5 style="color: var(--main-title-color);">Déficit énergétique</h5>
                <p class="description" style"text-align: justify;">
                    {np.round(deficit_energ_moy[0], 1)} GW
                </p>
                </div>""",
                unsafe_allow_html=True)
        
    with col_temp:
        st.markdown(f"""<div class="card">
                <h5 style="color: var(--main-title-color);">Température moyenne</h5>
                <p class="description" style"text-align: justify;">
                    {round(temp_moy, 1)} ° C
                </p>
                </div>""",
                unsafe_allow_html=True)

    fig = px.line(df_prod_conso, 
                title="Evolution de la production totale et de la consommation totale", 
                labels={
                        "timestamp": "Date",
                        "value": "Puissance en GW",
                        "variable": "Type"})
    st.plotly_chart(figure_or_data=fig)

    labels = ["SOLAR", "BIOMASS", "NUCLEAR", "WIND_ONSHORE"]
    values = [data[labels[0]].sum(), data[labels[1]].sum(), 
            data[labels[2]].sum(), data[labels[3]].sum()]
    st.plotly_chart(figure_or_data=go.Figure(data=[go.Pie(labels=labels, values=values)]))


