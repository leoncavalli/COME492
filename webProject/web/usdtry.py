from datetime import timedelta
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly
import numpy as np
from dateutil.parser import parse
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from sklearn.metrics import mean_squared_error
from math import sqrt
from statsmodels.tsa.stattools import adfuller, acf, pacf
import holidays
import warnings
from plotly.offline import plot
from plotly.graph_objs import Scatter

def getNextDate(data):
    lastdate = (data.index[-1]).date()
    nextday=lastdate+timedelta(days=1)
    return nextday

def getData():


    df = pd.read_csv(r'C:\djangoProject\webProject\web\dolartry2.csv')
    ts=pd.Series(df['Price'].values,index=pd.to_datetime(df['Date']))
    return ts

def currentGraph():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(ts.index), y=list(ts.values)))
    # Set title
    fig.update_layout(
        title_text="USD-TRY Graph"
    )
    plot_div2 = plot(fig,
            output_type='div')
    return plot_div2
# def test_stationarity(timeseries):
#     # Determing rolling statistics
#     rolmean = pd.Series(timeseries).rolling(window=12).mean()
#     rolstd = pd.Series(timeseries).rolling(window=12).std()
#
#     # Plot rolling statistics:
#     orig = plt.plot(timeseries, color='blue', label='Original')
#     mean = plt.plot(rolmean, color='red', label='Rolling Mean')
#     std = plt.plot(rolstd, color='black', label='Rolling Std')
#     plt.legend(loc='best')
#     plt.title('Rolling Mean & Standard Deviation')
#     plt.show(block=False)
#
#     # Perform Dickey-Fuller test:
#     print('Results of Dickey-Fuller Test: ')
#     dftest = adfuller(timeseries, autolag='AIC')
#     dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
#     for key, value in dftest[4].items():
#         dfoutput['Critical Value (%s)' % key] = value
#     print(dfoutput)
def forecast():
    ts=getData()
    ts_logtransformed=np.log(ts)
    # plt.plot(ts_logtransformed, label = 'Log Transformed')
    # plt.plot(Rolling_average, color = 'red', label = 'Rolling Average')
    #log_Rolling_difference = ts_logtransformed - Rolling_average
    #log_Rolling_difference.dropna(inplace=True)
# plt.plot(log_Rolling_difference)
# test_stationarity(log_Rolling_difference)


# //TRAIN TEST PREDICTION
# X = ts.values
# size = int(len(X) * 0.90)
# train, test = X[0:size], X[size:len(X)]
# history = [x for x in train]
# predictions = list()
# for t in range(len(test)):
# 	model = ARIMA(history, order=(6,1,2))
# 	model_fit = model.fit(disp=0)
# 	output = model_fit.forecast()
# 	yhat = output[0]
# 	predictions.append(yhat)
# 	obs = test[t]
# 	history.append(obs)
# 	print('predicted=%f, expected=%f' % (yhat, obs))
# error = mean_squared_error(test, predictions)
# print('Test MSE: %.3f' % error)
# # plot
# plt.plot(ts)
# predictions=pd.Series(predictions,index=ts[256:].index)
# print(predictions)
# plt.plot(predictions, color='red')
# plt.show()


#  ///   PLOTTING ACF AND PACF TO DETERMINE P AND Q VALUES
# lag_acf=acf(ts_diff_logtrans,nlags=30)
# lag_pacf=pacf(ts_diff_logtrans,nlags=50,method='ols')
# plt.subplot(121)
# plt.plot(lag_acf)
# plt.axhline(y=0,linestyle='--',color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(ts_diff_logtrans)),linestyle='--',color='gray')
# plt.axhline(y=1.96/np.sqrt(len(ts_diff_logtrans)),linestyle='--',color='gray')
# plt.title('Autocorrelation Function')
# plt.subplot(122)
# plt.plot(lag_pacf)
# plt.axhline(y=0,linestyle='--',color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(ts_diff_logtrans)),linestyle='--',color='gray')
# plt.axhline(y=1.96/np.sqrt(len(ts_diff_logtrans)),linestyle='--',color='gray')
# plt.title('Partial Autocorrelation Function')
# plt.tight_layout()
# plt.show()


    model = ARIMA(ts_logtransformed, order=(5, 1, 0))
    results_ARIMA = model.fit(trend= 'nc', disp=-1)
    #plt.plot(ts_diff_logtrans)
        # plt.plot(results_ARIMA.fittedvalues, color='red', label = 'p =8, q =18')
    #RSS =results_ARIMA.fittedvalues-ts_diff_logtrans
    #RSS.dropna(inplace=True)
# plt.title('RSS: %.4f'% sum(RSS**2))
# plt.legend(loc='best')

# predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
# predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
# predictions_ARIMA_log = pd.Series(ts_logtransformed, index=ts_logtransformed.index)
# predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
# predictions_ARIMA = np.exp(predictions_ARIMA_log)
# plt.plot(ts)
# plt.plot(predictions_ARIMA)
# plt.show()


#   ///    PREDICTING FUTURE VALUES
    dates = pd.date_range(getNextDate(ts), periods=10, freq='B')
    forecast = pd.Series(results_ARIMA.forecast(steps=10)[0],dates)
    forecast = np.exp(forecast)
    # print(forecast)
    # plt.plot(forecast)
    # plt.show()


    #  ///  FIGURE OUR GRAPH
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(ts.index), y=list(ts.values)))
    fig.add_trace(go.Scatter(x=list(dates),y=list(forecast.values)))
    # Set title
    fig.update_layout(
        title_text="Time series with range slider and selectors"
    )

# Add range slider
# fig.update_layout(
#     xaxis=go.layout.XAxis(
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1,
#                      label="1m",
#                      step="month",
#                      stepmode="backward"),
#                 dict(count=6,
#                      label="6m",
#                      step="month",
#                      stepmode="backward"),
#                 dict(count=1,
#                      label="YTD",
#                      step="year",
#                      stepmode="todate"),
#                 dict(count=1,
#                      label="1y",
#                      step="year",
#                      stepmode="backward"),
#                 dict(step="all")
#             ])
#         ),
#         rangeslider=dict(
#             visible=True
#         ),
#         type="date"
#     )
# )
    plot_div = plot(fig,
            output_type='div')

    # aPlot=plotly.io.to_html(fig)#Turns our graph in python to HTML code.
    #graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")

    return plot_div
# fig.show()#Shows figure in web browser
# print(aPlot)
# with open("webPage.html", 'w') as f:
#     f.write(aPlot)

