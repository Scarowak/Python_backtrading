# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 15:58:51 2023

@author: Krzychu
"""

# Importowanie bibliotek
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

import pandas_ta as ta





wyniki = pd.DataFrame(columns = ['i_window', 'i_sma', 'profit', 'chunk', 'minus_chunk'])

for i_window in range(7, 8):
    
    for i_sma in range(22,23):
            
                window = 24*i_window
                
                
                fee_taker = 0.00036 
                    
                fee_maker = 0.00018 
                
                
                
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
                
                
                
                '''
                df['Close'] = 1/df['Close']
                df['High'] = 1/df['High']
                df['Low'] = 1/df['Low']
                '''
                
                df['SMA_slow'] = ta.sma(df['Close'], length = 24 *i_sma)
                
                
                
                local_min = 0
                amplitude = 0
                
                buy = 0
                take_profit = 1000000000
                stop_loss = 0
                df['buy'] = np.nan
                df['sell'] = np.nan
                df['profit'] = np.nan
                df['cumulative_profit'] = np.nan
                
                for i in range(window, len(df)):
                  sd = df[i-window:i+1]
                  sd.reset_index(inplace = True, drop = True)
                
                  sd_max =  sd['Close'].max()
                  sd_min = sd['Close'].min()
                  sd_amp = sd_max - sd_min
                
                  if buy == 0 and df['Close'][i] < (local_min + sd_amp / 3) and df['Close'][i] > (local_min + sd_amp / 4)  and df['Close'][i]>df['SMA_slow'][i]:
                  #if buy == 0 and df['Low'][i] < local_min:
                
                    buy = df['Close'][i] * ( 1 + fee_taker)
                    #buy = local_min 
                    
                    
                
                    max = sd['Close'].max()
                    min = sd['Close'].min()
                    amplitude = max - min
                    take_profit = min + (2 * sd_amp) / 3
                    stop_loss = min 
                    df['buy'][i] = buy
                
                
                  elif buy != 0 and df['Low'][i] <= stop_loss :
                    sell = stop_loss * ( 1 - fee_maker)
                    df['sell'][i] = sell 
                    df['profit'][i] = (sell - buy)/buy 
                    buy=0
                
                    if df['profit'][i]> 0 :
                        print('error')
                    
                
                  elif buy != 0 and df['High'][i] >= take_profit :
                    sell = take_profit * ( 1 - fee_maker)
                    df['sell'][i] = sell
                    df['profit'][i] = (sell - buy)/buy
                    buy=0
                    
                    
                
                  df['cumulative_profit'][i] = df['profit'][:i].sum()    
                  
                  
                  
                
                      
                  local_min = sd['Close'].min()
                  
                
                plt.title(str(window))
                plt.plot(df.index, df.cumulative_profit)
                plt.show()
        
        

        
        
                wyniki = wyniki.append({'i_window' : i_window,
                                        'i_sma' : i_sma,
                                        'profit' : df['cumulative_profit'][i],
                                        },
                                       ignore_index = True)





profits = df.copy()
profits = profits["profit"]
profits.dropna(inplace = True)

investment = 100

balance_list = [0]

reinvest = 0.33 

account_balance = 100

levar = 10  


for profit in profits:
    
    lucre = ( profit* levar) * account_balance * reinvest
    
    account_balance = account_balance + lucre
    
    balance_list.append(account_balance)


        
plt.title('Balance')
plt.suptitle(balance_list[-1])  
plt.plot(balance_list) 
plt.show()



plt.figure(figsize=(20, 10))
plt.plot(df['Close'], linewidth=0.3, color='black')
#plt.plot(df['111'], color='yellow', linewidth=0.3)
#plt.plot(df['350'], color='green', linewidth=0.3)
plt.scatter(df.index, df.sell, s = 1.5, color='red')
plt.scatter(df.index, df.buy, s = 1.5, color='green')
#plt.legend(["111", "350"])
plt.savefig('window_csv.png', dpi=1200)

