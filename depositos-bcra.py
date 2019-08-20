#!/usr/bin/env python3
# coding=utf-8

#uncomment these lines if you are running in a server without screen
#import matplotlib
#matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import datetime
from math import sqrt
from os import environ
import bcrautils #file bcrautils.py
####################################################################################################################################################################################
home_dir = environ["HOME"]
today = datetime.datetime.today().date()
fecha_hasta = pd.to_datetime(today)
fecha_desde = fecha_hasta - pd.DateOffset(months=3)
delta = fecha_hasta - fecha_desde
days = mdates.DayLocator(interval = round(sqrt(delta.days)))
####################################################################################################################################################################################
serie_depositos='450'
depositos = bcrautils.getDf(fecha_desde, fecha_hasta, serie_depositos)
####################################################################################################################################################################################
serie_tc='7927'
tipo_cambio = bcrautils.getDf(fecha_desde, fecha_hasta, serie_tc)
tipo_cambio.rename(columns={'Valor':'ValorDolar'}, inplace=True)
####################################################################################################################################################################################
joined_df = pd.merge(tipo_cambio, depositos, how='inner', on = 'Fecha')
joined_df['Depositos en Dolares'] = joined_df.apply(lambda row : round(row.Valor / row.ValorDolar, 2), axis=1)
joined_df.drop(columns=['Valor', 'ValorDolar'], axis=1, inplace=True)
####################################################################################################################################################################################
bcrautils.plot(df=joined_df, y='Depositos en Dolares', title='Depositos en cajas de ahorro (en miles de USD)', days=days)
####################################################################################################################################################################################
plt.savefig(home_dir+'/IMG/depositos.png')
bcrautils.send_telegram_photo(home_dir+'/IMG/depositos.png')
####################################################################################################################################################################################