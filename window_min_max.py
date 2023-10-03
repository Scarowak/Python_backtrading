
# Importowanie bibliotek
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from datetime import date
pd.options.mode.chained_assignment = None # default='warn'


#Pobranie danych

company=[ 'BTC-USD', "SHIB-USD", 'DOGE-USD', 'ETH-USD', 'ADA-USD', 'XRP-USD', 'NEO-USD', 'XLM-USD', 'DOT-USD', 'BNB-USD'] # Wybór waluty, dane z https://finance.yahoo.com/  
#company=[ "GC=F"] # Wybór waluty, dane z https://finance.yahoo.com/  

x = 0.4
window = 18


fee_buy = 0.0360 * 0.01
    
fee_sell = 0.0180 * 0.01  
    
def download_df_long(company):  
    end=date.today() #koniec danych
    delta = 729
    
    
    start= end - dt.timedelta(days = delta) #początek danych
        
    #start= dt.datetime(1990,2,1)

    yf.pdr_override() 
    df=pdr.get_data_yahoo(c, start, end, interval = "1H") 
    df.reset_index(inplace=True)
    
    
    try:
      df['Datetime'] = df['Date']
    
    
    except:
      df['Datetime'] = df['index']
    
    

    
    
    df = df[['Datetime', 'Close', 'High', 'Low']]
    
    return df

def short_df(df):
    
    
    xd = df.copy()
    
    xd['Close'] = 1/df['Close']
    xd['High'] = 1/df['High']
    xd['Low'] = 1/df['Low']
    
    
    return xd


def back_trade (df):


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
      
    
    
      if buy == 0 and df['Close'][i] < local_min:
      #if buy == 0 and df['Low'][i] < local_min:
    
        buy = df['Close'][i] * ( 1 + fee_buy)
        #buy = local_min 
        
        
    
        max = sd['Close'].max()
        min = sd['Close'].min()
        amplitude = max - min
        take_profit = min + amplitude * x
        stop_loss = min - (amplitude * x / 3) 
        df['buy'][i] = buy
    
    
      elif buy != 0 and df['Low'][i] <= stop_loss :
        sell = stop_loss * ( 1 - fee_sell)
        df['sell'][i] = sell 
        df['profit'][i] = (sell - buy)/buy 
        buy=0
    
        
    
      elif buy != 0 and df['High'][i] >= take_profit :
        sell = take_profit * ( 1 - fee_sell)
        df['sell'][i] = sell
        df['profit'][i] = (sell - buy)/buy
        buy=0
        
        
    
      df['cumulative_profit'][i] = df['profit'][:i].sum()    
      
      
      

          
      local_min = sd['Close'].min()
      

    
    return df





wyniki = pd.DataFrame(columns = ['Company', 'Long', 'Short'])

for c in company:

    df_long = download_df_long(c)
    df_short = short_df(df_long)

    long = back_trade(df_long)
    
    
    profits_long = long.copy()
    profits_long = profits_long["profit"]
    profits_long.dropna(inplace = True)
    
    plt.title('Long_'+c)
    plt.suptitle(long['cumulative_profit'][len(long)-1])  
    plt.plot(long['cumulative_profit'], color = 'red') 
    plt.show()
    print(long['cumulative_profit'][len(long)-1])


    
    investment = 100
    
    balance_list = [0]

    reinvest = 0.33 

    account_balance = 100
    
    levar = 10   
    

    for profit in profits_long:
        
        lucre = ( profit* levar) * account_balance * reinvest
        
        account_balance = account_balance + lucre
        
        balance_list.append(account_balance)
    

    
    
        
    plt.title('Balance_long_'+c)
    plt.suptitle(balance_list[-1])  
    plt.plot(balance_list) 
    plt.show()
    
    
    
    
    short =back_trade(df_short)
    


    profits_short = short.copy()
    profits_short = profits_short["profit"]
    profits_short.dropna(inplace = True)

    
    plt.title('Short_'+c)
    plt.suptitle(short['cumulative_profit'][len(short)-1])   
    plt.plot(short['cumulative_profit'], color = 'red')     
    plt.show()
    print(short['cumulative_profit'][len(short)-1])
    



    
    balance_list_s = [0]

    reinvest_s = 0.33 

    account_balance_s = 100
    
    levar = 10   
    


    for profit in profits_short:
        
        lucre = ( profit* levar) * account_balance_s * reinvest
        
        account_balance_s = account_balance_s + lucre
        
        balance_list_s.append(account_balance_s)
    



    
        
    plt.title('Balance_short_'+c)
    plt.suptitle(balance_list_s[-1])  
    plt.plot(balance_list_s) 
    plt.show()
    
    
    wyniki = wyniki.append({'Company' : c, 'Long' : balance_list[-1], 'Short' : balance_list_s[-1]},
        ignore_index = True)
