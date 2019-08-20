#!/usr/bin/env python3
# coding=utf-8

#uncomment these lines if you are running in a server without screen
#import matplotlib
#matplotlib.use('Agg')

import requests
import lxml.html as lh
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
serie_reservas = '246'
df = bcrautils.getDf(fecha_desde, fecha_hasta, serie_reservas)
####################################################################################################################################################################################
bcrautils.plot(df=df, y='Valor', title='Reservas BCRA (en miles de USD)', days=days)
####################################################################################################################################################################################
plt.savefig(home_dir+'/IMG/reservas.png')
bcrautils.send_telegram_photo(home_dir+'/IMG/reservas.png')