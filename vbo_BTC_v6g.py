import time
from datetime import datetime
import pyupbit
import pandas as pd
import myUpbit
import math

Upbit_AccessKey = ""
Upbit_SecretKey = ""

upbit = pyupbit.Upbit(Upbit_AccessKey, Upbit_SecretKey)

api_call_interval = 5

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

pf = ["KRW-BTC", "KRW-ETH", "KRW-SOL", "KRW-XRP", "KRW-ADA"]
pf_ratio = [.3, .15, .35, .1, .1]
hold_ratio_tgt = 0.3

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
hold_ratio_tot = 0

hold_amt = myUpbit.get_volume(balances, target_ticker)
for i in range(5):
    # print("pf[i]:", pf[i])
    # input("Please press the Enter key to proceed")
    hold_amt_ticker = myUpbit.get_volume(balances, pf[i])
    if hold_amt_ticker > 0:
        # print("pf_ratio[i]:", pf_ratio[i])
        # input("Please press the Enter key to proceed")
        hold_ratio_tot += pf_ratio[i]
print("hold_amt:", hold_amt)
print("hold_ratio_tot:", hold_ratio_tot)
# input("Please press the Enter key to proceed")

# 투자 가능 KRW
avlb_krw = myUpbit.get_avlb_krw(balances)
if hold_amt == 0:
    avlb_krw = float(avlb_krw) * (hold_ratio_tgt/(1-hold_ratio_tot)) * 0.99
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
        hold_ratio_tot = 0

        hold_amt = myUpbit.get_volume(balances, target_ticker)
        for i in range(5):
            hold_amt_ticker = myUpbit.get_volume(balances, pf[i])
            if hold_amt_ticker > 0:
                hold_ratio_tot += pf_ratio[i]

        # 투자 가능 금액 계산
        avlb_krw = myUpbit.get_avlb_krw(balances)
        if hold_amt == 0:
            avlb_krw = float(avlb_krw) * (hold_ratio_tgt/(1-hold_ratio_tot)) * 0.99
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