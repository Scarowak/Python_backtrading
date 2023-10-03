# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 06:58:04 2023

@author: Krzychu
"""

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



df = pd.read_csv("C:/Users/Krzychu/Desktop/Binance_BTCUSDT_1h (1).csv")


df = df[::-1]

df.reset_index(inplace=True, drop = True)



try:
  df['Datetime'] = df['Date']
  #df['Datetime'] = df['date']
  

except:
  df['Datetime'] = df['index']




try:
    
  df['Close'] =df['close'] 
  df['High'] =df['high'] 
  df['Low'] =df['low'] 
  
except:
  print('OK')              





df = df[['Datetime', 'Close', 'High', 'Low']]


df['111'] = ta.sma(df['Close'], length=111)

df['350'] = ta.sma(df['Close'], length=350)

df['350'] = df['350']* 1.1


df['111-1'] = df['111'].shift(1)
    
    
df['Sell'] = np.where(np.logical_and(   df['111']>df['350'] , df['111-1']<df['350'] ), df['Close'], np.nan)







df['Close_B'] = 1/df['Close']


df['111_B'] = ta.sma(df['Close_B'], length=111)

df['350_B'] = ta.sma(df['Close_B'], length=350)

df['350_B'] = df['350_B']* 1.1

df['350_buy'] = df['350_B']* 0.8


df['111-1_B'] = df['111_B'].shift(1)
    
    
df['Buy'] = np.where(np.logical_and(   df['111_B']>df['350_B'] , df['111-1_B']<df['350_B'] ), df['Close'], np.nan)



buy = 0 

df['profit'] = np.nan
df['cumulative_profit'] = np.nan



for i in range(len(df)):
    
    if ~np.isnan(df['Buy'][i]) and buy == 0: 
        
        buy  = df['Buy'][i]      

    if ~np.isnan(df['Sell'][i]) and buy != 0:

        sell = df['Sell'][i]
        profit = sell / buy -1
        
        df['profit'][i] = profit
        

        buy = 0
        
    df['cumulative_profit'][i] = df['profit'][:i].sum()  

print(df['cumulative_profit'][i])

plt.figure(figsize=(20, 10))
plt.plot(df['Close'], linewidth=0.3, color='black')
#plt.plot(df['111'], color='yellow', linewidth=0.3)
#plt.plot(df['350'], color='green', linewidth=0.3)
plt.scatter(df.index, df.Sell, s = 1.5, color='red')
plt.scatter(df.index, df.Buy, s = 1.5, color='green')
#plt.legend(["111", "350"])
plt.savefig('Pi Cycle Top.png', dpi=1200)

#plt.savefig('Pi Cycle Top_2.png', dpi=600)