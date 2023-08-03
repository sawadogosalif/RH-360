import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to S2H RH 360 Dashboard! 👋")
st.sidebar.image("./INPUT/logo.png", use_column_width=True)
st.sidebar.success("Select a demo above.")

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