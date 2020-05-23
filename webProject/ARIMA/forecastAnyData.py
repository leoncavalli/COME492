from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import holidays
import investpy
import math
from statsmodels.tsa.statespace.sarimax import SARIMAX
import time
from sklearn.metrics import r2_score


def getData(stock,fromdate,todate,period):
    data = investpy.get_stock_historical_data(stock=stock,country='turkey',
                                              from_date=fromdate,
                                              to_date=todate,interval=period)
    keep_col=['Close']
    data=data[keep_col]
    data.index=pd.to_datetime(data.index)
    data=pd.Series(data['Close'].values,index=data.index)

    return data

def getNextDate(data):
    lastdate = (data.index[-1]).date()
    nextday=lastdate+timedelta(days=1)
    return nextday

class Metrics:
    def __init__(self,forecast,actual):
        self.metrictypes=['SMAPE','RMSE','MSE']
        self.forecast=forecast
        self.actual=actual
        self.results={r:None for r in self.metrictypes}

    def R2(self):
        return r2_score(self.actual,self.forecast)
    def sMAPE(self):##define SMAPE metric
        return 100/len(self.actual) * np.sum(2 * np.abs(self.forecast - self.actual) / (np.abs(self.actual) + np.abs(self.forecast)))
    def RMSE(self):##define RMSE metric
        return np.sqrt(((self.forecast - self.actual) ** 2).mean())
    def MSE(self):
        return mean_squared_error(self.forecast,self.actual)
    def run(self):
        self.results['R2']=self.R2()
        self.results['SMAPE']=self.sMAPE()
        self.results['RMSE']=self.RMSE()
        self.results['MSE']=self.MSE()

        return self.results

def figGraph(forecast,actualseries):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(actualseries.index), y=list(actualseries.values),line_color='deepskyblue',name="Actual"))
    fig.add_trace(go.Scatter(x=list(forecast.index), y=list(forecast.values),line_color='red',name="Forecast"))
    fig.update_layout(
        title_text=" FORECAST MODEL",
        xaxis_title = "Dates",
        yaxis_title = "Close Price",
    )
    plot=plotly.offline.plot(fig)
    return plot


def ForecastFuture(data):
    dataValues= data.values
    history = [x for x in dataValues]
    predictions = list()
    for t in range(12):
        model = ARIMA(history, order=(12,1,4))
        model_fit = model.fit(disp=-1)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = yhat
        history.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))
    predictions=np.ravel(predictions)
    dates = pd.date_range(getNextDate(data), periods=12, freq='M')
    predictions=pd.Series(predictions,index=dates)
    plt.plot(predictions, color='red')
    figGraph(predictions,data)

def trainTestForecast(stock,fromdate,todate,period,metrics):
    data=getData(stock,fromdate,todate,period)
    dataValues=data.values
    size = int(len(dataValues) * 0.90)
    train, test = dataValues[0:size], dataValues[size:len(dataValues)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(3,1,0))
        model_fit = model.fit(disp=-1)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))
    predictions=np.ravel(predictions)
    predictions=pd.Series(predictions,index=data[size:].index)
    err=Metrics(predictions,test).run()
    errors={k:err[k] for k in metrics if k in err}
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(data.index), y=data.values,line_color='deepskyblue',name="Actual"))
    fig.add_trace(go.Scatter(x=list(predictions.index), y=predictions,line_color='red',name="Forecast"))
    fig.update_layout(
        title_text=stock+ " FORECAST MODEL",
        xaxis_title = "Dates",
        yaxis_title = "Close Price",
    )
    plot=plotly.offline.plot(fig,output_type='div')
    return plot,errors





