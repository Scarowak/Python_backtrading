# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 06:20:41 2023

@author: Krzychu
"""
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

import pandas_ta as ta


fee_taker = 0.00036 
    
fee_maker = 0.00018 

SMA = 24*7*2

df = pd.read_csv("C:/Users/Krzychu/Desktop/Binance_BTCUSDT_1h (1).csv")
#df = pd.read_csv("C:/Users/Krzychu/Desktop/Binance_ETHUSDT_1h.csv")
#df = pd.read_csv("C:/Users/Krzychu/Desktop/Binance_AAVEUSDT_1h.csv")
#df = pd.read_csv("C:/Users/Krzychu/Desktop/Binance_BNBUSDT_1h.csv")
#df = pd.read_csv("C:/Users/Krzychu/Desktop/DOGEUSDT_Binance_futures_UM_hour.csv")


#df = pd.read_csv("C:/Users/Krzychu/Desktop/minutes/Binance_BTCUSDT_2020_minute.csv")
#df = pd.read_csv("C:/Users/Krzychu/Desktop/minutes/Binance_BTCUSDT_2021_minute.csv")
#df = pd.read_csv("C:/Users/Krzychu/Desktop/minutes/Binance_BTCUSDT_2022_minute.csv")
#df = pd.read_csv("C:/Users/Krzychu/Desktop/minutes/Binance_BTCUSDT_2023_minute.csv")

df = df[::-1]

df.reset_index(inplace=True, drop = True)



try:
  df['Datetime'] = df['Date']
  #df['Datetime'] = df['date']
  

except:
  df['Datetime'] = df['ndex']




try:
    
  df['Close'] =df['close'] 
  df['High'] =df['high'] 
  df['Low'] =df['low'] 
  
except:
  print('OK')              



df = df[['Datetime', 'Close', 'High', 'Low']]




df['MA'] = ta.sma(df['Close'], length=SMA)

df['MA_1'] = df['MA'] *0.9 #buy

df['MA_5'] = df['MA'] *1.1 #sell



df['Buy'] = np.where(df['Close']<df['MA_1'], df['Close'], np.nan)
df['Sell'] = np.where(df['Close']>df['MA_5'], df['Close'], np.nan)


plt.plot(df['Close'])
plt.plot(df['Buy'], color='green')

plt.plot(df['Sell'], color='red')

plt.savefig('SMA5.png', dpi=800)