from streamlit_option_menu import option_menu
import streamlit as st
import dataframefunctions
import dataexploration
import plots
import runpredictions
from PIL import Image
import numpy as np
import pandas as pd

choose = option_menu("Data Cleaner",["Home","Prepocesing","Vizualisation","M.Learning","About"],
    icons=['house','file','bi bi-search','graph-up','person lines fill'],
    menu_icon = "None", default_index=0,
    styles={
        "container": {"padding": "5!important", "background-color": ""},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "10px", "text-align": "left", "margin":"5px", "--hover-color": ""},
        "nav-link-selected": {"background-color": ""},
    },orientation = "horizontal"
    )
#*********************************************************************
if choose=="Prepocesing":
    with st.sidebar:
        uploaded_file = st.sidebar.file_uploader("Please upload your dataset (CSV format):", type='csv')
        is_loaded_dataset = st.sidebar.warning("Dataset not uploaded")
        if uploaded_file is not None:
            is_loaded_dataset.success("Dataset uploaded successfully!")
            dataframe = dataframefunctions.get_dataframe(uploaded_file)
            df = dataframe.copy()
            df.to_csv("df")
    dataexploration.load_page(df)

#*********************************************************************
if choose=="Vizualisation":
    df = pd.read_csv("df")
    select = st.sidebar.selectbox("Select the Kind of plot",["Plot","Statistique Test"])
    if select== "Plot":
        plots.load_page(df)

if choose=="M.Learning":
    df = pd.read_csv("df")
    select1 = st.sidebar.selectbox("Choose",["Prediction","Classification"])
    if select1=="Prediction":
        runpredictions.load_page(df)
    if select1=="Classification":
        runpredictions.classification()

