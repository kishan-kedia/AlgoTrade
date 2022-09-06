# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 09:19:22 2021

@author: Firos
"""

# package import statement
from smartapi import SmartConnect 
import pandas as pd
import os
import requests
from datetime import datetime as dt
from datetime import timedelta
import numpy as np
import time
#or from smartapi.smartConnect import SmartConnect
#import smartapi.smartExceptions(for smartExceptions)

cwd = os.chdir("C:\\Algotrade")

#create object of call
key = open("api_key.txt",'r').read()
user_ID = open("Client_ID.txt",'r').read()
pswd = open("Password.txt",'r').read()
obj=SmartConnect(api_key=key)
                #optional
                #access_token = "your access token",
                #refresh_token = "your refresh_token")

#login api call

data = obj.generateSession(user_ID,pswd)
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()

#fetch User Profile
userProfile= obj.getProfile(refreshToken)
del key
del user_ID
del pswd

def fetchOHLC(symbol,token,interval,fromdate,todate):
    try:
        historicParam={
            "exchange": 'NSE',
            "tradingsymbol":symbol,
            "symboltoken": token,
            "interval": interval,
            "fromdate": fromdate, 
            "todate": todate
            }
        
        his = obj.getCandleData(historicParam)
        historic = pd.DataFrame(his['data'])
        historic = historic.rename(columns = {0:'DateTime',1:'open',2:'high',3:'low',4:'close',5:'volume'})
        historic['DateTime'] = pd.to_datetime(historic['DateTime'])
        return historic
    except Exception as e:
        print("Historic Api failed: {}".format(e))   


nifty100 = ['ABB-EQ','ABCAPITAL-EQ','ACC-EQ','ADANIPORTS-EQ','AMBUJACEM-EQ','ASHOKLEY-EQ','ASIANPAINT-EQ','AUROPHARMA-EQ','AXISBANK-EQ','BAJAJ-AUTO-EQ',
            'BAJFINANCE-EQ','BAJAJFINSV-EQ','BANKBARODA-EQ','BEL-EQ','BHEL-EQ','BPCL-EQ','BHARTIARTL-EQ','INDUSTOWER-EQ','BOSCHLTD-EQ','BRITANNIA-EQ','CADILAHC-EQ',
            'CIPLA-EQ','COALINDIA-EQ','COLPAL-EQ','CONCOR-EQ','CUMMINSIND-EQ','DLF-EQ','DABUR-EQ','DRREDDY-EQ','EICHERMOT-EQ','EMAMILTD-EQ','GAIL-EQ','GICRE-EQ',
            'GRASIM-EQ','GODREJCP-EQ','HCLTECH-EQ','HDFCBANK-EQ','HAVELLS-EQ','HEROMOTOCO-EQ','HINDALCO-EQ','HINDPETRO-EQ','HINDUNILVR-EQ','HINDZINC-EQ',
            'HDFC-EQ','ITC-EQ','ICICIBANK-EQ','ICICIPRULI-EQ','IDEA-EQ','IBULHSGFIN-EQ','IOC-EQ','INDUSINDBK-EQ','INFY-EQ','INDIGO-EQ','JSWSTEEL-EQ',
            'KOTAKBANK-EQ','LICHSGFIN-EQ','LT-EQ','L&TFH-EQ','LUPIN-EQ','M&M-EQ','MARICO-EQ','MARUTI-EQ','MOTHERSUMI-EQ','NHPC-EQ','NMDC-EQ','NTPC-EQ',
            'ONGC-EQ','OIL-EQ','OFSS-EQ','PETRONET-EQ','PIDILITIND-EQ','PEL-EQ','PFC-EQ','POWERGRID-EQ','PGHH-EQ','PNB-EQ','RELIANCE-EQ','RECLTD-EQ',
            'SHREECEM-EQ','SRTRANSFIN-EQ','SIEMENS-EQ','SBIN-EQ','SAIL-EQ','SUNPHARMA-EQ','SUNTV-EQ','TCS-EQ','TATAMTRDVR-EQ','TATAMOTORS-EQ','TATAPOWER-EQ',
            'TATASTEEL-EQ','TECHM-EQ','TITAN-EQ','UPL-EQ','ULTRACEMCO-EQ','UBL-EQ','MCDOWELL-N-EQ','VEDL-EQ','WIPRO-EQ','YESBANK-EQ','ZEEL-EQ']

url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
sym_tok = requests.get(url).json()
tokendf = pd.DataFrame.from_dict(sym_tok)

tokendf = tokendf[tokendf['exch_seg']=='NSE']
tokendf = tokendf[tokendf['lotsize'] == '1']
tokendf = tokendf.set_index('symbol')
tokendf = tokendf.loc[nifty100]
tokendf = tokendf.drop(columns=['expiry','instrumenttype','strike'])

now = dt.now()
#now = now-timedelta(hours=12)
before = now-timedelta(days=110)
before2 = before-timedelta(days=30)
now = now.strftime("%Y-%m-%d %H:%M")
before = before.strftime("%Y-%m-%d %H:%M")
before2 = before2.strftime("%Y-%m-%d %H:%M")

   
ohlc_day = {}
for ticker in nifty100:
    try:
        ohlc_day[ticker] = fetchOHLC(ticker, tokendf.loc[ticker,'token'], 'ONE_DAY', before2, before)
        time.sleep(0.2)
    except:
        print(ticker," failed to connect")


ohlc_day2 = {}
for ticker in nifty100:
    ohlc_day2[ticker] = ohlc_day[ticker].copy(deep=True)
ohlc_day2['DateTime'] = ohlc_day2['DateTime'].dt.tz_localize(None)

ohlc_3min = {}
for ticker in nifty100:
    try:
        ohlc_3min[ticker] = fetchOHLC(ticker, tokendf.loc[ticker,'token'], 'THREE_MINUTE', before2, before)
        time.sleep(0.2)
    except:
        print(ticker," failed to connect")

ohlc_3min2 = {}
for ticker in nifty100:
    ohlc_3min2[ticker] = ohlc_3min[ticker].copy(deep=True)
ohlc_3min2['DateTime'] = ohlc_3min2['DateTime'].dt.tz_localize(None)   
    
    
    
for ticker in nifty100:
    ohlc_day2[ticker] = ohlc_day2[ticker].drop(index=(len(ohlc_day2[ticker])-1))
    
    
ohlc['ABB-EQ'].dtypes
  
ohlc = {}
#ohlc.loc['ABB-EQ'] = fetchOHLC('ABB-EQ',tokendf.loc['ABB-EQ','token'],'FIVE_MINUTE',before,now)
for x in nifty100:
    try:
        ohlc[x] = fetchOHLC(x,tokendf.loc[x,'token'],'FIVE_MINUTE',before,now)
    except:
        print(x," failed to connect")

ohlcbefore = {}
for x in nifty100:
    try:
        ohlcbefore[x] = fetchOHLC(x,tokendf.loc[x,'token'],'FIVE_MINUTE',before2,before)
    except:
        print(x," failed to connect")
    
       
def place_order(ticker,token,txntype,
    try:
        orderparams = {
            "variety": "ROBO",
            "tradingsymbol" : "HDFCBANK-EQ",
            "symboltoken" : "1333",
            "transactiontype": "SELL",
            "exchange": "NSE",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "squareoff": "0",
            "stoploss": "1525",
            "trailingStopLoss": ""
            "quantity": "1"
            }
        orderId=obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))    
    except Exception as e: 
        print("Order placement failed: {}".format(e.message))

###################################################################################
def trend(sloped):
    if sloped>25:
        return "uptrend"
    elif sloped<-25:
        return "downtrend"
    else:
        return "no trend"
    

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

for ticker in nifty100:
    ohlc2[ticker]["roll_max_vol"] = ohlc2[ticker]["volume"].rolling(10).max()
    
    
def main():
    
    
    
starttime=time.time()
timeout = time.time() + 60*60*4  # 60 seconds times 360 meaning 6 hrs
while time.time() <= timeout:
    try:
        main()
        time.sleep(300 - ((time.time() - starttime) % 300.0))
    except:
        print('\n\nKeyboard exception received. Exiting.')
        exit()        
##########################################################################################

try:
    logout=obj.terminateSession('K335277')
    print("Logout Successfull")
except Exception as e:
    print("Logout failed: {}".format(e.message))
