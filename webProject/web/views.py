from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from plotly.offline import plot
from plotly.graph_objs import Scatter
from web import example
from web import usdtry
from ARIMA import bist30Arima
from ARIMA import forecastAnyData
from LSTM import lstm
import json
from django.shortcuts import render
from . import forms
from TradeRobot import trader
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
import json


class HomePageView(TemplateView):
    template_name = 'index.html'
 
def lstmview(request):
    stocks=forms.STOCK_CHOICES
    periods=forms.PERIODS
    metrics=forms.METRICS
    if request.method == 'POST':
        stocks = request.POST.get('stock')
        trdate1 = request.POST.get('trdate1_')
        trdate2 = request.POST.get('trdate2_')
        period = request.POST.get('period')
        request.session['name'] = stocks
        request.session['trdate1_'] = trdate1
        request.session['trdate2_'] = trdate2
        request.session['period'] = period
        return redirect('lstmForecast')
    return render(request,'lstm.html',context={'stocks':stocks,'periods':periods,'metrics':metrics})
    
def lstmForecast(request):
    stok = request.session['name']
    trdate1 = request.session['trdate1_']
    trdate2 = request.session['trdate2_']
    period = request.session['period']
    div = lstm.lstmForecastWeb(stok,trdate1,trdate2,period)
    return render(request, 'lstmForecast.html', context={'div': div})

def arimaview(request):
    stocks=forms.STOCK_CHOICES
    periods=forms.PERIODS
    metrics=forms.METRICS
    if request.method == 'POST':
        stocks = request.POST.get('stock')
        trdate1 = request.POST.get('trdate1')
        trdate2 = request.POST.get('trdate2')
        period = request.POST.get('period')
        metric=request.POST.getlist('metric')
        request.session['name'] = stocks
        request.session['trdate1'] = trdate1
        request.session['trdate2'] = trdate2
        request.session['period'] = period
        request.session['metric'] = metric
        return redirect('arimaForecast')
    return render(request,'arima.html',context={'stocks':stocks,'periods':periods,'metrics':metrics})


def forecast(request):
    stok = request.session['name']
    trdate1 = request.session['trdate1']
    trdate2 = request.session['trdate2']
    period = request.session['period']
    metric = request.session['metric']
    values = forecastAnyData.trainTestForecastWeb(stok,trdate1,trdate2,period,metric)
    div=values[0]
    errors=values[1]
    return render(request, 'arimaForecast.html', context={'div': div,'errors':errors})


def ChoosePage(request):
    template_name = 'chooseModel.html'
    return render(request, template_name)


def StockPage(request):
    stocks=forms.STOCK_CHOICES
    template_name = 'stocks.html'
    return render(request, template_name,context={'stocks':stocks})

def CurrencyPage(request):
    currencies=forms.CURRENCY
    template_name = 'currencies.html'
    return render(request, template_name,context={'currencies':currencies})

def CryptoPage(request):
    cryptos=forms.CRYPTO
    template_name = 'cryptos.html'
    return render(request, template_name,context={'cryptos':cryptos})

def TradeRobot(request):
    stocks=forms.STOCK_CHOICES
    if request.method == 'POST':
        trstock = request.POST.getlist('trstocks')
        trdate1 = request.POST.get('trdate1')
        trdate2 = request.POST.get('trdate2')
        trbudget = request.POST.get('trbudget')
        request.session['trstocks'] = trstock
        request.session['trdate1'] = trdate1
        request.session['trdate2'] = trdate2
        request.session['trbudget'] = trbudget
        return redirect('TradeRobotResult')
    template_name='tradeRobot.html'
    return render(request,template_name,context={'stocks':stocks})

def TradeRobotResult(request):  
    trstock  =  request.session['trstocks'] 
    trdate1  =  request.session['trdate1']
    trdate2  =  request.session['trdate2'] 
    trbudget =  request.session['trbudget']
    app = trader.Robot(trstock,int(trbudget),trdate1,trdate2)
    vals=app.run()  
    finalBudget=vals[0]
    finalPortfolio=json.dumps(vals[1])
    cash=vals[2]
    latests=json.dumps(vals[3])
    template_name='traderResult.html'
    return render(request,template_name,context={'trbudget':trbudget,'cash':cash,'finalBudget':finalBudget,'finalPortfolio':finalPortfolio,'latests':latests})

@api_view(['POST'])
def simpleapi(stockdata):
    try:
        data=json.loads(stockdata.body) 
        stock=data['stock']
        startDate=data['startDate']
        endDate=data['endDate']
        period=data['period']
        values = forecastAnyData.trainTestForecast(stock,startDate,endDate,period,['R2'])
        return Response(json.loads(values[0]))
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def simpleapi2(stockdata):
    try:
        data=json.loads(stockdata.body) 
        stock=data['stock']
        startDate=data['startDate']
        endDate=data['endDate']
        period=data['period']
        values = lstm.lstmForecast(stock,startDate,endDate,period)
        return Response(json.loads(values))
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def simpleapi3(stockdata):
    try:
        data=json.loads(stockdata.body)
        stocks=data['selectedItems']
        budget=data['budget']
        fromdate=data['fromdate']
        todate=data['todate']
        app = trader.Robot(stocks,int(budget),fromdate,todate)
        values=app.run()  
        jsondata=json.dumps({'budget':values[0],'portfolio':values[1],'cash':values[2],'latests':values[3]})
        return Response(json.loads(jsondata))
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)