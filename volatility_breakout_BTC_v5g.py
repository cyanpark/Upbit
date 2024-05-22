import time
from datetime import datetime
import pyupbit
import pandas as pd
import myUpbit
import math

Upbit_AccessKey = ""
Upbit_SecretKey = ""

upbit = pyupbit.Upbit(Upbit_AccessKey, Upbit_SecretKey)

api_call_interval = 2

###############################################################################
# method
def calc_target_price(df):
    df['hma10'] = df['high'].rolling(10).mean()

    yesterday = df.iloc[-2]

    long_target = yesterday['hma10']

    return long_target

###############################################################################
# TEST
# ohlcv = pyupbit.get_ohlcv(ticker="KRW-BTC", interval="day", count=300)
# time.sleep(api_call_interval)
# ohlcv.to_csv('D:/Study/Upbit/Upbit_BTCKRW.csv')
# print(ohlcv)
# input("Please press the Enter key to proceed")

###############################################################################
# Execution
target_ticker = "KRW-BTC"
print("\ntarget_ticker:", target_ticker)

# 캔들 정보 조회
ohlcv = pyupbit.get_ohlcv(ticker=target_ticker, interval="day")
time.sleep(api_call_interval)

# 현재 날짜 확인
monitoring_date = ohlcv.index[-1]
print("\ndate_today:", monitoring_date)

# 시가
open_price = float(ohlcv['open'].values[-1])
print("open_price:", open_price)

# 돌파 가격 계산
long_target = calc_target_price(ohlcv)
print("long_target:", long_target)

# 원화 잔고 조회
balances = upbit.get_balances()
time.sleep(api_call_interval)
# print(balances)

# 종목 보유 수량
hold_amt = myUpbit.get_volume(balances, target_ticker)
hold_amt_eth = myUpbit.get_volume(balances, "KRW-ETH")
print("hold_amt:", hold_amt)

# 투자 가능 KRW
avlb_krw = myUpbit.get_avlb_krw(balances)
if (hold_amt == 0) and (hold_amt_eth == 0):
    avlb_krw = float(avlb_krw) * 0.99 * (1/2)
elif (hold_amt == 0) and (hold_amt_eth > 0):
    avlb_krw = float(avlb_krw) * 0.99
else:
    avlb_krw = 0
print("avlb_krw:", avlb_krw)
# input("Please press the Enter key to proceed")

# Loop
while True:
    try:
        # 캔들 정보 조회
        ohlcv = pyupbit.get_ohlcv(ticker=target_ticker, interval="day")
        time.sleep(api_call_interval)

        # 현재 날짜 확인
        date_today = ohlcv.index[-1]

        # 원화 잔고 조회
        balances = upbit.get_balances()
        time.sleep(api_call_interval)

        # 종목 보유 수량
        hold_amt = myUpbit.get_volume(balances, target_ticker)
        hold_amt_eth = myUpbit.get_volume(balances, "KRW-ETH")

        # 투자 가능 금액 계산
        avlb_krw = myUpbit.get_avlb_krw(balances)
        if (hold_amt == 0) and (hold_amt_eth == 0):
            avlb_krw = float(avlb_krw) * 0.99 * (1/2)
        elif (hold_amt == 0) and (hold_amt_eth > 0):
            avlb_krw = float(avlb_krw) * 0.99
        else:
            avlb_krw = 0

        # 시점 갱신 확인
        if monitoring_date != date_today:
            print("\ndate_today:", date_today)

            # 시가
            open_price = float(ohlcv['open'].values[-1])
            print("open_price:", open_price)

            # 돌파 가격 계산
            long_target = calc_target_price(ohlcv)
            print("long_target:", long_target)

            # 종목 정리
            if (hold_amt > 0) and (open_price < long_target):
                ret = upbit.sell_market_order(target_ticker, hold_amt)
                time.sleep(10)
            
            # 시작 시점 업데이트
            monitoring_date = date_today

        else:
            # 돌파 감지
            cur_price = ohlcv['close'].values[-1]
            if hold_amt == 0 and cur_price > long_target:
                ret = upbit.buy_market_order(target_ticker, avlb_krw)
                time.sleep(10)
        
        time.sleep(api_call_interval)

    except Exception as e:
        print(time.strftime('%m/%d %H:%M:%S'), "Exception: " + str(e))