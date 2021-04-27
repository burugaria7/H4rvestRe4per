from binance.client import Client
from datetime import datetime
import ccxt
from bs4 import BeautifulSoup
import urllib.request as req
import NotificationCenter
import time


class BinanceControllerClass:
    def __init__(self, api_key, api_secret, user):
        self.api_key = api_key
        self.api_secret = api_secret
        self.user = user
        self.client = Client(api_key, api_secret)
        self.CCXT_binance = ccxt.binance({'apiKey': str(api_key), 'secret': str(api_secret), })
        self.notify = NotificationCenter.NotificationCenterClass("BinanceControllerClass")

    def get_price(self, coin):
        info = self.client.get_recent_trades(symbol=coin)
        coin = info[-1]['price']
        print("現在の価格:", coin)
        return coin

    def get_ticker(self):
        while True:
            try:
                prices = self.client.get_all_tickers()
                return prices
            except Exception as e:
                self.notify.debug(e)
                time.sleep(1)
                pass

    def get_balance(self):
        bi_balance = self.CCXT_binance.fetchBalance()
        dic = bi_balance['total']
        tmp = {}
        for key, value in dic.items():
            if value != 0:
                tmp[key] = value
        return tmp

    def buy_all(self, coin):
        while True:
            try:
                dic = self.get_balance()
                qat = int(dic['USDT'] / float(self.get_price(coin)))
                order = self.client.order_market_buy(symbol=coin, quantity=qat)
                self.notify.debug("[buy_all]"+order["symbol"])
                self.notify.debug("[buy_all]"+order["side"])
                self.notify.debug("[buy_all]"+"量：" + order["origQty"])
                return order["origQty"]
            except Exception as e:
                self.notify.critical(e, self.user)
                time.sleep(1)
                pass

    def sell_all(self, coin):
        while True:
            try:
                dic = self.get_balance()
                qat = int(dic[coin.replace('USDT', '')])
                order = self.client.order_market_sell(symbol=coin, quantity=qat)
                self.notify.debug("[sell_all]" + order["symbol"])
                self.notify.debug("[sell_all]" + order["side"])
                self.notify.debug("[sell_all]" + "量：" + order["origQty"])
                return order["origQty"]
            except Exception as e:
                self.notify.critical(e, self.user)
                time.sleep(1)
                pass

    def buy_piece(self, coin, qat):
        while True:
            try:
                order = self.client.order_market_buy(symbol=coin, quantity=qat)
                print(order["symbol"])
                print(order["side"])
                print("量：" + order["origQty"])
            except Exception as e:
                self.notify.critical(e, self.user)
                time.sleep(1)
                pass

    def sell_piece(self, coin, qat):
        while True:
            try:
                order = self.client.order_market_sell(symbol=coin, quantity=qat)
                print(order["symbol"])
                print(order["side"])
                print("量：" + order["origQty"])
            except Exception as e:
                self.notify.critical(e, self.user)
                time.sleep(1)
                pass

    # 取得配列の内訳
    # [OpenTime,Open,High,Low,Close,Volume,CloseTime,QuoteAssetVolume,NumberOfTrades,TakerBuyBaseAssetVolume,TakerBuyQuoteAssetVolume,Ignore]
    def coin_tec_1min(self, coin):
        klines = self.client.get_klines(symbol=coin, interval=Client.KLINE_INTERVAL_1MINUTE)
        openP = [i[1] for i in klines]
        openT = [self.deta_cul(i[0]) for i in klines]
        return openP, openT

    def coin_tec_15min(self, coin):
        klines = self.client.get_klines(symbol=coin, interval=Client.KLINE_INTERVAL_15MINUTE)
        openP = [i[1] for i in klines]
        openT = [self.deta_cul(i[0]) for i in klines]
        return openP, openT

    def coin_raw_1min(self, coin):
        klines = self.client.get_historical_klines(coin, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
        return klines

    def deta_cul(self, servertime):  # サーバータイムを日付に変換する
        time = float(servertime) / 1000
        dt = datetime.fromtimestamp(time)
        return dt

    def time_cul(self, date):  # 日付をサーバータイムに変換する
        time = date.timestamp() * 1000
        return time

    def get_USDJPY(self):
        url = "https://info.finance.yahoo.co.jp/fx/detail/?code=USDJPY=FX"
        res = req.urlopen(url)
        soup = BeautifulSoup(res, 'html.parser');
        values = soup.select_one("#USDJPY_detail_bid").findAll(text=True)
        current_value = float(''.join(values))
        return current_value
