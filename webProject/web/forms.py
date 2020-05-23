from django import forms
from django.core import validators
import investpy
import pandas as pd


STOCK_CHOICES=pd.read_csv('bist100.csv')
STOCK_CHOICES=STOCK_CHOICES.values.tolist()

CURRENCY=pd.read_csv('currencies.csv')
CURRENCY=CURRENCY.values.tolist()

CRYPTO=pd.read_csv('cryptos.csv')
CRYPTO=CRYPTO.values.tolist()

PERIODS=[
    ('Daily'),
    ('Weekly'),
    ('Monthly'),
    ('Yearly')]

METRICS=[('R2'),
    ('MSE'),
    ('RMSE'),
    ('SMAPE')]

