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
serie_leliqs = '7926'
leliqs = bcrautils.getDf(fecha_desde, fecha_hasta, serie_leliqs)
leliqs.set_index('Fecha')
leliqs.rename(columns={'Valor':'Leliqs'}, inplace=True)
####################################################################################################################################################################################
serie_bm = '250'
base_monetaria = bcrautils.getDf(fecha_desde, fecha_hasta, serie_bm)
base_monetaria.set_index('Fecha')
base_monetaria.rename(columns={'Valor':'Base Monetaria'}, inplace=True)
####################################################################################################################################################################################
joined_df = pd.merge(leliqs, base_monetaria, how='inner', on = 'Fecha')
bcrautils.plot(df=joined_df, y=["Base Monetaria","Leliqs"], title="Base monetaria (en millones de pesos)", legend=True, color = ['lightgreen', 'lightblue'], days=days)
####################################################################################################################################################################################
plt.savefig(home_dir+'/IMG/base_monetaria.png')
bcrautils.send_telegram_photo(home_dir+'/IMG/base_monetaria.png')