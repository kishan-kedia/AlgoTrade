# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 21:39:07 2022

@author: Firos
"""

from smartapi import SmartConnect 
import pandas as pd
import os
import requests
from datetime import datetime as dt
from datetime import timedelta
import numpy as np
import time
import talib
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from statsmodels.regression.rolling import RollingOLS
import math

for ticker in nifty100:
    ohlc_3min2[ticker] = ohlc_3min2[ticker].reset_index()
    ohlc_3min2[ticker] = ohlc_3min2[ticker].drop(columns=['index'])

for ticker in nifty100:
    ohlc_3min2[ticker]['Buy/Sell'] = ''


for ticker in nifty100:
    ohlc_3min2[ticker]['colour'] = np.where(ohlc_3min2[ticker]['close']>=ohlc_3min2[ticker]['open'],'green','red')
    ohlc_3min2[ticker]['colour'] = np.where(ohlc_3min2[ticker]['close']==ohlc_3min2[ticker]['open'],'doji',ohlc_3min2[ticker]['colour'])

def slope3(df,n,r):  
    if((n-r)<r):
        return 'NaN'
    df = df.iloc[n-r:n,:]
    y = df['close'].values
    x = np.array(range(r)).reshape((-1,1))
    cons_y = 0.5/(y.max())
    cons_x = 0.5/(x.max())
    y_scaled = (y - y.min())/(y.max() - y.min() + 0.05)
    x_scaled = (x - x.min())/(x.max() - x.min() + 0.05)
    model = LinearRegression().fit(x_scaled,y_scaled)
    slp = np.rad2deg(np.arctan(model.coef_)[0])
    return slp


for ticker in nifty100:
    last_index = len(ohlc_3min2[ticker])
    for i in reversed(range(1,last_index-40)):
        ohlc_3min2[ticker].loc[(last_index-i),'slope'] = slope3(ohlc_3min2[ticker],(last_index-i),10)


days = [i+1 for i in range(30)]
stocks = [i for i in nifty100]
stock_ret = pd.DataFrame(columns=stocks,index=days)
status = ''
init_price = 0
final_price = 0
capital = 20000
qty = 0

#df_gap_up_slope = pd.DataFrame(columns=['Stock','DateTime','prev_day_slope','morning_slope','slope_diff','return','profit',
#                                        'target1','target2','init_price','day_high','day_low','morning_candle'])
#df_gap_down_slope = pd.DataFrame(columns=['Stock','DateTime','prev_day_slope','morning_slope','slope_diff','return','profit',
#                                          'target1','target2','init_price','day_high','day_low','morning_candle'])


df_gap_up_slope = pd.DataFrame(columns=['Stock','DateTime','prev_day_slope','morning_slope','slope_diff',
                                        'target1','target2','init_price','day_high','day_low','morning_candle'])
df_gap_down_slope = pd.DataFrame(columns=['Stock','DateTime','prev_day_slope','morning_slope','slope_diff',
                                          'target1','target2','init_price','day_high','day_low','morning_candle'])



day = 0

a3 = 0
n = 19
for day in reversed(range(1,n)):
    print("\nDay",n-day)
    for ticker in nifty100:
        init_price = 0
        final_price = 0
        status = ''
        lowest = 0
        highest = 0
        gap = ''
        if ticker=='PGHH-EQ':
            continue
        #if ticker=='TATAMOTORS-EQ':
         #   continue
        df_day = ohlc_day2[ticker]
        df_3min = ohlc_3min2[ticker]
        last_index = len(df_3min)
        morning = -125*day + last_index
        day_index = len(df_day) - day - 1
        #print(ohlc_3min2[ticker].loc[morning,'open'])    ----- next day 5 minute candle
        #print(ohlc_day2[ticker].loc[66-day,'open']) ----- previous day values
        
        prev_day_high = df_day.loc[day_index,'high']
        prev_day_low = df_day.loc[day_index,'low']
        prev_day_close = df_day.loc[day_index,'close']
        day_high = df_day.loc[(day_index+1),'high']
        day_low = df_day.loc[(day_index+1),'low']
        day_open = df_day.loc[(day_index+1),'open']
        day_close =  df_day.loc[(day_index+1),'close']
        prev_range = ((prev_day_high-prev_day_low)/(prev_day_high))*100
        target = round(prev_range*0.8,1)
        stop_loss_percent = target/2
        target2_down = ((prev_day_close - day_open)/(day_open))*100
        target2_up = ((day_open - prev_day_close)/(day_open))*100   
        #Gap - up
        if((df_3min.loc[morning,'low']>prev_day_high)&(prev_range>=1)):
            print("\nGap Up -> ",ticker,"-",target," ",df_3min.loc[morning,'DateTime']," ",df_day.loc[day_index,'DateTime'])
            end_rally = 110
            slope_prev = df_3min.loc[(morning-1),'slope']
            init_price = df_3min.loc[morning+1,'open']
            lowest = init_price
            highest =init_price
            gap = 'up'  
            slope_call = df_3min.loc[i,'slope']
            print(init_price)
            for i in range(morning+1,(morning+end_rally)):
                b = i
                a3 += 1
                #df_3min.loc[i+1,'Buy/Sell'] = 'sell'
                lowest = min(lowest,df_3min.loc[i,'low'])
                highest = max(highest,df_3min.loc[i,'high'])
                
                
                    
        #Gap - down
        if((df_3min.loc[morning,'high']<prev_day_low)&(prev_range>1)):
            print("\nGap Down -> ",ticker,"-",target," ",df_3min.loc[morning,'DateTime']," ",df_day.loc[day_index,'DateTime'])
            end_rally = 110
            slope_prev = df_3min.loc[(morning-1),'slope']
            init_price = df_3min.loc[morning+1,'open']
            lowest = init_price
            highest =init_price
            gap = 'down'  
            slope_call = df_3min.loc[i,'slope']
            print(init_price)
            for i in range(morning+1,morning+end_rally):
                status = 'buy'
                gap = 'down'
                b = i
                a3 += 1
                #df_3min.loc[i+1,'Buy/Sell'] = 'buy'
                lowest = min(lowest,df_3min.loc[i,'low'])
                highest = max(highest,df_3min.loc[i,'high'])
                
        
        if(gap=='up'):
            qty = math.floor(capital/init_price)
            #dif = round((init_price-final_price),1)
            #brokerage = capital*0.001
            #profit = round((dif*qty)-brokerage,1) 
            #diff = round((((dif)/(init_price))*100),2)
            gap = ''
            #stock_ret[ticker][n-day] = profit
            #print("return ->",diff,"% ","Rs:",profit)
            slope_diff = slope_call - slope_prev
            temp = {'Stock':ticker,'DateTime':df_3min.loc[(morning),'DateTime'],'prev_day_slope':slope_prev,'morning_slope':slope_call,'slope_diff':slope_diff,'target1':target,'target2':target2_up,'init_price':init_price,'day_high':highest,'day_low':lowest,'morning_candle':df_3min.loc[morning,'colour']}
            df_gap_up_slope = df_gap_up_slope.append(temp,ignore_index=True)
            
        elif(gap=='down'):
            qty = math.floor(capital/init_price)
            #dif = round((final_price-init_price),1)
            #diff = round(((dif)/(final_price))*100,2)
            gap = ''
            #brokerage = capital*0.001
            #profit = round((dif*qty)-brokerage,1) 
            #stock_ret[ticker][n-day] = profit
            #print("return ->",diff,"% ","Rs:",profit)
            slope_diff = slope_call - slope_prev
            temp = {'Stock':ticker,'DateTime':df_3min.loc[(morning),'DateTime'],'prev_day_slope':slope_prev,'morning_slope':slope_call,'slope_diff':slope_diff,'target1':target,'target2':target2_down,'init_price':init_price,'day_high':highest,'day_low':lowest,'morning_candle':df_3min.loc[morning,'colour']}
            df_gap_down_slope = df_gap_down_slope.append(temp,ignore_index=True)


gap_down_1 = df_gap_down_slope.copy(deep=True)
gap_up_1 = df_gap_up_slope.copy(deep=True)


gap_down_2 = df_gap_down_slope.copy(deep=True)
gap_up_2 = df_gap_up_slope.copy(deep=True)

gap_down_3 = df_gap_down_slope.copy(deep=True)
gap_up_3 = df_gap_up_slope.copy(deep=True)

gap_down_4 = df_gap_down_slope.copy(deep=True)
gap_up_4 = df_gap_up_slope.copy(deep=True)

df = gap_down_4.copy(deep=True)
# Check which columns have timezones datetime64[ns, UTC] 
df.dtypes

# Remove timezone from columns

gap_down_1['DateTime'] = gap_down_1['DateTime'].dt.tz_localize(None)
gap_up_1['DateTime'] = gap_up_1['DateTime'].dt.tz_localize(None)
gap_down_2['DateTime'] = gap_down_2['DateTime'].dt.tz_localize(None)
gap_up_2['DateTime'] = gap_up_2['DateTime'].dt.tz_localize(None)
gap_down_3['DateTime'] = gap_down_3['DateTime'].dt.tz_localize(None)
gap_up_3['DateTime'] = gap_up_3['DateTime'].dt.tz_localize(None)
gap_down_4['DateTime'] = gap_down_4['DateTime'].dt.tz_localize(None)
gap_up_4['DateTime'] = gap_up_4['DateTime'].dt.tz_localize(None)


data_to_excel = pd.ExcelWriter("returns4.xlsx")
with data_to_excel as writer:
    gap_up_1.to_excel(data_to_excel,sheet_name='up_1')
    gap_up_2.to_excel(data_to_excel,sheet_name='up_2')
    gap_up_3.to_excel(data_to_excel,sheet_name='up_3')
    gap_up_4.to_excel(data_to_excel,sheet_name='up_4')
    gap_down_1.to_excel(data_to_excel,sheet_name='down_1')
    gap_down_2.to_excel(data_to_excel,sheet_name='down_2')
    gap_down_3.to_excel(data_to_excel,sheet_name='down_3')
    gap_down_4.to_excel(data_to_excel,sheet_name='down_4')
