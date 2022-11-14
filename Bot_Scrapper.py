#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import threading
import time
from telegram.ext import (Updater, CommandHandler)


# In[2]:


def get_falabella_data():
    url = "https://linio.falabella.com/linio-cl/category/cat720161/Smartphones?facetSelected=true&f.product.brandName=apple&f.range.derived.variant.discount=50%25+dcto+y+m%C3%A1s"

    respuesta = requests.get(
            url,
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }
        )
    contenido_web = BeautifulSoup(respuesta.text, 'lxml')
    seccion = contenido_web.find('div', attrs={'id':'testId-searchResults-products'})

    precios = seccion.findChildren('b')
    
    x = re.findall("\$..\w+\.\w+", str(seccion))
    
    precios = re.findall('(?<=">).*?(?=<\/)', str(precios))
    
    celulares = []
    for i in precios:
        if len(i) > 13:
            celulares.append(i)
    
    nueva_lista = []
    for elemento in np.arange(len(x)):
        if elemento % 2 == 0:
            nueva_lista.append(x[elemento])

    data = {"Celulares": celulares,"Precio":nueva_lista}
    df = pd.DataFrame(data)
    string = ""
    for i in np.arange(len(df)):
        string = string+" | "+str(df.Celulares[i])+" Precio: "+df.Precio[i]
    
    return string


# In[ ]:


def start(update, context):
    ''' START '''
    # Enviar un mensaje a un ID determinado.
    bienvenida = "Bienvenido! \nTe enviaré cada 5 minutos las actualizaciones.\nHaz click en /actualiza para comenzar"
    context.bot.send_message("-886124178", bienvenida)
    
def actualiza(update,context):
    while(True):
        context.bot.send_message("-886124178", get_falabella_data())
        time.sleep(300)
    
def main():
    TOKEN="5497341473:AAEYYRlAQ8y-PXPP0RyBN_HUnKxrn-s08qs"
    updater=Updater(TOKEN, use_context=True)
    dp=updater.dispatcher
    
    # Eventos que activarán nuestro bot.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('actualiza', actualiza))
    #group_id = "-886124178"
    
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()


if __name__ == '__main__':
    main()


# In[ ]:




