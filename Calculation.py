import json
import os
import time
import BinanceController
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import talib
import numpy as np
import pandas as pd
from binance.client import Client
import statistics
import traceback
from NotificationCenter import debug, info, warning, error, critical


class CalculationClass:
    def __init__(self, binance_instance, user):
        self.binance_instance: BinanceController = binance_instance
        self.user = user

    def do_maxmin(self, dic):
        start = dic['buy_time'].strftime("%Y/%m/%d %H:%M")
        end = dic['sell_time'].strftime("%Y/%m/%d %H:%M")
        max_min = {
            'coin': dic['pair'],
            'price': dic['sell_coin'],
            'start': datetime.strptime(start, '%Y/%m/%d %H:%M'),
            'end': datetime.strptime(end, '%Y/%m/%d %H:%M')
        }
        return self.maxmin_auto(max_min)

    def maxmin_auto(self, dic):
        klines = self.binance_instance.coin_raw_1min(dic['coin'])
        openT = [self.binance_instance.deta_cul(i[0]) for i in klines]
        openX = [i[2] for i in klines]
        openN = [i[3] for i in klines]
        ST = openT.index(dic['start'])
        ED = openT.index(dic['end'])
        MAX1 = [openX[i] for i in range(ED) if ST <= i]
        MIN1 = [openN[i] for i in range(ED) if ST <= i]
        Time = [openT[i] for i in range(ED) if ST <= i]
        info = []
        maxA = max(MAX1)
        minA = min(MIN1)
        print("最大：", maxA, ",", (float(maxA) / float(dic['price']) - 1), "%,", Time[MAX1.index(maxA)])
        print("最小：", minA, ",", (1 - float(dic['price']) / float(minA)), "%,", Time[MIN1.index(minA)])
        info.extend(
            [maxA, minA, (float(maxA) / float(dic['price']) - 1), (1 - float(dic['price']) / float(minA)),
             Time[MAX1.index(maxA)],
             Time[MIN1.index(minA)]])
        return info

    # 時価総額計算（$）
    def cul_profit(self, dic):
        mylist = list(dic.keys())
        sum = 0
        for i in mylist:
            if i == "USDT":
                dol = dic[i]
            else:
                amount = dic[i]
                label = i + "USDT"
                dol = float(self.binance_instance.get_price(label)) * amount
            sum += dol
        return sum

    def set_chart_url(self, coin):
        recoin = coin.replace('USDT', '')
        url = "https://www.binance.com/ja/trade/" + recoin + "_USDT"
        debug("Binanceチャート" + url)
        return url

    def tax_cul(self, dic):
        BNBprice = dic['BNB'] * float(self.binance_instance.get_price("BNBUSDT"))
        debug("BNB" + str(BNBprice / self.cul_profit(dic) * 100) + "%全体保有")
        if BNBprice < self.cul_profit(dic) * 0.01:
            info("BNBが不足のため買い足します", self.user)
            return True
        return False

    # datetimeをstrに変換してjsonで使えるように
    def json_dumps(self, json_obj):
        def json_serial(obj):
            # 日付型の場合には、文字列に変換します
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            # 上記以外はサポート対象外
            raise TypeError("Type %s not serializable" % type(obj))

        return json.dumps(json_obj, default=json_serial)

    def plot_main(self, date, price, macd, macdsignal, macdhist, rsi14):
        fig = plt.figure()
        ax1 = fig.add_subplot(311, title='Price')
        ax2 = fig.add_subplot(312, title='MACD')
        ax3 = fig.add_subplot(313, title='RSI')
        ax1.set_xlim(date[-200], date[-1])
        ax2.set_xlim(date[-200], date[-1])
        ax3.set_xlim(date[-200], date[-1])
        ax1.axes.xaxis.set_visible(False)
        ax2.axes.xaxis.set_visible(False)
        plt.ion()
        ax1.plot(date, price, label="price")
        ax2.plot(date, macd, label="macd")
        ax2.plot(date, macdsignal, label="macdsignal")
        ax2.plot(date, macdhist, label="macdhist")
        ax3.plot(date, rsi14, label="rsi14")
        save_dir = '/image/'
        os.makedirs(save_dir, exist_ok=True)
        plt.savefig(save_dir + 'plot.png')
        plt.ioff()

    # 1:1min 2:5min 3:15min
    def cul_tec(self, coin, period):
        tec = {
            'coin': coin,
            'macdline': 0,
            'rsi14': 0,
            'wasOverbuy': False,
            'wasOversold': False,
            'crossover_buy': False,
            'crossover_sell': False,
            'detect_descent': False,
            'choice': False,
            'do_sell': False
        }
        RSISoldLevel = 30
        RSIBuyLevel = 70

        if period == 1:
            Price, Time = self.binance_instance.coin_tec_1min(coin)
        elif period == 2:
            Price, Time = self.binance_instance.coin_tec_5min(coin)
        else:
            Price, Time = self.binance_instance.coin_tec_15min(coin)

        items = pd.DataFrame({'Value': Price, 'Time': Time})

        # データをnumpy行列に変換する
        price = np.array(items['Value'], dtype='f8')
        macd, macdsignal, macdhist = talib.MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
        rsi14 = talib.RSI(price, timeperiod=14)
        tec['rsi14'] = rsi14[-1]

        macdline = macd - macdsignal
        tec['macdline'] = macdline[-1]

        if (rsi14[-1] <= RSISoldLevel or rsi14[-2] <= RSISoldLevel or rsi14[-3] <= RSISoldLevel or
                rsi14[-4] <= RSISoldLevel or rsi14[-5] <= RSISoldLevel or rsi14[-6] <= RSISoldLevel or
                rsi14[-7] <= RSISoldLevel or rsi14[-8] <= RSISoldLevel or rsi14[-9] <= RSISoldLevel):
            tec['wasOversold'] = True

        if rsi14[-1] >= RSIBuyLevel or rsi14[-2] >= RSIBuyLevel or rsi14[-3] >= RSIBuyLevel or rsi14[
            -4] >= RSIBuyLevel or rsi14[-5] >= RSIBuyLevel or rsi14[-6] >= RSIBuyLevel:
            tec['wasOverbuy'] = True

        if macdhist[-1] >= 0 and macdline[-1] > 0 and macdline[-2] < 0:
            tec['crossover_buy'] = True

        if macdhist[-1] <= 0 and macdline[-1] < 0 and macdline[-2] > 0:
            tec['crossover_sell'] = True

        if tec['wasOversold'] and tec['crossover_buy']:
            tec['choice'] = True

        if macdhist[-1] <= 0 and macdline[-1] < 0:
            tec['detect_descent'] = True

        if tec['wasOverbuy'] and tec['crossover_sell']:
            tec['do_sell'] = True

        return tec

    def check_1minute(self, usecoin):
        while True:
            try:
                klines = self.binance_instance.client.get_klines(symbol=usecoin, interval=Client.KLINE_INTERVAL_1MINUTE)
                NumberOfTrades = [i[8] for i in klines]
                return statistics.mean(NumberOfTrades)
            except Exception as e:
                debug(str(e))

    def prepare_log_data_set(self, data, user):
        raw_data = []

        if user == 0:
            # date_insert
            buy_date = str(data['buy_time'])
            buy_date_list = buy_date.split(' ')

            sell_date = str(data['sell_time'])
            sell_date_list = sell_date.split(' ')

            raw_data.extend([buy_date_list[0], buy_date_list[1], sell_date_list[0], sell_date_list[1]])
            raw_data.extend(
                [data['pair'], data['buy_coin'], data['sell_coin'], data['buy_mode'], data['mode']])

        else:
            # date_insert
            buy_date = str(data['buy_time'])
            buy_date_list = buy_date.split(' ')

            sell_date = str(data['sell_time'])
            sell_date_list = sell_date.split(' ')

            raw_data.extend([buy_date_list[0], buy_date_list[1], sell_date_list[0], sell_date_list[1]])
            raw_data.extend(
                [data['pair'], data['buy_coin'], data['sell_coin'], data['amount'],
                 data['profit'] * self.binance_instance.get_USDJPY(), data['mode']])

        max_and_min = self.do_maxmin(data)
        print(max_and_min)
        if data['buy_coin'] <= data['sell_coin']:
            percent = (float(data['sell_coin']) / float(data['buy_coin']) - 1)
            raw_data.append(percent)
        else:
            percent = (1 - float(data['buy_coin']) / float(data['sell_coin']))
            raw_data.append(percent)
        for j in max_and_min:
            if isinstance(j, type(max_and_min[-1])):
                raw_data.append(str(j))
            else:
                raw_data.append(j)

        return raw_data

    # 売るためのalgorithm計算
    def sell_algorithm(self, dict):
        dict['price'] = self.binance_instance.get_price(dict['pair'])
        if float(dict['buy_coin']) * 0.97 >= float(dict['price']):
            dict['win'] = False
            dict['loss'] = True
        elif float(dict['buy_coin']) * 1.03 <= float(dict['price']):
            dict['win'] = True
            dict['loss'] = False
        else:
            dict['win'] = False
            dict['loss'] = False
        return dict


if __name__ == "__main__":
    Cal = CalculationClass(.3)
    print(Cal.check_1minute('BTCUSDT'))
