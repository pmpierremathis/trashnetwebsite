from re import S
import streamlit as st
import requests
from PIL import Image
import time

'''
# Bienvenue sur Garby.ai, votre assistant poubelle !
'''
st.markdown("""
    Vous ne savez pas dans quelle poubelle mettre votre déchet ?
    Laissez notre réseau de neurones *Garby Le Magnifique* s'en occuper pour vous !
    """)


st.markdown("""
    ### Comment ça marche ?
    """)

st.markdown("""
    C'est très simple : **prenez une photographie de votre déchet, et transmettez-la ci-dessous à Garby**. Il vous donnera immédiatement la réponse.
    """)

uploaded_file = st.file_uploader("Importez votre image ici:")

url_predict = 'http://127.0.0.1:8000/predict/image'
url_labelling = 'http://127.0.0.1:8000/labelling'
# url_predict = 'https://image-trashnet-znuzg7cgua-ew.a.run.app/predict/image'

if uploaded_file is not None:
    data = uploaded_file.read()
    st.image(data)
    files = {'file' : data}
    response_predict = requests.post(url_predict, files=files)
    translation = {
        'paper' : 'Papier',
        'cardboard' : 'Carton',
        'glass' : 'Verre',
        'plastic' : 'Plastique',
        'metal' : 'Métal',
        'trash' : 'Ordures ménagères'
    }
    
    option_translation = {
        'Papier' : 'paper',
        'Carton' : 'cardboard',
        'Verre' : 'glass',
        'Plastique' : 'plastic',
        'Métal' : 'metal',
        'Ordures ménagères' : 'trash',
        "Ceci ne va pas à la poubelle !" : "other"
        }
    
    # my_bar = st.progress(0)
    # for percent_complete in range(100):
    #     time.sleep(0.1)
    #     my_bar.progress(percent_complete + 1)
        
     ## IF GARBY IS ABLE TO MAKE A PREDICTION  
    if response_predict.json()['probability'] >= 0.90:
        st.markdown("""
        ### Garby est confiant à plus de 90% que votre déchet doit aller dans la poubelle :
        """)
        st.success(translation[response_predict.json()['prediction']])
        trash_image = Image.open(f"{response_predict.json()['prediction']}.png")
        st.image(trash_image)
        
        # USER VALIDATE THE PREDICTION
        st.write("Êtes-vous d'accord avec cette prédiction?")
        yes = st.button('Oui')
        no = st.button('Non')
        if yes:
            st.write('Merci pour votre aide ! A bientôt 🎉')
            checked_label = response_predict.json()['prediction']
            data = {"checked_label" : checked_label}
            requests.post(url_labelling, data = data, files = files)
            st.markdown("""
            ### Et voilà ! Merci qui ? Merci Garby !
            """)
            image = Image.open('leo.png')
            st.image(image, caption='This goes into the glass trash bro', use_column_width=False)
    
        # USER CHANGE THE PREDICTION
        if no:
            option = st.selectbox('Selon vous, ce déchet doit aller dans la poubelle :',("Faites votre choix", 'Papier', 'Carton', 'Métal', 'Plastique', 'Verre', 'Ordures ménagères', 'Ceci ne va pas à la poubelle !'))
            if option=="Faites votre choix":
                pass
            else:
                st.write('Merci pour votre aide ! A bientôt 🎉')
                image = Image.open('leo.png')
                st.image(image, caption='This goes into the glass trash bro', use_column_width=False)
                checked_label = option_translation[option]
                data = {"checked_label" : checked_label}
                requests.post(url_labelling, data = data, files = files)
        
    ## IF GARBY IS NOT ABLE TO MAKE A PREDICTION  
    else:
        st.markdown("""
            ## Garby n'est pas certain de pouvoir vous aider. Pouvez-vous lui donner votre meilleure estimation ?
            """)

        option = st.selectbox('Selon vous, ce déchet doit aller dans la poubelle :',('Papier', 'Carton', 'Métal', 'Plastique', 'Verre', 'Ordures ménagères', 'Ceci ne va pas à la poubelle !'))
        validate2 = st.button('Je valide')
        if validate2:
            st.write('Merci pour votre aide ! A bientôt 🎉')
            image = Image.open('leo.png')
            st.image(image, caption='This goes into the glass trash bro', use_column_width=False)
            checked_label = option_translation[option]
            data = {"checked_label" : checked_label}
            requests.post(url_labelling, data = data, files = files)
