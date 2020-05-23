from datetime import timedelta
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly
import numpy as np
from plotly.graph_objs import *
from dateutil.parser import parse
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from sklearn.metrics import mean_squared_error
from math import sqrt
from statsmodels.tsa.stattools import adfuller, acf, pacf
import holidays
import warnings
import investpy
import math

def getData():
    datam=pd.read_excel('C:\djangoProject\webProject\ARIMA\data.xlsx')
    datam.index=pd.to_datetime(datam['tarih'])
    price = datam['bist_deger']
    s1=datam['S1']
    s1Series=pd.Series(s1,index=datam.index)
    dataSeries = pd.Series(price, index=datam.index)
    return dataSeries

def s1s2s3(value):
    keep_col=[value]
    myData=datam[keep_col]
    return myData

def sMAPE(F,A):
    return 100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))
def RMSE(predict, target):
    return np.sqrt(((predict - target) ** 2).mean())


def trainTestForecast():
    data=getData()
    dataValues= data.values
    size = int(len(dataValues) * 0.90)
    train, test = dataValues[0:size], dataValues[size:len(dataValues)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5,0,1))
        model_fit = model.fit(disp=-1)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        # print('predicted=%f, expected=%f' % (yhat, obs))
    predictions=np.ravel(predictions)
    predictions=pd.Series(predictions,index=data[size:].index)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=list(data.values),line_color='deepskyblue'))
    fig.add_trace(go.Scatter(x=predictions.index, y=list(predictions.values), line_color='red'))
    fig.update_layout(
         paper_bgcolor= 'rgba(255,255,255,1)',
         plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20))
    plot=plotly.offline.plot(fig,output_type='div')
    return plot
 


def trainTestForecast_semantic(data,semanticNumber):
    mySemantic=s1s2s3(semanticNumber)
    dataValues= data.values
    size = int(len(dataValues) * 0.90)
    semantic = mySemantic.values
    train, test = dataValues[0:size], dataValues[size:len(dataValues)]
    s1,s1tst=semantic[0:size],semantic[size:len(dataValues)]
    s1xtest=semantic[size:]
    history = [x for x in train]
    S1=[y for y in s1]
    predictions = list()
    for t in range(len(test)):
        model = SARIMAX(history,exog=S1, order=(3,1,1))
        model_fit = model.fit(disp=-1)
        output = model_fit.forecast(exog=[s1xtest[t]])
        yhat = output
        predictions.append(yhat)
        obsS1=s1tst[t]
        S1.append(obsS1)
        obs = test[t]
        history.append(obs)
        # print('predicted=%f, expected=%f' % (yhat, obs))
    # plt.plot(data)
    predictions=pd.Series(predictions,index=data[size:].index)
    # print(predictions)
    # plt.plot(predictions, color='red')
    # plt.show()
    print("MAPE "+semanticNumber+": " + str(sMAPE(predictions, test)))
    print("RMSE "+semanticNumber+": " + str(RMSE(predictions, test)))
    print("MSE "+semanticNumber+": "+str(mean_squared_error(predictions,test)))





