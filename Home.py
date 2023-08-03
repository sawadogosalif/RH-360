import streamlit as st
from PIL import Image
import streamlit as st
from datetime import datetime

# You can always call this function where ever you want

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://media.glassdoor.com/sqll/799976/siaci-saint-honore-squareLogo-1625563554225.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
 """,
        unsafe_allow_html=True,
    )



st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
add_logo()

st.write("# Welcome to S2H RH 360 Dashboard! 👋")
st.markdown(
    """
    Dans ce tableau de bord, vous aurez la possibilité d'observer l'avanceement du PoC
  
    ### Les niveaux d'analyses?
    - Une vision globale
    - Une analyse par collaborateur
    - Analyse mix
       ### Want to learn more?
    - Visiter  [streamlit.io](https://streamlit.io)
    - Utiliser la   [documentation officielle](https://docs.streamlit.io)
	"""
)



d = st.date_input(
    "When's your birthday",
    datetime.date(2019, 7, 6))
st.write('Your birthday is:', d)