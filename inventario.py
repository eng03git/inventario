######################################################################################################
                                           #Introduaao
######################################################################################################



######################################################################################################
                                 # importar bibliotecas
######################################################################################################

import streamlit as st
from streamlit import caching
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
#import json
#import smtplib
from datetime import  datetime, time
import pytz
#import base64
from io import StringIO
import pymongo
from st_aggrid import AgGrid
from pylogix import PLC
from PIL import Image
import io
import matplotlib.pyplot as plt
import cv2
from pyzbar.pyzbar import decode

######################################################################################################
				#Configuraaaes da pagina
######################################################################################################

st.set_page_config(
     page_title="Inventario",
     #layout="wide",
)

######################################################################################################
				#Configurando acesso ao mongodb
######################################################################################################


def read_barcodes(frame):
    barcodes = decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect        #1
        barcode_info = barcode.data.decode('utf-8')
        # cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        # #2
        # font = cv2.FONT_HERSHEY_DUPLEX
        # cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)        #3
        # with open("barcode_result.txt", mode ='w') as file:
        #     file.write("Recognized Barcode:" + barcode_info)    
            
        return barcode_info


# Configurando o acesso ao mongodb
myclient = pymongo.MongoClient("mongodb://192.168.81.128:27017/")
mydb = myclient["mydatabase"]

# upload de imagem para mongodb
images = mydb.images
# im2 = st.file_uploader('Selecione a imagem para upload')

# if im2 != None:
#     image = {
#         '_id': 'imagem1',
#         'data': im2.getvalue()
#     }
#     myquery = {'_id': 'imagem1'}
#     newvalues = {"$set":{'data': im2.getvalue()}}

#     images.update_one(myquery, newvalues)

# # busca de imagem no mongodb
# query = {'_id': 'imagem1'}
# image = images.find(query)

# for doc in image:
#     st.image(io.BytesIO(doc['data']))

# st.image(io.BytesIO(im2.getvalue()))


##### Sidebar #####

st.sidebar.image('latas minas.png')

telas = ['Inserir item no inventario', 'Atualizar item no inventario', 'Visualizar inventarios']
tela = st.sidebar.radio('Menu', telas)

######################################################################################################
                               #Funaoes
######################################################################################################


st.title('Inventario Ambev - LM :memo:')
if tela == 'Inserir item no inventario':
    st.subheader('Formulario')

    with st.form(key='myform'):
        st.text_input('data do inventario') # data
        st.text_input('empresa')
        st.text_input('Unidade') #latas minas 
        st.text_input('Numero do bem')
        st.text_input('situacao') #opcoes:
        st.text_input('Descricao do ativo')
        st.text_input('loca/departamento')
        st.text_input('Responsavel pela localizacao')
        st.text_input('Numero TAG/Paleta')
        st.text_input('Turnos para uso do bem') #opcoes a,b,c,todos a e b, a e c, b e c
        st.text_input('data da aquisicao') #data
        st.text_input('Marca')
        st.text_input('Modelo')
        st.text_input('Numero de serie')
        st.text_input('Quantidade')

        submit_button = st.form_submit_button(label='Submit')

    st.write('TAG do equipamento')
    im1 = st.file_uploader('Selecione a foto da TAG')
    if im1 != None:
        st.image(io.BytesIO(im1.getvalue()))
        st.button('Confirma envio da foto da TAG?')

    st.write('Foto do equipamento')
    im2 = st.file_uploader('Selecione a foto do equipamento')
    if im2 != None:
        st.image(io.BytesIO(im2.getvalue()))
        st.button('Confirma envio da foto do equipamento?')
       

if tela == 'Visualizar inventarios':
    im2 = st.file_uploader('Selecione a foto do equipamento')

    if im2 is not None:
        file_bytes = io.BytesIO(im2.getvalue())
        image = cv2.imdecode(np.frombuffer(file_bytes.read(), np.uint8), cv2.IMREAD_COLOR)
        # qrCodeDetector = cv2.QRCodeDetector()
        # decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
        # qr_data = decodedText.split(',')
        # st.write(qr_data[0])
        valor = read_barcodes(image)
        st.write(valor)