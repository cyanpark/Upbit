import time
from decimal import Decimal

import pandas_ta as ta
import pyupbit

import dateutil
from datetime import datetime

#
api_call_interval = 0.5



def get_indicators(ohlcv):
    ohlcv['CCI'] = ta.cci(ohlcv['high'], ohlcv['low'], ohlcv['close'], length=14)
    ohlcv['RSI'] = ta.rsi(ohlcv['close'], length=14)

    return ohlcv


def get_top_acc_trade_price_24h(curr_price):
    acc_trade_price_24h = {}

    for ticker_price in curr_price:
        acc_trade_price_24h[ticker_price['market']] = ticker_price['acc_trade_price_24h']

    tickers_sorted_by_acc_price = dict(sorted(acc_trade_price_24h.items(), key=lambda x: x[1], reverse=True))
    top_acc_price = list(tickers_sorted_by_acc_price.keys())

    return top_acc_price


def get_hold_tickers(balances, tickers):
    hold_tickers = []
    hold_volumes = {}
    for balance in balances:
        ticker_name = balance['unit_currency'] + "-" + balance['currency']
        buy_money = float(balance['balance']) * float(balance['avg_buy_price'])

        if ((ticker_name in tickers) and (buy_money > 5000)):
            hold_tickers.append(ticker_name)
            hold_volumes[ticker_name] = balance['balance']

    return hold_tickers, hold_volumes


def get_avlb_krw(balances):
    for balance in balances:
        if balance['currency'] == "KRW":
            return float(balance['balance'])


def get_avg_buy_price(balances, ticker):
    for balance in balances:
        ticker_name = balance['unit_currency'] + "-" + balance['currency']

        if ticker == ticker_name:
            return float(balance['avg_buy_price'])


def get_last_buy_order(order_list):
    # 매도(ask) 또는 매수(bid) 만 남길 경우
    for order in order_list:
        if order['side'] == "bid":
            return order


# 티커에 해당하는 코인이 매수된 상태면 참을 리턴하는함수
def IsHasCoin(balances, ticker):
    HasCoin = False
    for value in balances:
        market_ticker = value['unit_currency'] + "-" + value['currency']
        if ticker == market_ticker:
            HasCoin = True
    return HasCoin


# 티커에 해당하는 코인의 보유수량을 리턴한다.
def get_volume(balances, ticker):
    volume = 0
    for value in balances:
        market_ticker = value['unit_currency'] + "-" + value['currency']
        if ticker == market_ticker:
            volume = Decimal(value['balance']) + Decimal(value['locked'])
    return float(volume)


def get_resistance_price(df):
    pivots = []
    dates = []
    counter = 0
    lastPivot = 0

    Range = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in df.index:
        currentMax = max(Range, default=0)
        value = df["high"][i]

        Range = Range[1:9]
        Range.append(value)
        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == max(Range, default=0):
            counter += 1
        else:
            counter = 0

        if counter == 5:
            lastPivot = currentMax
            dateloc = Range.index(lastPivot)
            lastDate = dateRange[dateloc]

            pivots.append(lastPivot)
            dates.append(lastDate)

    # for index in range(len(pivots)):
    #     print(str(pivots[index])+": "+str(dates[index]))

    return dates, pivots


def get_support_price(df):
    pivots = []
    dates = []
    counter = 0
    lastPivot = 0

    Range = [1E+08, 1E+08, 1E+08, 1E+08, 1E+08, 1E+08, 1E+08, 1E+08, 1E+08, 1E+08]
    dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in df.index:
        currentMax = min(Range, default=1E+08)
        value = df["low"][i]

        Range = Range[1:9]
        Range.append(value)
        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == min(Range, default=1E+08):
            counter += 1
        else:
            counter = 0

        if counter == 5:
            lastPivot = currentMax
            dateloc = Range.index(lastPivot)
            lastDate = dateRange[dateloc]

            pivots.append(lastPivot)
            dates.append(lastDate)

    # for index in range(len(pivots)):
    #     print(str(pivots[index])+": "+str(dates[index]))

    return dates, pivots