import time
import numpy as np  
import pandas as pd 
import plotly.express as px  
import streamlit as st 
from datetime import datetime


def get_data() -> pd.DataFrame:
    df2 =  pd.read_pickle(r"C:\Users\sawal\OneDrive - UPEC\Diot-Siaci\OUTPUT\presence_anomalies.pkl")
    df1 = pd.read_pickle(r"C:\Users\sawal\OneDrive - UPEC\Diot-Siaci\OUTPUT\presence_indcator.pkl")
    df3 = pd.read_pickle(r"C:\Users\sawal\OneDrive - UPEC\Diot-Siaci\OUTPUT\presence_agg.pkl")
    return df1,df2,df3


# dashboard setup

st.set_page_config(
    page_title="RH 360 Dashboard",
    page_icon="✅",
    layout="wide",
)

# TITLE 
st.title("RH 360 Dashboard")


df_indicator, df_anomalies, df_agg = get_data()




st.date_input(label, value=datetime(2021, 10,1), min_value=datetime(2013,1,1), max_value=datetime(2022,10,1), key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")
start_time = st.slider(
    "When do you start?",
    value=datetime(2020, 1, 1, 9, 30),
    format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)


# filters
filtre = st.selectbox("Select the id", pd.unique(df_anomalies["id"]))
# dataframe filter
#df_indicator = df_indicator[df_indicator["id"] == filtre]
#df_agg = df_agg[df_agg["id"] == filtre]
#df_anomalies = df_anomalies[df_anomalies["id"] == filtre]

# -- FILTER DATE
cols, continent_col, log_x_col = st.columns([5, 5, 5])
with cols:
	slider  = st.sidebar.select_slider('Select date', 
			min_value=dt.datetime(year=2007,month=1,day=1),
		        value=dt.datetime.now() ,
			max_value=dt.datetime.now())

# -- Apply the year filter given by the user

df_indicator = df_indicator[df_indicator["date"] <= slider ]
df_agg = df_agg[df_agg["mois"] <= slider ]
df_anomalies = df_anomalies[df_anomalies["date_fin"] <= slider ]


# creating a single-element container
placeholder = st.empty()
# creating KPIs
sum_abscence = np.sum(df_indicator["presence"])
ratio_abscence = sum_abscence/ len(df_indicator["presence"]) 
periods = len(df_anomalies) 

with placeholder.container():

    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Nombre total d'abscence ⏳",
        value=int(sum_abscence),
    )
    
    kpi2.metric(
        label="Taux de depart pou congés",
        value=f"{round(ratio_abscence*100)} abscences/ 100 jours",
    )
    
    kpi3.metric(
        label="Nombre de périodes de congés",
        value=int(periods),
    )
    

    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Heatmap periodes d'abscence par collaborateur")
        fig = px.density_heatmap(
            data_frame=df_agg, y="NB_arret", x=df_agg['mois'].dt.strftime('%b')
        )
        st.write(fig)
        
    with fig_col2:
        st.markdown("### distribution periodes d'abscence par collaborateur")
        fig2 = px.histogram(data_frame=df_agg, x="NB_arret")
        st.write(fig2)
     
   
    df_agg['mois'] = df_agg['mois'].dt.strftime('%Y-%m-%d')
    df_agg['date_debut'] = df_agg['date_debut'].dt.strftime('%Y-%m-%d')
    df_agg['date_fin'] = df_agg['date_fin'].dt.strftime('%Y-%m-%d')
    
    
    st.markdown("### Details des données individuelles")
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    df_agg = df_agg.drop("id", axis=1)
    tab1.subheader("A tab with a chart")
    tab1.line_chart(df_agg, y="NB_arret", x='mois')

    tab2.subheader("A tab with the data")
    tab2.write(df_agg, y="NB_arret", x='mois')
