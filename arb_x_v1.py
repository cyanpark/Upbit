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
chat_id = 0000000000

api_call_interval = 2

###############################################################################
# method
def send_msg(text_msg):
    bot = telegram.Bot(token = token)
    asyncio.run(bot.send_message(chat_id = chat_id, text = text_msg))

def get_avg_price_market_order(ob, side, size, size_type):
    if size_type == "ticker":
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
    
    else:
        if side == "ask":
            cum_ask_price = 0
            cum_ask_size = 0
            cum_ask_cnt = 0
            for ob_unit in ob['orderbook_units']:
                cum_ask_price = cum_ask_price + float(ob_unit['ask_price'])
                cum_ask_size = cum_ask_size + (float(ob_unit['ask_price']) * float(ob_unit['ask_size']))
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
                cum_bid_size = cum_bid_size + (float(ob_unit['ask_price']) * float(ob_unit['ask_size']))
                cum_bid_cnt = cum_bid_cnt + 1
                
                if cum_bid_size < size:
                    break

            avg_price = cum_bid_price / cum_bid_cnt

    return avg_price
###############################################################################
# Execution
Fee_KRW = 0.0005
Fee_BTC = 0.0025

TCKs = ["ETH", "SOL", "XRP", "ADA"]

AVL_KRW = 1000000

# for TCK in TCKs:
#     print(f"\nTICKER: {TCK}")
#     ob_BTC_KRW = pyupbit.get_orderbook("KRW-BTC")
#     ob_TCK_KRW = pyupbit.get_orderbook("KRW-"+TCK)
#     ob_TCK_BTC = pyupbit.get_orderbook("BTC-"+TCK)

#     BTC_vol = AVL_KRW * (1-Fee_KRW) / get_avg_price_market_order(ob_BTC_KRW, "ask", AVL_KRW, "market")
#     TCK_vol = BTC_vol * (1-Fee_BTC) / get_avg_price_market_order(ob_TCK_BTC, "ask", BTC_vol * (1-Fee_BTC), "market")
#     KRW_vol = TCK_vol * (1-Fee_KRW) * get_avg_price_market_order(ob_TCK_KRW, "bid", TCK_vol * (1-Fee_KRW), "ticker")
#     print(f"\nBTC > BTC-{TCK} > {TCK}:", KRW_vol)
#     print(f"BTC_KRW_buy_avgp:", get_avg_price_market_order(ob_BTC_KRW, "ask", AVL_KRW, "market"))
#     print(f"{TCK}_BTC_buy_avgp:", get_avg_price_market_order(ob_TCK_BTC, "ask", BTC_vol * (1-Fee_BTC), "market"))
#     print(f"{TCK}_KRW_sel_avgp:", get_avg_price_market_order(ob_TCK_KRW, "bid", TCK_vol * (1-Fee_KRW), "ticker"))

#     TCK_vol = AVL_KRW * (1-Fee_KRW) / get_avg_price_market_order(ob_TCK_KRW, "ask", AVL_KRW, "market")
#     BTC_vol = TCK_vol * (1-Fee_BTC) * get_avg_price_market_order(ob_TCK_BTC, "bid", TCK_vol * (1-Fee_BTC), "ticker")
#     KRW_vol = BTC_vol * (1-Fee_KRW) * get_avg_price_market_order(ob_BTC_KRW, "bid", BTC_vol * (1-Fee_KRW), "ticker")
#     print(f"\n{TCK} > BTC-{TCK} > BTC:", KRW_vol)
#     print(f"{TCK}_KRW_buy_avgp:", get_avg_price_market_order(ob_TCK_KRW, "ask", AVL_KRW, "market"))
#     print(f"{TCK}_BTC_sel_avgp:", get_avg_price_market_order(ob_TCK_BTC, "bid", TCK_vol * (1-Fee_BTC), "ticker"))
#     print(f"BTC_KRW_sel_avgp:", get_avg_price_market_order(ob_BTC_KRW, "bid", BTC_vol * (1-Fee_KRW), "ticker"))
#     time.sleep(api_call_interval)
#     input("Please press the Enter key to proceed")

# Loop
while True:
    try:
        for TCK in TCKs:
            ob_BTC_KRW = pyupbit.get_orderbook("KRW-BTC")
            ob_TCK_KRW = pyupbit.get_orderbook("KRW-"+TCK)
            ob_TCK_BTC = pyupbit.get_orderbook("BTC-"+TCK)

            # CASE-1 : BTC/KRW > ETH/BTC > ETH/KRW
            BTC_KRW_buy_avgp = get_avg_price_market_order(ob_BTC_KRW, "ask", AVL_KRW, "market")
            BTC_vol = AVL_KRW * (1-Fee_KRW) / BTC_KRW_buy_avgp
            TCK_BTC_buy_avgp = get_avg_price_market_order(ob_TCK_BTC, "ask", BTC_vol * (1-Fee_BTC), "market")
            TCK_vol = BTC_vol * (1-Fee_BTC) / TCK_BTC_buy_avgp
            TCK_KRW_sel_avgp = get_avg_price_market_order(ob_TCK_KRW, "bid", TCK_vol * (1-Fee_KRW), "ticker")
            KRW_vol = TCK_vol * (1-Fee_KRW) * TCK_KRW_sel_avgp
            
            if KRW_vol > AVL_KRW:
                send_msg(f"CASE-1: BTC > BTC-{TCK} > {TCK}" + 
                         f"\nBTC_KRW_buy_avgp: " + str(round(BTC_KRW_buy_avgp,0)) +
                         f"\n{TCK}_BTC_buy_avgp: " + str(round(TCK_BTC_buy_avgp, 8)) +
                         f"\n{TCK}_KRW_sel_avgp: " + str(TCK_KRW_sel_avgp) +
                         f"\nFinal_KRW: " + str(KRW_vol))

            # CASE-2 : ETH/KRW > EHT/BTC > BTC/KRW
            TCK_KRW_buy_avgp = get_avg_price_market_order(ob_TCK_KRW, "ask", AVL_KRW, "market")
            TCK_vol = AVL_KRW * (1-Fee_KRW) / TCK_KRW_buy_avgp
            TCK_BTC_sel_avgp = get_avg_price_market_order(ob_TCK_BTC, "bid", TCK_vol * (1-Fee_BTC), "ticker")
            BTC_vol = TCK_vol * (1-Fee_BTC) * TCK_BTC_sel_avgp
            BTC_KRW_sel_avgp = get_avg_price_market_order(ob_BTC_KRW, "bid", BTC_vol * (1-Fee_KRW), "ticker")
            KRW_vol = BTC_vol * (1-Fee_KRW) * BTC_KRW_sel_avgp
            
            if KRW_vol > AVL_KRW:
                send_msg(f"CASE-2: {TCK} > BTC-{TCK} > BTC" + 
                         f"\n{TCK}_KRW_buy_avgp: " + str(TCK_KRW_buy_avgp) +
                         f"\n{TCK}_BTC_sel_avgp: " + str(round(TCK_BTC_sel_avgp,8)) +
                         f"\nBTC_KRW_sel_avgp: " + str(round(BTC_KRW_sel_avgp,0)) +
                         f"\nFinal_KRW: " + str(KRW_vol))
            
            time.sleep(api_call_interval)
            input("Please press the Enter key to proceed")

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

    except Exception as e:
        send_msg("Exception: " + str(e))
        # print("Exception: " + str(e))