from django.urls import path
from .views import HomePageView
#from .views import ArimaPageView
from .views import *

urlpatterns=[
    path('',HomePageView.as_view(),name="index"), 
    path('arima/',arimaview,name="arima"),
    path('lstm/',lstmview,name="lstm"),

    path('arima/forecast',forecast,name="arimaForecast"),
    path('lstm/forecasts',lstmForecast,name="lstmForecast"),

    path('choosemodel/',ChoosePage,name="chooseModel"),
    path('stocks/',StockPage,name="StockPage"),
    path('currencies/',CurrencyPage,name="CurrencyPage"),
    path('cryptos/',CryptoPage,name="CryptoPage"),
    path('traderobot/',TradeRobot,name="TradeRobot"),
    path('traderobot/results',TradeRobotResult,name="TradeRobotResult"),
    path('simpleapi/',simpleapi),  
    path('simpleapi2/',simpleapi2)





]
