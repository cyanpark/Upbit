import time
from datetime import datetime
import pyupbit
import pandas as pd
import myUpbit
import math
import telegram
import asyncio

Upbit_AccessKey = ""
Upbit_SecretKey = ""
upbit = pyupbit.Upbit(Upbit_AccessKey, Upbit_SecretKey)

token = ''
chat_id = 6063855502

api_call_interval = 1

###############################################################################
# method
def send_msg(text_msg):
    bot = telegram.Bot(token = token)
    asyncio.run(bot.send_message(chat_id = chat_id, text = text_msg))

def get_avg_price_market_order(ob, side, size):
    if side == "ask":
        cum_ask_price = 0
        cum_ask_size = 0
        cum_ask_cnt = 0
        for ob_unit in ob['orderbook_units']:
            cum_ask_price = cum_ask_price + float(ob_unit['ask_price'])
            cum_ask_size = cum_ask_size + float(ob_unit['ask_size'])
            cum_ask_cnt = cum_ask_cnt + 1

            if cum_ask_size > size:
                break

        avg_price = cum_ask_price / cum_ask_cnt
    
    else:
        cum_bid_price = 0
        cum_bid_size = 0
        cum_bid_cnt = 0
        for ob_unit in ob['orderbook_units']:
            cum_bid_price = cum_bid_price + float(ob_unit['bid_price'])
            cum_bid_size = cum_bid_size + float(ob_unit['bid_size'])
            cum_bid_cnt = cum_bid_cnt + 1
            
            if cum_bid_size < size:
                break

        avg_price = cum_bid_price / cum_bid_cnt

    return avg_price
###############################################################################
# Execution
Fee_KRW = 0.0005
Fee_BTC = 0.0025

AVL_KRW = 1000000
# BTC_KRW = pyupbit.get_current_price(ticker="KRW-BTC")
# ETH_KRW = pyupbit.get_current_price(ticker="KRW-ETH")
# ETH_BTC = pyupbit.get_current_price(ticker="BTC-ETH")
# time.sleep(api_call_interval)

# print("BTC_KRW:", BTC_KRW)
# print("ETH_KRW:", ETH_KRW)
# print("ETH_BTC:", ETH_BTC)
# E_B_KRW = ETH_KRW / BTC_KRW
# Gap_pctg = round((E_B_KRW - ETH_BTC) / ETH_BTC * 100, 2)
# print("Gap: " + str(Gap_pctg) + "%")


# BTC_KRW_size = round(AVL_KRW / BTC_KRW * (10^8)) / (10^8)
# ETH_KRW_size = round(AVL_KRW / ETH_KRW * (10^8)) / (10^8)


# ob_BTC_KRW = pyupbit.get_orderbook("KRW-BTC")
# ob_ETH_KRW = pyupbit.get_orderbook("KRW-ETH")
# ob_ETH_BTC = pyupbit.get_orderbook("BTC-ETH")
# time.sleep(api_call_interval)

# BTC_volume = AVL_KRW * (1-Fee_KRW) / get_avg_price_market_order(ob_BTC_KRW, "ask", BTC_KRW_size)
# ETH_BTC_size = round(BTC_volume / ETH_BTC * (10^8)) / (10^8)
# E_B_volume = BTC_volume * (1-Fee_BTC) / get_avg_price_market_order(ob_ETH_BTC, "ask", ETH_BTC_size * (1-Fee_BTC))
# KRW_volume = E_B_volume * (1-Fee_KRW) * get_avg_price_market_order(ob_ETH_KRW, "bid", E_B_volume * (1-Fee_KRW))
# print("\n")
# print("BTC_KRW_buy_avgp:", get_avg_price_market_order(ob_BTC_KRW, "ask", BTC_KRW_size))
# print("ETH_BTC_buy_avgp:", get_avg_price_market_order(ob_ETH_BTC, "ask", ETH_BTC_size * (1-Fee_BTC)))
# print("ETH_KRW_sel_avgp:", get_avg_price_market_order(ob_ETH_KRW, "bid", E_B_volume * (1-Fee_KRW)))
# print("BTC/KRW > ETH/BTC > ETH/KRW:", KRW_volume)

# ETH_volume = AVL_KRW * (1-Fee_KRW) / get_avg_price_market_order(ob_ETH_KRW, "ask", ETH_KRW_size)
# E_B_volume = ETH_volume * (1-Fee_BTC) * get_avg_price_market_order(ob_ETH_BTC, "bid", ETH_volume * (1-Fee_BTC))
# KRW_volume = E_B_volume * (1-Fee_KRW) * get_avg_price_market_order(ob_BTC_KRW, "bid", E_B_volume * (1-Fee_KRW))
# print("\n")
# print("ETH_KRW_buy_avgp:", get_avg_price_market_order(ob_ETH_KRW, "ask", ETH_KRW_size))
# print("ETH_BTC_sel_avgp:", get_avg_price_market_order(ob_ETH_BTC, "bid", ETH_volume * (1-Fee_BTC)))
# print("BTC_KRW_sel_avgp:", get_avg_price_market_order(ob_BTC_KRW, "bid", E_B_volume * (1-Fee_KRW)))
# print("ETH/KRW > EHT/BTC > BTC/KRW:", KRW_volume)
# input("Please press the Enter key to proceed")

# Loop
while True:
    try:
        # 캔들 정보 조회
        BTC_KRW = pyupbit.get_current_price(ticker="KRW-BTC")
        ETH_KRW = pyupbit.get_current_price(ticker="KRW-ETH")
        ETH_BTC = pyupbit.get_current_price(ticker="BTC-ETH")
        E_B_KRW = ETH_KRW / BTC_KRW
        time.sleep(api_call_interval)

        Gap_pctg = (E_B_KRW - ETH_BTC) / ETH_BTC * 100
        Gap_pctg = round(Gap_pctg, 2)

        BTC_KRW_size = round(AVL_KRW / BTC_KRW * (10^8)) / (10^8)
        ETH_KRW_size = round(AVL_KRW / ETH_KRW * (10^8)) / (10^8)
        
        ob_BTC_KRW = pyupbit.get_orderbook("KRW-BTC")
        ob_ETH_KRW = pyupbit.get_orderbook("KRW-ETH")
        ob_ETH_BTC = pyupbit.get_orderbook("BTC-ETH")
        time.sleep(api_call_interval)

        # CASE-1 : BTC/KRW > ETH/BTC > ETH/KRW
        BTC_volume = AVL_KRW * (1-Fee_KRW) / get_avg_price_market_order(ob_BTC_KRW, "ask", BTC_KRW_size)
        ETH_BTC_size = round(BTC_volume / ETH_BTC * (10^8)) / (10^8)
        E_B_volume = BTC_volume * (1-Fee_BTC) / get_avg_price_market_order(ob_ETH_BTC, "ask", ETH_BTC_size * (1-Fee_BTC))
        KRW_volume = E_B_volume * (1-Fee_KRW) * get_avg_price_market_order(ob_ETH_KRW, "bid", E_B_volume * (1-Fee_KRW))

        if KRW_volume > AVL_KRW:
            send_msg("CASE-1 : BTC/KRW > ETH/BTC > ETH/KRW" + 
                     "\nBTC_KRW:" + str(BTC_KRW) +
                     "\nETH_KRW:" + str(ETH_KRW) +
                     "\nETH_BTC:" + str(ETH_BTC) +
                     "\nGap: " + str(Gap_pctg) + "%" +
                     "\nBTC_KRW_buy_avgp:" + str(get_avg_price_market_order(ob_BTC_KRW, "ask", BTC_KRW_size)) +
                     "\nETH_BTC_buy_avgp:" + str(get_avg_price_market_order(ob_ETH_BTC, "ask", ETH_BTC_size * (1-Fee_BTC))) +
                     "\nETH_KRW_sel_avgp:" + str(get_avg_price_market_order(ob_ETH_KRW, "bid", E_B_volume * (1-Fee_KRW))) +
                     "\nFinal_KRW:" + str(KRW_volume))

        # CASE-2 : ETH/KRW > EHT/BTC > BTC/KRW
        ETH_volume = AVL_KRW * (1-Fee_KRW) / get_avg_price_market_order("KRW-ETH", "ask", ETH_KRW_size)
        E_B_volume = ETH_volume * (1-Fee_BTC) * get_avg_price_market_order("BTC-ETH", "bid", ETH_volume * (1-Fee_BTC))
        KRW_volume = E_B_volume * (1-Fee_KRW) * get_avg_price_market_order("KRW-BTC", "bid", E_B_volume * (1-Fee_KRW))

        if KRW_volume > AVL_KRW:
            send_msg("CASE-2 : ETH/KRW > EHT/BTC > BTC/KRW" + 
                     "\nBTC_KRW:" + str(BTC_KRW) +
                     "\nETH_KRW:" + str(ETH_KRW) +
                     "\nETH_BTC:" + str(ETH_BTC) +
                     "\nGap: " + str(Gap_pctg) + "%" +
                     "\nETH_KRW_buy_avgp:" + str(get_avg_price_market_order("KRW-ETH", "ask", ETH_KRW_size)) +
                     "\nETH_BTC_sel_avgp:" + str(get_avg_price_market_order("BTC-ETH", "bid", ETH_volume * (1-Fee_BTC))) +
                     "\nBTC_KRW_sel_avgp:" + str(get_avg_price_market_order("KRW-BTC", "bid", E_B_volume * (1-Fee_KRW))) +
                     "\nFinal_KRW:" + str(KRW_volume))
        # input("Please press the Enter key to proceed")

        # # BTC/KRW 저평가
        # if Gap > 0:
        #     upbit.buy_market_order("KRW-BTC", 00000000)
        #     upbit.buy_market_order("BTC-ETH", 00000000)
        #     upbit.sell_market_order("KRW-ETH", 00000000)
        #     time.sleep(api_call_interval)
        
        # # ETH/KRW 저평가
        # elif Gap < 0:
        #     upbit.buy_market_order("KRW-ETH", 00000000)
        #     upbit.sell_market_order("BTC-ETH", 00000000)
        #     upbit.sell_market_order("KRW-BTC", 00000000)
        #     time.sleep(api_call_interval)

        time.sleep(api_call_interval)

    except Exception as e:
        print(time.strftime('%m/%d %H:%M:%S'), "Exception: " + str(e))