import streamlit as st
import requests
from PIL import Image

'''
# Mais dans quelle poubelle dois-je mettre ce déchet ?
'''

st.markdown("""
    ### Bienvenue sur Garby.ai, votre assistant poubelle !""")

st.markdown("""
    Vous ne savez pas dans quelle poubelle mettre votre déchet ?
    Laissez notre réseau de neurones *Garby Le Magnifique* s'en occuper pour vous !
    """)


st.markdown("""
    ## Génial ! Comment ça marche ?
    """)

st.markdown("""
    C'est très simple : prenez une photographie de votre déchet, et transmettez-la à Garby. Il vous donnera immédiatement la réponse.
    """)

uploaded_file = st.file_uploader("Importez votre image ici:")

url = 'http://127.0.0.1:8000/predict/image'
# url = 'https://image-trashnet-znuzg7cgua-ew.a.run.app/predict/image'

if uploaded_file is not None:
    data = uploaded_file.read()
    st.image(data)
    files = {'file' : data}
    response = requests.post(url, files=files)
    translation = {
        'paper' : 'Papier',
        'cardboard' : 'Carton',
        'glass' : 'Verre',
        'plastic' : 'Plastique',
        'metal' : 'Métal',
        'trash' : 'Ordures ménagères'
    }
    
    if response.json()['probability'] >= 0.9:
        st.markdown("""
        ## Selon Garby, votre déchet doit aller dans la poubelle :
        """)
        st.write(translation[response.json()['prediction']])
        
        st.markdown("""
        ## Le niveau de confiance de Garby est de :
        """)
        st.write(round(float(response.json()['probability'])*100,3))
        
        st.markdown("""
        ## Et voilà ! Merci qui ? Merci Garby !
        """)

        image = Image.open('leo.png')
        st.image(image, caption='This goes into the glass trash bro', use_column_width=False)

    else:
        st.markdown("""
            ## Garby n'est pas certain de pouvoir vous aider. Pouvez-vous lui donner votre meilleure estimation ?
            """)

        option = st.selectbox('Selon vous, ce déchet doit aller dans la poubelle :',('Papier', 'Carton', 'Métal', 'Plastique', 'Verre', 'Ordures ménagères', 'Ceci ne va pas à la poubelle !'))

        if st.button('Je valide'):
            st.write('Merci pour votre aide ! A bientôt 🎉')
            image = Image.open('leo.png')
            st.image(image, caption='This goes into the glass trash bro', use_column_width=False)

