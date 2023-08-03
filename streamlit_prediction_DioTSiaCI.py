# -*- coding: utf-8 -*-

import os
import pandas as pd
import pickle




###########################################################################
###########################################################################
# Constantes vers les répertoires et les pickles
###########################################################################
###########################################################################
#les pickles sont stockés dans le sous-répertoire deployment



############################################################################
f = open("./INTERMED/random_forest_model.sav", "rb" )
#charger le fichier
modele=pickle.load(f)
# fermer le fichier
f.close()


with open("./INTERMED/vectorizer.sav", "rb" ) as f:
	vectorizer=pickle.load(f)


ref = 0.135



############################################################################

############################################################################
# Partie spécifique à streamlit
############################################################################
############################################################################
import streamlit as st

Description  = st.text_input("Veuillez renseigner la description de l'entreprise")




#page principale

st.header("**Prédiction probabilité de la classe positive**")

st.subheader("Données saisies")
st.write(Description)  


X_profil = pd.DataFrame(     [[         Description  ,
                               ]],
                                    columns=[ 'Description'  
                                            ]
                        )

  


if(st.button("Calculer le score d'apparténance à classe positive")): 
    v = vectorizer.transform(X_profil['Description'])
    proba = modele.predict_proba(v)[:,1]

    # appeler la fonclion cliked_button lorsqu'on appui sur cliquer
    st.subheader("Résultat du score")
    st.write(f"Probabilité calculée {proba}")
    if proba< ref:
       st.success("Class= False  : 👍 Go Pas de problème")
    else:
       st.error(f"Probabilité > {ref*100}*  : 😭 Class=True")