# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 01:40:14 2023

@author: Krzychu
"""
from datetime import datetime
import numpy as np

import time

############## VARIABLES ###################

bot = input("Włączyć bota?")

last_current_time = np.nan


local_min = 0
amplitude = 0
buy = 0
take_profit = 1000000000
stop_loss = 0



position_size_in_dollars = 0
leverage = 0 


#################### FUNCTIONS ###################

def what_time():
    
    
    now = datetime.now()
    current_minute = now.strftime("%M")
    current_time = now.strftime("%m/%d/%Y, %H:%M")

    
    return current_minute, current_time



def check_market():
    
    return True


def market_buy():
    print("Buying")
    return 


def make_stop_loss():
    print("Placing stop loss order...")

    return


def make_take_profit():
    print("Placing take profit order...")

    return    





############## BOT ######################


while bot == "1":
    
    current_minute = what_time()[0]
    current_time = what_time()[1]
    
    
    if current_minute == "59":
        
        print(f"It's: {current_time}, bot is starting...")
        print('Checking market...')
        
        if check_market:
            print("Making orders....")
            
            market_buy()
        
            make_stop_loss()
            
            make_take_profit()
            
            
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        print("Time for short break")
        time.sleep(110)
        

    elif last_current_time!=current_minute:
        print(current_time)
        last_current_time = current_minute
    

    
    
    
    
    
    