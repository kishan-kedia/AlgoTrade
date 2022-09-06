# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:37:45 2021

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

def atr(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs(df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].ewm(com=n,min_periods=n).mean()
    return df['ATR']

def bollBnd(DF,n):
    "function to calculate Bollinger Band"
    df = DF.copy()
    df["MA"] = df['close'].rolling(n).mean()
    #df["MA"] = df['close'].ewm(span=n,min_periods=n).mean()
    df["BB_up"] = df["MA"] + 2*df['close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2*df['close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    return df

bband = {}
for ticker in nifty100:
    bband[ticker] = bollBnd(ohlc[ticker],20)
    
ohlc2 = {}
for ticker in nifty100:
    ohlc2[ticker] = bband[ticker].copy(deep=True)



for ticker in nifty100:
    # Identify chart patterns (e.g. two crows, three crows, three inside, engulging pattern etc.)
    ohlc2[ticker]["3LS"] = talib.CDL3LINESTRIKE(ohlc2[ticker]["open"],            #3 line strike
                                                 ohlc2[ticker]["high"],
                                                 ohlc2[ticker]["low"],
                                                 ohlc2[ticker]["close"])
    
    ohlc2[ticker]["3BC"] = talib.CDL3BLACKCROWS(ohlc2[ticker]["open"],            #3 black crows
                                                 ohlc2[ticker]["high"],
                                                 ohlc2[ticker]["low"],
                                                 ohlc2[ticker]["close"])
    
    ohlc2[ticker]["ES"] = talib.CDLEVENINGSTAR(ohlc2[ticker]["open"],             #evening star
                                                 ohlc2[ticker]["high"],
                                                 ohlc2[ticker]["low"],
                                                 ohlc2[ticker]["close"],
                                                 penetration=0)
    
    ohlc2[ticker]["TG"] = talib.CDLTASUKIGAP(ohlc2[ticker]["open"],               #tasuki gap
                                                 ohlc2[ticker]["high"],
                                                 ohlc2[ticker]["low"],
                                                 ohlc2[ticker]["close"])
    
    ohlc2[ticker]["HI"] = talib.CDLINVERTEDHAMMER(ohlc2[ticker]["open"],          #hammer inverted
                                                 ohlc2[ticker]["high"],
                                                 ohlc2[ticker]["low"],
                                                 ohlc2[ticker]["close"])
        
    ohlc2[ticker]["ML"] = talib.CDLMATCHINGLOW(ohlc2[ticker]["open"],             #matching low
                                                 ohlc2[ticker]["high"],
                                                 ohlc2[ticker]["low"],
                                                 ohlc2[ticker]["close"])
    
    
    ohlc2[ticker]["BR"] = talib.CDLBREAKAWAY(ohlc2[ticker]["open"],               #breakaway
                                                 ohlc2[ticker]["high"],
                                                 ohlc2[ticker]["low"],
                                                 ohlc2[ticker]["close"])
    

print("\n3 line strike bearish reversal")
for i in range(30,75):
    for ticker in nifty100:
        if ohlc2[ticker].iloc[-1*i]['3LS']>0:
            print(ticker," ",ohlc2[ticker].iloc[-1*i]['DateTime'])
            
print("\n3 line strike bullish reversal")
for i in range(30,75):
    for ticker in nifty100:
        if ohlc2[ticker].iloc[-1*i]['3LS']<0:
            print(ticker," ",ohlc2[ticker].iloc[-1*i]['DateTime'])
            
print("\n3 black crows bearish reversal")
for i in range(30,150):
    for ticker in nifty100:
        if ohlc2[ticker].iloc[-1*i]['3BC']<0:
            print(ticker," ",ohlc2[ticker].iloc[-1*i]['DateTime'])
    
print("\nEvening Star bearish reversal")
for i in range(30,75):
    for ticker in nifty100:
        if ohlc2[ticker].iloc[-1*i]['ES']<0:
            print(ticker," ",ohlc2[ticker].iloc[-1*i]['DateTime'])
            
print("\nupside tasuki gap bullish continuation")
for i in range(30,75):
    for ticker in nifty100:
        if ohlc2[ticker].iloc[-1*i]['TG']>0:
            print(ticker," ",ohlc2[ticker].iloc[-1*i]['DateTime'])

print("\nhammer inverted bearish continuation")
for i in range(30,75):
    for ticker in nifty100:
        if ohlc2[ticker].iloc[-1*i]['HI']>0:
            print(ticker," ",ohlc2[ticker].iloc[-1*i]['DateTime'])    
            
print("\nmatching low bearish continuation/bullish reversal")
for i in range(30,75):
    for ticker in nifty100:
        if ohlc2[ticker].iloc[-1*i]['ML']>0:
            print(ticker," ",ohlc2[ticker].iloc[-1*i]['DateTime'])


for day in reversed(range(45)):
    print("Day",45-day)
    for ticker in nifty100:
          for i in range(-75*(day+1),-75*day + 18):
              if ohlc2[ticker].loc[last_index+i+1,'Buy/Sell'] == 'Buy'
              buy_price = 

ohlc2['ABB-EQ'].iloc[-100]['Buy/Sell']

def slope(ohlc_df,n):
    "function to calculate the slope of regression line for n consecutive points on a plot"
    df = ohlc_df.iloc[-1*n:,:]
    y = ((df["open"] + df["close"])/2).values
    x = np.array(range(n)).reshape((-1,1))
    y_scaled = (y - y.min())/(y.max() - y.min())
    x_scaled = (x - x.min())/(x.max() - x.min())
    model = LinearRegression().fit(x_scaled,y_scaled)
    slp = np.rad2deg(np.arctan(model.coef_)[0])
    return slp

def trend(df[]):
    
    

def slope2(df,to,n):
    if to==0:
        df = df.iloc[-n:,:]
    else:
        df = df.iloc[to-n:to,:]
    y = ((df["open"] + df["close"])/2).values
    x = np.array(range(n)).reshape((-1,1))
    y_scaled = (y - y.min())/(y.max() - y.min() + 0.5)
    x_scaled = (x - x.min())/(x.max() - x.min() + 0.5)
    model = LinearRegression().fit(x_scaled,y_scaled)
    slp = np.rad2deg(np.arctan(model.coef_)[0])
    return slp

for ticker in nifty100:
    last_index = ohlc2[ticker].iloc[-1].name 
    ohlc2[ticker]["slope_7"] = 0

for ticker in nifty100:
    for i in range(0,4000):
        ohlc2[ticker].loc[last_index-i,"slope_7"] = slope2(ohlc2[ticker],-1*i,7)

for ticker in nifty100:
    ohlc2[ticker] = ohlc2[ticker].drop(columns=['slope_7','trend'],axis=1)

for ticker in nifty100:
    ohlc2[ticker]['trend'] = ohlc2[ticker]['slope_7'].apply(trend)

for ticker in nifty100:
    bband[ticker]['angle'] = talib.LINEARREG_ANGLE(ohlc2[ticker]["close"], timeperiod=14)


for ticker in nifty100:
    ohlc2[ticker]["Buy/Sell"] = ""

for ticker in nifty100:
    for i in range(3075,3089):
        ohlc2[ticker] = ohlc2[ticker].drop([i])

for ticker in nifty100:
    ohlc2[ticker] = ohlc2[ticker].reset_index()
    ohlc2[ticker] = ohlc2[ticker].drop(columns=['index'])


for ticker in nifty100:
    ohlc2[ticker]['colour'] = np.where(ohlc2[ticker]['close']>=ohlc2[ticker]['open'],'green','red')
    ohlc2[ticker]['colour'] = np.where(ohlc2[ticker]['close']==ohlc2[ticker]['open'],'doji',ohlc2[ticker]['colour'])

for ticker in nifty100:
    ohlc2[ticker]['candle'] = np.where(ohlc2[ticker]['colour']=='green',1,-1)
    ohlc2[ticker]['candle'] = np.where(ohlc2[ticker]['colour']=='doji',0,ohlc2[ticker]['candle'])

for ticker in nifty100:
    ohlc2[ticker]['cum_trend'] = ohlc2[ticker]['candle'].rolling(7).sum()

for ticker in nifty100:
    ohlc2[ticker]['trend'] = 'no trend'
    ohlc2[ticker]['trend'] = np.where((ohlc2[ticker]['cum_trend']>=2)&(ohlc2[ticker]['close']>ohlc2[ticker]['close'].shift(7))
                                      ,'uptrend',ohlc2[ticker]['trend'])
    ohlc2[ticker]['trend'] = np.where((ohlc2[ticker]['cum_trend']<=-2)&(ohlc2[ticker]['close']<ohlc2[ticker]['close'].shift(7))
                                      ,'downtrend',ohlc2[ticker]['trend'])
for ticker in nifty100:
    ohlc2[ticker]["roll_max_vol"] = ohlc2[ticker]["volume"].rolling(10).max()




a1 = 0
a2 = 0

n = 50
for day in reversed(range(n)):
    print("Day",n-day)
    
    for i in range(-75*(day+1),(-75*day)-9):    
        for ticker in nifty100:
            last_index = len(ohlc2[ticker])
            curr_index = last_index+i
            if (ohlc2[ticker].iloc[curr_index]['3LS']>0 and ohlc2[ticker].iloc[curr_index-4]['trend']=='uptrend'):           #bearish reversal 3 line strike
                if ohlc2[ticker].iloc[curr_index]['roll_max_vol']>1.5*ohlc2[ticker].iloc[curr_index-4]['roll_max_vol']:
                    print("3 line strike bearish reversal",ticker,ohlc2[ticker].iloc[curr_index]['DateTime'])
                    ohlc2[ticker].loc[curr_index,'Buy/Sell'] = 'Sell'
                    a1 += 1
                    
            if (ohlc2[ticker].iloc[curr_index]['3LS']<0 and ohlc2[ticker].iloc[curr_index-4]['trend']=='downtrend'):         #bullish reversal 3 line strike
                if ohlc2[ticker].iloc[curr_index]['roll_max_vol']>1.5*ohlc2[ticker].iloc[curr_index-4]['roll_max_vol']:
                    print("3 line strike bullish reversal",ticker,ohlc2[ticker].iloc[curr_index]['DateTime'])
                    ohlc2[ticker].loc[curr_index,'Buy/Sell'] = 'Buy'
                    a1 += 1
                    
            if (ohlc2[ticker].iloc[curr_index]['3BC']<0 and ohlc2[ticker].iloc[curr_index-3]['trend']=='uptrend'):           #bearish reversal 3 black crow
                if ohlc2[ticker].iloc[curr_index]['roll_max_vol']>1.5*ohlc2[ticker].iloc[curr_index-3]['roll_max_vol']:
                    print("3 black crow bearish reversal",ticker,ohlc2[ticker].iloc[curr_index]['DateTime'])
                    ohlc2[ticker].loc[curr_index,'Buy/Sell'] = 'Sell'
                    a1 += 1
                    
            if (ohlc2[ticker].iloc[curr_index]['ES']<0 and ohlc2[ticker].iloc[curr_index-3]['trend']=='uptrend'):            #bearish reversal evening star
                if ohlc2[ticker].iloc[curr_index]['roll_max_vol']>1.5*ohlc2[ticker].iloc[curr_index-3]['roll_max_vol']:
                    print("evening star bearish reversal",ticker,ohlc2[ticker].iloc[curr_index]['DateTime'])
                    ohlc2[ticker].loc[curr_index,'Buy/Sell'] = 'Sell'
                    a1 += 1
                    
            if (ohlc2[ticker].iloc[curr_index]['TG']>0 and ohlc2[ticker].iloc[curr_index-3]['trend']=='uptrend'):            #bullish continuation upside tasuki gap
                if ohlc2[ticker].iloc[curr_index]['roll_max_vol']>1.5*ohlc2[ticker].iloc[curr_index-3]['roll_max_vol']:
                    print("upside tasuki gap bullish continuation",ticker,ohlc2[ticker].iloc[curr_index]['DateTime'])
                    ohlc2[ticker].loc[curr_index,'Buy/Sell'] = 'Buy'
                    a1 += 1
                    
            if (ohlc2[ticker].iloc[curr_index]['HI']>0 and ohlc2[ticker].iloc[curr_index-2]['trend']=='downtrend'):          #bearish continuation hammer inverted
                if ohlc2[ticker].iloc[curr_index]['roll_max_vol']>1.5*ohlc2[ticker].iloc[curr_index-2]['roll_max_vol']:
                    print("hammer inverted bearish continuation",ticker,ohlc2[ticker].iloc[curr_index]['DateTime'])
                    ohlc2[ticker].loc[curr_index,'Buy/Sell'] = 'Sell'
                    a1 += 1
                    
            if (ohlc2[ticker].iloc[curr_index]['ML']>0 and ohlc2[ticker].iloc[curr_index-3]['trend']=='downtrend'):          #bearish continuation matching low
                if ohlc2[ticker].iloc[curr_index]['roll_max_vol']>1.5*ohlc2[ticker].iloc[curr_index-3]['roll_max_vol']:
                    print("matching low bearish continuation",ticker,ohlc2[ticker].iloc[curr_index]['DateTime'])
                    ohlc2[ticker].loc[curr_index,'Buy/Sell'] = 'Sell'
                    a1 += 1

for ticker in nifty100:
    ohlc2[ticker]['cum_red/green'] = 0
    ohlc2[ticker]['cum_red/green'] = np.where((ohlc2[ticker]['colour']=='green'),1,ohlc2[ticker]['cum_red/green'])
    ohlc2[ticker]['cum_red/green'] = np.where(((ohlc2[ticker]['colour']=='green')&(ohlc2[ticker]['colour'].shift(1)=='green')),(ohlc2[ticker]['cum_red/green'].shift(1))+1,ohlc2[ticker]['cum_red/green'])
    ohlc2[ticker]['cum_red/green'] = np.where((ohlc2[ticker]['colour']=='red'),-1,ohlc2[ticker]['cum_red/green'])
    ohlc2[ticker]['cum_red/green'] = np.where(((ohlc2[ticker]['colour']=='red')&(ohlc2[ticker]['colour'].shift(1)=='red')),(ohlc2[ticker]['cum_red/green'].shift(1))-1,ohlc2[ticker]['cum_red/green'])

for ticker in nifty100:
    ohlc2[ticker]['cum_red/green'] = 0
    ohlc2[ticker]['cum_red/green'] = np.where((ohlc2[ticker]['colour']=='green'),1,ohlc2[ticker]['cum_red/green'])
    ohlc2[ticker]['cum_red/green'] = np.where(((ohlc2[ticker]['colour']=='green')&(ohlc2[ticker]['colour'].shift(1)=='green')),(ohlc2[ticker]['cum_red/green'].shift(1))+1,ohlc2[ticker]['cum_red/green'])
    ohlc2[ticker]['cum_red/green'] = np.where((ohlc2[ticker]['colour']=='red'),-1,ohlc2[ticker]['cum_red/green'])
    ohlc2[ticker]['cum_red/green'] = np.where(((ohlc2[ticker]['colour']=='red')&(ohlc2[ticker]['colour'].shift(1)=='red')),(ohlc2[ticker]['cum_red/green'].shift(1))-1,ohlc2[ticker]['cum_red/green'])


for ticker in nifty100:
    ohlc2[ticker]['exit'] = ''

#backtest


days = [i+1 for i in range(50)]
stocks = [i for i in nifty100]
stock_ret = pd.DataFrame(columns=stocks,index=days)
status = ''
init_price = 0
final_price = 0
capital = 10000
qty = 0


###########################################################################################
a2 = 0
n = 50
for day in reversed(range(n)):
    print("\nDay",n-day)
    for ticker in nifty100:
        last_index = len(ohlc2[ticker])
        for i in range(-75*(day+1),((-75*day)-5)):
            curr_index = last_index + i
            if ((ohlc2[ticker].iloc[curr_index]['Buy/Sell'] == 'Buy') & (status =='')):
                status = 'buy'
                init_price = (ohlc2[ticker].iloc[(curr_index+1)]['open']+ohlc2[ticker].iloc[(curr_index+1)]['high'])/2
                qty = math.floor((capital)/init_price)
                print(ticker)
                a2 += 1
            elif ((ohlc2[ticker].iloc[curr_index]['Buy/Sell'] == 'Sell') & (status =='')):
                status = 'sell'
                init_price = (ohlc2[ticker].i5loc[(curr_index+1)]['open']+ohlc2[ticker].iloc[(curr_index+1)]['low'])/2
                qty = math.floor((capital)/init_price)
                print(ticker)
                a2 += 1
            elif ((status=='buy') & (ohlc2[ticker].iloc[curr_index]['cum_red/green']==-2) & (ohlc2[ticker].iloc[curr_index-1]['cum_red/green']==-2)):
                status = ''
                final_price = (ohlc2[ticker].iloc[(curr_index+1)]['open']+ohlc2[ticker].iloc[(curr_index+1)]['low'])/2
                stock_ret[n-day][ticker] = (final_price-init_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='sell') & (ohlc2[ticker].iloc[curr_index]['cum_red/green']==2) & (ohlc2[ticker].iloc[(curr_index-1)]['cum_red/green']==2)):
                status = ''
                final_price = (ohlc2[ticker].iloc[(curr_index+1)]['open']+ohlc2[ticker].iloc[(curr_index+1)]['high'])/2
                stock_ret[n-day][ticker] = (init_price-final_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='buy') & (i==((-75*day)-5)-1)):
                status = ''
                final_price = (ohlc2[ticker].iloc[(curr_index+1)]['open']+ohlc2[ticker].iloc[(curr_index+1)]['low'])/2
                stock_ret[n-day][ticker] = (final_price-init_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='sell') & (i==((-75*day)-5)-1)):
                status = ''
                final_price = (ohlc2[ticker].iloc[(curr_index+1)]['open']+ohlc2[ticker].iloc[(curr_index+1)]['high'])/2
                stock_ret[n-day][ticker] = (init_price-final_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)

a2 = 0
n = 50
for day in reversed(range(n)):
    print("\nDay",n-day)
    for ticker in nifty100:
        last_index = len(ohlc2[ticker])
        for i in range(-75*(day+1),((-75*day)-5)):
            curr_index = last_index + i
            if ((ohlc2[ticker].iloc[curr_index]['Buy/Sell'] == 'Buy') & (status =='')):
                status = 'buy'
                init_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                qty = math.floor((capital)/init_price)
                print(ticker)
                a2 += 1
            elif ((ohlc2[ticker].iloc[curr_index]['Buy/Sell'] == 'Sell') & (status =='')):
                status = 'sell'
                init_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                qty = math.floor((capital)/init_price)
                print(ticker)
                a2 += 1
            elif ((status=='buy') & (ohlc2[ticker].iloc[curr_index]['cum_red/green']==-2)):
                status = ''
                final_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                stock_ret[ticker][n-day] = (final_price-init_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='sell') & (ohlc2[ticker].iloc[curr_index]['cum_red/green']==2)):
                status = ''
                final_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                stock_ret[ticker][n-day] = (init_price-final_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='buy') & (i==((-75*day)-5)-1)):
                status = ''
                final_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                stock_ret[ticker][n-day] = (final_price-init_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='sell') & (i==((-75*day)-5)-1)):
                status = ''
                final_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                stock_ret[ticker][n-day] = (init_price-final_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)




###################################################################################################

day_open = pd.DataFrame(columns=['prev_close','prev_high','prev_low','prev_vol','open','high','low','close','volume'],
                        index = stocks)
day_open_all = {}
for day in days:
    day_open_all[day] = day_open


    


df = ohlc_3min2['ABB-EQ']
l = len(df)
for i in range(22):
    df = df.drop(l-2397+i)

for ticker in nifty100:
    l = len(ohlc_3min2[ticker])
    for i in range(22):
        ohlc_3min2[ticker] = ohlc_3min2[ticker].drop(l-2397+i)
#ohlc2_3min2.remove('PGHH-EQ')



for ticker in nifty100:
    ohlc_3min2[ticker] = ohlc_3min2[ticker].reset_index()
    ohlc_3min2[ticker] = ohlc_3min2[ticker].drop(columns=['index'])
 
for ticker in nifty100:
    ohlc_3min2[ticker] = bollBnd(ohlc_3min2[ticker],20)

for ticker in nifty100:
    ohlc_3min2[ticker]['Buy/Sell'] = ''

def bollBnd(DF,n):
    "function to calculate Bollinger Band"
    df = DF.copy()
    df["MA"] = df['close'].rolling(n).mean()
    #df["MA"] = df['close'].ewm(span=n,min_periods=n).mean()
    df["BB_up"] = df["MA"] + 2*df['close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2*df['close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    return df


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
        ohlc_3min2[ticker].loc[(last_index-i),'slope'] = slope3(ohlc_3min2[ticker],(last_index-i),20)


days = [i+1 for i in range(30)]
stocks = [i for i in nifty100]
stock_ret = pd.DataFrame(columns=stocks,index=days)
status = ''
init_price = 0
final_price = 0
capital = 20000
qty = 0

df_gap_up_slope = pd.DataFrame(columns=['Stock','DateTime','prev_day_slope','morning_slope','slope_diff','return','profit',
                                        'target1','target2','init_price','day_high','day_low','morning_candle'])
df_gap_down_slope = pd.DataFrame(columns=['Stock','DateTime','prev_day_slope','morning_slope','slope_diff','return','profit',
                                          'target1','target2','init_price','day_high','day_low','morning_candle'])


a3 = 0
n = 20
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
            end_rally = 30
            slope_prev = df_3min.loc[(morning-1),'slope']
            for i in range(morning+1,(morning+end_rally)):
                if((status == '') & (df_3min.loc[i,'colour']=='red')):
                    if(df_3min.loc[i,'MA']<df_3min.loc[i,'low']):
                        status = 'sell'
                        gap = 'up'
                        b = i
                        a3 += 1
                        #df_3min.loc[i+1,'Buy/Sell'] = 'sell'
                        init_price = df_3min.loc[i+1,'open']
                        lowest = init_price
                        target_price = init_price - ((init_price*target)/100)
                        stop_loss = ((init_price*stop_loss_percent)/100) + init_price
                        print(init_price)
                        slope_call = df_3min.loc[i,'slope']
                        
                    else:
                        status = ''
                        gap = ''
                        print('False Signal')
                        break
                
                if(status == 'sell'):
                    bb_signal = ''
                    bb_up = df_3min.loc[i,'BB_up']
                    bb_down = df_3min.loc[i,'BB_dn']
                    bb_width = df_3min.loc[i,'BB_width']*0.1
                    
                    if((df_3min.loc[i,'high']>(bb_up-bb_width))&((i-b)>4)):
                        final_price = df_3min.loc[i+1,'open']
                        df_3min[i+1,'Buy/Sell'] = 'exit'
                        print(final_price,'bb_up')
                        break
                    
                    if((df_3min.loc[i,'low']<(bb_down+bb_width))&((i-b)>1)):
                        final_price = df_3min.loc[i+1,'open']
                        df_3min[i+1,'Buy/Sell'] = 'exit'
                        print(final_price,'bb_dn')
                        break
                    
                    if(df_3min.loc[i,'low']<target_price):
                        status = ''
                        final_price = target_price
                        df_3min.loc[i,'Buy/Sell'] = 'exit'
                        print(final_price,'target reached')
                        break
                    
                    elif(df_3min.loc[i,'high']>stop_loss):
                        status = ''
                        final_price = stop_loss
                        df_3min.loc[i,'Buy/Sell'] = 'exit'
                        print(final_price,'stop loss reached')
                        break
                    
                    elif(df_3min.loc[i,'close']<lowest):
                        lowest = df_3min.loc[i,'close']
                        stop_loss = ((lowest*stop_loss_percent)/100) + lowest
                    
                    
                    elif(i==(morning+end_rally-1)):
                        status = ''
                        final_price = df_3min.loc[i+1,'open']
                        df_3min.loc[i,'Buy/Sell'] = 'exit'
                        print(final_price,'end of rally')
                        break
                    
        #Gap - down
        if((df_3min.loc[morning,'high']<prev_day_low)&(prev_range>1)):
            print("\nGap Down -> ",ticker,"-",target," ",df_3min.loc[morning,'DateTime']," ",df_day.loc[day_index,'DateTime'])
            end_rally = 30
            slope_prev = df_3min.loc[(morning-1),'slope']
            for i in range(morning+1,morning+end_rally):
                if((status == '') & (df_3min.loc[i,'colour']=='green')):
                    if(df_3min.loc[i,'MA']>df_3min.loc[i,'high']):
                        status = 'buy'
                        gap = 'down'
                        b = i
                        a3 += 1
                        #df_3min.loc[i+1,'Buy/Sell'] = 'buy'
                        init_price = df_3min.loc[i+1,'open']
                        highest = init_price
                        target_price = init_price + ((init_price*target)/100)
                        stop_loss = init_price - ((init_price*stop_loss_percent)/100)
                        print(init_price)
                        slope_call = df_3min.loc[i,'slope']
                    else:
                        status = ''
                        gap = ''
                        print('False Signal')
                        break
                    
                if(status == 'buy'):
                    bb_signal = ''
                    bb_up = df_3min.loc[i,'BB_up']
                    bb_down = df_3min.loc[i,'BB_dn']
                    bb_width = df_3min.loc[i,'BB_width']*0.1
                    
                    if((df_3min.loc[i,'high']>(bb_up-bb_width))&((i-b)>1)):
                        final_price = df_3min.loc[i+1,'open']
                        df_3min[i+1,'Buy/Sell'] = 'exit'
                        print(final_price,'bb_up')
                        break
                    
                    if((df_3min.loc[i,'low']<(bb_down+bb_width))&(i-b)>4):
                        final_price = df_3min.loc[i+1,'open']
                        df_3min[i+1,'Buy/Sell'] = 'exit'
                        print(final_price,'bb_up')
                        break
                    
                    if(df_3min.loc[i,'high']>target_price):
                        status = ''
                        final_price = target_price
                        print(final_price,'target reached')
                        df_3min.loc[i,'Buy/Sell'] = 'exit'
                        break
                    
                    elif(df_3min.loc[i,'low']<stop_loss):
                        status = ''
                        final_price = stop_loss
                        df_3min.loc[i,'Buy/Sell'] = 'exit'
                        print(final_price,'stop loss reached')
                        break
                    
                    elif(df_3min.loc[i,'close']>highest):
                        highest = df_3min.loc[i,'close']
                        stop_loss = highest - ((highest*stop_loss_percent)/100)
                         
                    elif(i==(morning+end_rally-1)):
                        status = ''
                        final_price = df_3min.loc[i+1,'open']
                        df_3min.loc[i,'Buy/Sell'] = 'exit'
                        print(final_price,'end of rally')
                        break
        
        if(gap=='up'):
            qty = math.floor(capital/init_price)
            dif = round((init_price-final_price),1)
            brokerage = capital*0.001
            profit = round((dif*qty)-brokerage,1) 
            diff = round((((dif)/(init_price))*100),2)
            gap = ''
            stock_ret[ticker][n-day] = profit
            print("return ->",diff,"% ","Rs:",profit)
            slope_diff = slope_call - slope_prev
            temp = {'Stock':ticker,'DateTime':df_day.loc[(day_index+1),'DateTime'],'prev_day_slope':slope_prev,'morning_slope':slope_call,'slope_diff':slope_diff,'return':diff,'profit':profit,'target1':target,'target2':target2_up,'init_price':init_price,'day_high':day_high,'day_low':day_low,'morning_candle':df_3min.loc[morning,'colour']}
            df_gap_up_slope = df_gap_up_slope.append(temp,ignore_index=True)
            
        elif(gap=='down'):
            qty = math.floor(capital/init_price)
            dif = round((final_price-init_price),1)
            diff = round(((dif)/(final_price))*100,2)
            gap = ''
            brokerage = capital*0.001
            profit = round((dif*qty)-brokerage,1) 
            stock_ret[ticker][n-day] = profit
            print("return ->",diff,"% ","Rs:",profit)
            slope_diff = slope_call - slope_prev
            temp = {'Stock':ticker,'DateTime':df_day.loc[(day_index+1),'DateTime'],'prev_day_slope':slope_prev,'morning_slope':slope_call,'slope_diff':slope_diff,'return':diff,'profit':profit,'target1':target,'target2':target2_down,'init_price':init_price,'day_high':day_high,'day_low':day_low,'morning_candle':df_3min.loc[morning,'colour']}
            df_gap_down_slope = df_gap_down_slope.append(temp,ignore_index=True)


Total = 0
stock_ret['total'] = 0
stock_ret['total'] = stock_ret.sum(axis=1)
Total = round(stock_ret['total'].sum())


total_gap_down = 0
total_up_gap = 0
total_up_gap = round(df_gap_up_slope['profit'].sum())
total_gap_down = round(df_gap_down_slope['profit'].sum())





gap_down_nov = df_gap_down_slope.copy(deep=True)
gap_up_nov = df_gap_up_slope.copy(deep=True)
total_gap_down = round(gap_down_oct['profit'].sum())

gap_down_oct = df_gap_down_slope.copy(deep=True)
gap_up_oct = df_gap_up_slope.copy(deep=True)

gap_down_sept = df_gap_down_slope.copy(deep=True)
gap_up_sept = df_gap_up_slope.copy(deep=True)

gap_down_aug = df_gap_down_slope.copy(deep=True)
gap_up_aug = df_gap_up_slope.copy(deep=True)

data_to_excel = pd.ExcelWriter("returns3.xlsx")
with data_to_excel as writer:
    gap_up_nov.to_excel(data_to_excel,sheet_name='up_nov')
    gap_up_oct.to_excel(data_to_excel,sheet_name='up_oct')
    gap_up_sept.to_excel(data_to_excel,sheet_name='up_sept')
    gap_up_aug.to_excel(data_to_excel,sheet_name='up_aug')
    gap_down_nov.to_excel(data_to_excel,sheet_name='down_nov')
    gap_down_oct.to_excel(data_to_excel,sheet_name='down_oct')
    gap_down_sept.to_excel(data_to_excel,sheet_name='down_sept')
    gap_down_aug.to_excel(data_to_excel,sheet_name='down_aug')


stock_ret.count().sum()

stock_ret['average'] = 0
stock_ret['average'] = stock_ret.mean(axis=1)

stock_ret2 = stock_ret.copy(deep=True)



df = ohlc_3min2['ABB-EQ'].copy(deep=True)



for i in range(len(df)):
    if i < 41:
        continue
    else:
        df.loc[i,'slope'] = slope3(df,i,20)

for ticker in nifty100:
    df_3min = ohlc_3min2[ticker]
    for i in range(len(df_3min)):
        if i<50:
            continue
        else:
            df_3min.loc[i,'slope'] = slope3(df_3min,i,5)



a2 = 0
n = 15
for day in reversed(range(n)):
    print("\nDay",n-day)
    for ticker in nifty100:
        last_index = len(ohlc2[ticker])
        for i in range(-125*(day+1),((-125*day)-5)):
            curr_index = last_index + i
            if ((ohlc2[ticker].iloc[curr_index]['Buy/Sell'] == 'Buy') & (status =='')):
                status = 'buy'
                init_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                qty = math.floor((capital)/init_price)
                print(ticker)
                a2 += 1
            elif ((ohlc2[ticker].iloc[curr_index]['Buy/Sell'] == 'Sell') & (status =='')):
                status = 'sell'
                init_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                qty = math.floor((capital)/init_price)
                print(ticker)
                a2 += 1
            elif ((status=='buy') & (ohlc2[ticker].iloc[curr_index]['cum_red/green']==-2)):
                status = ''
                final_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                stock_ret[ticker][n-day] = (final_price-init_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='sell') & (ohlc2[ticker].iloc[curr_index]['cum_red/green']==2)):
                status = ''
                final_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                stock_ret[ticker][n-day] = (init_price-final_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='buy') & (i==((-75*day)-5)-1)):
                status = ''
                final_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                stock_ret[ticker][n-day] = (final_price-init_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)
            elif ((status=='sell') & (i==((-75*day)-5)-1)):
                status = ''
                final_price = ohlc2[ticker].iloc[(curr_index+1)]['open']
                stock_ret[ticker][n-day] = (init_price-final_price)*qty - 50
                ohlc2[ticker].loc[curr_index,'exit'] = 'exit'
                print(ticker)

                   
 n = 15
for day in reversed(range(1,n)):
    print("\nDay",n-day)
    for ticker in nifty100:
        last_index = len(ohlc_3min2[ticker])
        morning = -125*(day) + last_index
        day_index = len(ohlc_day2[ticker]) - day -1
        #print(ohlc_3min2[ticker].loc[morning,'open'])    ----- next day 5 minute candle
        #print(ohlc_day2[ticker].loc[66-day,'open']) ----- previous day values
        
        prev_day_high = ohlc_day2[ticker].loc[day_index,'high']
        prev_day_low = ohlc_day2[ticker].loc[day_index,'low']
        prev_range = ((prev_day_high-prev_day_low)/(prev_day_high))*100
        morning_low = ohlc_3min2[ticker].loc[morning,'low']
        morning_high = ohlc_3min2[ticker].loc[morning,'high']
        target = round(prev_range*0.8,1)
        #Gap - up
        if((morning_low>prev_day_high)&(prev_range>=1.5)):
            target = ohlc_3min2[ticker].loc[morning,'open'] - ohlc_day2[ticker].loc[day_index,'close']
            target = round((target/morning_low)*100,1)
            if target>1:
                print("Gap Up -> ",ticker,"-",target," ",ohlc_3min2[ticker].loc[morning,'DateTime'])
        #Gap - down
        if((morning_high<prev_day_low)&(prev_range>1.5)):
            target = ohlc_day2[ticker].loc[day_index,'close'] - ohlc_3min2[ticker].loc[morning,'open'] 
            target = round((target/morning_high)*100,1)
            if target>1:
                print("Gap Down -> ",ticker,"-",target," ",ohlc_3min2[ticker].loc[morning,'DateTime'])
                
            


