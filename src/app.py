# Import necessary libraries
import streamlit as st
from pickle import load
import xgboost
import numpy as np

################################
import pandas as pd
import json




#### Eliminamos el boton superior de deploy

st.set_page_config(page_title="Mental Health Care", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)





X_train = pd.read_csv("../data/processed/X_train_sel.csv")
todas_columnas = X_train.columns

# JSON file source in SPANISH
#ruta_json = "../data/json_files/full_var_dict.json"

# JSON file source in ENGLISH
ruta_json='../data/json_files/english_json.json'

# loading JSON file
with open(ruta_json, 'r') as archivo:
    varijson = json.load(archivo)


def parse_json(columna):
    categories = list(varijson[columna]['dictionary'].values())
    categories = [str(cat) for cat in categories]

    values=list(varijson[columna]['dictionary'].keys())
    values = [int(cat) for cat in values]
    
    title = varijson[columna]['Description']

    return values, categories, title

valores = []
categorias = []
titulos = []

for column in todas_columnas:
    val, cat, titl = parse_json(column)

    valores.append(val)
    categorias.append(cat)
    titulos.append(titl)

################################ CARGA MODELO

# Load the pre-trained machine learning model
model = load(open("../models/boost_final.pk", "rb"))



##################### EDICION DISEÑO




# Set the title and description for the Streamlit app
st.title("Depression or Anxiety Risk Prediction using European Mental Health Survey Data for Spain (2020)")

st.image('../assets/emotionalmental_sp23_1200x540.jpg')

st.subheader("Welcome to our machine learning project focused on predicting the risk of depression or anxiety using data from the European Mental Health Survey for Spain in 2020. We leverage a comprehensive dataset with approximately 400 columns and 22,000 rows of survey responses to develop a predictive model aimed at identifying individuals more prone to experiencing depression or anxiety.")


respuestas = []


for cats, titl, valor_prdeterminado in zip(categorias, titulos, [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 1, 1, 1]):

    if len(cats) < 3:
        # Checkbox para opciones cortas
        opcion_seleccionada = st.radio(titl, cats, index=valor_prdeterminado)
        respuestas.append(opcion_seleccionada)

    else:
        # Radio para opciones largas
        opcion_seleccionada = st.radio(titl, cats, index=valor_prdeterminado)
        respuestas.append(opcion_seleccionada)
    

#######################################


def parse_json_inversa(var,respuesta):


    for clave, valor in varijson[var]['dictionary'].items():

        if valor == respuesta:
            return clave   

respuestas_numero =[]

for columna, respuesta in zip(todas_columnas,respuestas):

    respuestas_numero.append(int(parse_json_inversa(columna,respuesta)))

###########################################
    

# Mostrar la opción seleccionada
print(respuestas)
print(respuestas_numero)




# Define a dictionary to map model predictions to human-readable messages
prediction_messages = {
    0: "Based on the model prediction, it suggests that you are at a lower risk of experiencing depression or anxiety.",
    1: "The model predicts a higher likelihood of experiencing depression or anxiety. It is advisable to seek professional advice or support."
}


# Button to trigger the prediction
if st.button("Predict"):

    # Make a prediction using the model
    prediction = model.predict([respuestas_numero])[0]

    print(prediction)

    # Get the probabilities of each class
    class_indices = np.argmax(model.predict_proba([respuestas_numero]), axis=1)
    probabilities = model.predict_proba([respuestas_numero])[0]
    
    print('Prediction:', prediction)
    print('Probabilities:', probabilities[1] *100)

    pred_val = prediction_messages.get(prediction)



    st.write('Prediction:', pred_val)

    # Probabilities
    probability = probabilities[1] * 100
    formatted_probability = "{:.2f}".format(probability)
    st.write(f'The probability that the patient presents symptoms of anxiety or depression is about {formatted_probability}%')
