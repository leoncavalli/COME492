import pandas as pd
import numpy as np
import investpy as inv
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import matplotlib.pyplot as plt
import statsmodels.api as sm
from talib import RSI


def getData(stock, fromdate, todate):
    data = inv.get_stock_historical_data(stock=stock,
                                         country='Turkey',
                                         from_date=fromdate, to_date=todate,
                                         interval='Daily')
    data = pd.DataFrame(data)

    exp1 = data.Close.ewm(span=12, adjust=False).mean()
    exp2 = data.Close.ewm(span=26, adjust=False).mean()

    macd = exp1 - exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()

    data['macd'] = macd
    data['signal'] = exp3

    data['rsi'] = RSI(data['Close'], timeperiod=14)

    data['Mavg5'] = data['Close'].rolling(window=5).mean()
    data['Mavg20'] = data['Close'].rolling(window=20).mean()

    return data


class Signals:
    def __init__(self, data, i):
        self.data = data
        self.i = i

    def buysignalSMA(self):
        if (self.data['Mavg5'][self.i] <= self.data['Mavg20'][self.i]) & (
                self.data['Mavg5'][self.i - 1] >= self.data['Mavg20'][self.i - 1]):
            print ("Buy signal SMA")
            print ("---------------")

            print(str(self.data['Close'][self.i]) + "   " + str(self.data.index[self.i]))
            return True
        else:
            return False

    def buysignalMACD(self):
        if (self.data['macd'][self.i - 1] <= self.data['signal'][self.i - 1]) & (
                self.data['macd'][self.i] >= self.data['signal'][self.i]):
            print ("Buy signal MACD")
            print ("---------------")

            print(str(self.data['Close'][self.i]) + "   " + str(self.data.index[self.i]))
            return True
        else:
            return False

    def buysignalRSI(self):
        if self.data['rsi'][self.i] < 30:
            print ("Buy signal RSI")
            print ("---------------")

            print(str(self.data['Close'][self.i]) + "   " + str(self.data.index[self.i]))
            return True
        else:
            return False

    def sellsignalSMA(self):
        if (self.data['Mavg5'][self.i] >= self.data['Mavg20'][self.i]) & (
                self.data['Mavg5'][self.i - 1] <= self.data['Mavg20'][self.i - 1]):
            print ("Sell signal SMA")
            print ("---------------")

            print(str(self.data['Close'][self.i]) + "   " + str(self.data.index[self.i]))
            return True
        else:
            return False

    def sellsignalRSI(self):
        if self.data['rsi'][self.i] > 65:
            print ("Sell signal RSI")
            print ("---------------")

            print(str(self.data['Close'][self.i]) + "   " + str(self.data.index[self.i]))
            return True
        else:
            return False


class Robot:
    def __init__(self, stocks, budget):
        self.stocks = stocks
        self.initialBudget = budget
        self.budget = budget
        self.cash = 0
        self.Portfolio = {p: 0 for p in stocks}
        self.latestBoughts = {x: [] for x in stocks}

    def getStockData(self):
        stocks = {p: None for p in self.stocks}
        for i in range(len(self.stocks)):
            stok = getData(self.stocks[i], fromdate='01/01/2019', todate='01/01/2020')
            stocks[self.stocks[i]] = stok

        return stocks

    def getLastPrice(self, data):
        lastprices = {p: None for p in self.stocks}
        for s in self.stocks:
            lastprices[s] = data[s]['Close'][-1]
        return lastprices

    def buy(self, data, i, symbol):
        if self.budget >= data['Close'][i] * 4:
            currentPrice = data['Close'][i]
            self.latestBoughts[symbol].append(currentPrice)
            boughtCount = int(self.budget * 0.15 / currentPrice)
            self.budget = int(self.budget - boughtCount * currentPrice)
            self.Portfolio[symbol] = self.Portfolio[symbol] + boughtCount
            print(str(boughtCount) + " stock bought.")
            print("Your budget is now " + str(self.budget) + " your portfolio " + str(
                self.Portfolio) + "your cash : " + str(self.cash))
            print("***************")
        else:
            print("No enough money in account.")
            print("Your budget is now " + str(self.budget) + " your portfolio " + str(
                self.Portfolio) + "your cash : " + str(self.cash))
            print ("**************")

    def sell(self, data, i, symbol):
        if self.Portfolio[symbol] > 0:
            currentPrice = data['Close'][i]
            if (currentPrice >= np.array(self.latestBoughts[symbol]).mean()):
                sellPiece = self.Portfolio[symbol]
                self.Portfolio[symbol] = self.Portfolio[symbol] - sellPiece
                self.budget = int(self.budget + currentPrice * sellPiece)
                print(str(sellPiece) + "of" + symbol + " stock sold.")
                print("Your budget is now " + str(self.budget) + " your portfolio " + str(
                    self.Portfolio) + "your cash : " + str(self.cash))
                print("************")
                self.checkCash()
                self.latestBoughts[symbol] = []
            else:
                print ("Cant sell at this price")
                print("Your budget is now " + str(self.budget) + " your portfolio " + str(
                    self.Portfolio) + "your cash : " + str(self.cash))
                print("*************")

    def checkCash(self):
        if self.budget > self.initialBudget:
            profit = self.budget - self.initialBudget
            self.cash = self.cash + profit

    def run(self):
        datas = self.getStockData()
        for i in range(len(datas[self.stocks[0]])):
            for s in (self.stocks):
                sgn = Signals(datas[s], i)
                if sgn.buysignalSMA() | sgn.buysignalMACD() | sgn.buysignalRSI():
                    self.buy(datas[s], i, s)
                elif sgn.sellsignalSMA() | sgn.sellsignalRSI():
                    self.sell(datas[s], i, s)
        latests = self.getLastPrice(datas)
        return self.budget, self.Portfolio, self.cash, latests


