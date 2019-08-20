#!/usr/bin/env python
# coding=utf-8

import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import datetime
from os import environ

session = requests.Session()

headers = {
    'Origin':'http://www.bcra.gov.ar',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer':'http://www.bcra.gov.ar/PublicacionesEstadisticas/Principales_variables_datos.asp',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'es-ES,es;q=0.9,en;q=0.8,gl;q=0.7,fr;q=0.6,pt;q=0.5,it;q=0.4',
    'Cookie':'ASPSESSIONIDQSRRDTSQ=GLCHIGJDGFANGHJMNFADKGJE'
}

url = 'http://www.bcra.gov.ar/PublicacionesEstadisticas/Principales_variables_datos.asp'

def getDf(fecha_desde, fecha_hasta, serie, serie1='0', serie2='0', serie3='0', serie4='0'):
    payload = {
        'B1':'Enviar',
        'fecha_desde':fecha_desde,
        'fecha_hasta':fecha_hasta,
        'primeravez':'1',
        'serie':serie,
        'serie1':serie1,
        'serie2':serie2,
        'serie3':serie3,
        'serie4':serie4
    }

    page = session.post(url, headers = headers, data = payload)

    doc = lh.fromstring(page.content)

    tr_elements = doc.xpath('//tr')

    col=[]
    i=0

    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        col.append((name,[]))


    for j in range(1,len(tr_elements)):

        T=tr_elements[j]
        
        i=0
        
        for t in T.iterchildren():
            data=t.text_content().strip().replace('.', '').replace(',', '.')
            try:
                data=int(data)
            except:
                pass
            
            col[i][1].append(data)
            
            i+=1

    Dict={title:column for (title,column) in col}

    df = pd.DataFrame(Dict)

    df['Fecha'] = pd.to_datetime(df['Fecha'], format="""%d/%m/%Y""")
    df['Valor'] = df['Valor'].apply(pd.to_numeric)
    df.set_index('Fecha')

    return df

def plot(df, y, title, days, color='lightgreen', linewidth=5, x='Fecha', legend=False, grid=True):
    sns.set(rc={'figure.figsize':(11, 5)})
    df.plot(linewidth=linewidth, x=x, y=y, title=title, legend=legend, color=color, grid=grid,  xticks=([df['Fecha'].min(), df['Fecha'].max()]), xlim=((df['Fecha'].min()-pd.DateOffset(days=2)), (df['Fecha'].max()+pd.DateOffset(days=2)))).xaxis.set_major_locator(days)


def send_telegram_photo(file_location, caption=''):
    bot = environ["BOT_TOKEN"]
    chat_id = environ["CHAT_ID"]
    url = "https://api.telegram.org/bot{}/sendPhoto?chat_id={}&caption={}".format(
        bot, chat_id, caption
    )
    files = {'photo': open(file_location, 'rb')}
    r = session.post(url, files=files)
    pass