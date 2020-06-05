import numpy as np
import matplotlib.pyplot as plt
from keras.losses import mean_absolute_error
import pandas as pd
import math
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import os
import investpy
import plotly
import plotly.graph_objects as go


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def getData(stock,fromdate,todate,period):
    data = investpy.get_stock_historical_data(stock=stock,country='turkey',
                                              from_date=fromdate,
                                              to_date=todate,interval=period)
    keep_col=['Close']
    data=data[keep_col]
    data.index=pd.to_datetime(data.index)

    return data

def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)




def lstmForecast(stock,fromdate,todate,period):
    data=getData(stock,fromdate,todate,period)

    dataset = data.values
    dataset = dataset.astype('float32')
    # normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)

    # split into train and test sets
    train_size = int(len(dataset) * 0.9)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size], dataset[train_size:]
    # reshape into X=t and Y=t+1
    look_back = 1
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    
    
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(50, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=50, batch_size=1, verbose=2, shuffle=False)
    # make predictions
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)


    # invert predictions
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])


    # calculate root mean squared error
    scoreRMS = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
    scoreMS = mean_squared_error(testY[0], testPredict[:, 0])
    scoreMAE = mean_absolute_error(testY[0], testPredict[:, 0])
    # shift train predictions for plotting
    trainPredictPlot = np.empty_like(dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = np.empty_like(dataset)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(dataset) - 1, :] = testPredict

    actuals=pd.Series(np.ravel(data.values),index=data.index)
    predictions=pd.Series(np.ravel(testPredictPlot[train_size:]),index=data.index[train_size:])
    # plot baseline and predictions

    fig = go.Figure()
    trace0 = go.Scatter(x=actuals.index, y=actuals, line_color='deepskyblue', name="Actual")
    trace1 = go.Scatter(x=predictions.index, y=predictions, line_color='red', name="Forecast")
    fig.add_trace(trace0)
    fig.add_trace(trace1)
    fig.update_layout(
        title_text=stock + " FORECAST MODEL",
        xaxis_title="Dates",
        yaxis_title="Close Price",
    )
    data=[trace0,trace1]
    myfigure=go.Figure(data=data)

    myfigure.update_layout(
        margin=dict(l=20, r=0, t=80, b=50),
        title_text=stock+ " FORECAST MODEL",
        xaxis_title = "Dates",
        yaxis_title = "Close Price",
        
    )
    myfigurejson=myfigure.to_json()
  
  
    plot = plotly.offline.plot(fig, output_type='div')
    return myfigurejson

def lstmForecastWeb(stock,fromdate,todate,period):
    data=getData(stock,fromdate,todate,period)

    dataset = data.values
    dataset = dataset.astype('float32')
    # normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)

    # split into train and test sets
    train_size = int(len(dataset) * 0.9)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size], dataset[train_size:]
    # reshape into X=t and Y=t+1
    look_back = 1
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    
    
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(50, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=50, batch_size=1, verbose=2, shuffle=False)
    # make predictions
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)


    # invert predictions
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])


    # calculate root mean squared error
    scoreRMS = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
    scoreMS = mean_squared_error(testY[0], testPredict[:, 0])
    scoreMAE = mean_absolute_error(testY[0], testPredict[:, 0])
    # shift train predictions for plotting
    trainPredictPlot = np.empty_like(dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = np.empty_like(dataset)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(dataset) - 1, :] = testPredict

    actuals=pd.Series(np.ravel(data.values),index=data.index)
    predictions=pd.Series(np.ravel(testPredictPlot[train_size:]),index=data.index[train_size:])
    # plot baseline and predictions

    fig = go.Figure()
    trace0 = go.Scatter(x=actuals.index, y=actuals, line_color='deepskyblue', name="Actual")
    trace1 = go.Scatter(x=predictions.index, y=predictions, line_color='red', name="Forecast")
    fig.add_trace(trace0)
    fig.add_trace(trace1)
    fig.update_layout(
        title_text=stock + " FORECAST MODEL",
        xaxis_title="Dates",
        yaxis_title="Close Price",
    )
    
    plot = plotly.offline.plot(fig, output_type='div')
    return plot