import json
import os
import time
import BinanceController
from datetime import date, datetime, timedelta
import NotificationCenter
import matplotlib.pyplot as plt


class CalculationClass:
    def __init__(self, binance_instance, user):
        self.binance_instance: BinanceController = binance_instance
        self.user = user
        self.notify = NotificationCenter.NotificationCenterClass("CalculationClass")

    def maxmin_auto(self, coin, Start, End, Price):
        klines = self.binance_instance.coin_raw_1min(coin)
        openT = [self.binance_instance.deta_cul(i[0]) for i in klines]
        openX = [i[2] for i in klines]
        openN = [i[3] for i in klines]
        ST = openT.index(Start)
        ED = openT.index(End)
        MAX1 = [openX[i] for i in range(ED) if ST <= i]
        MIN1 = [openN[i] for i in range(ED) if ST <= i]
        Time = [openT[i] for i in range(ED) if ST <= i]
        info = []
        maxA = max(MAX1)
        minA = min(MIN1)
        print("最大：", maxA, ",", (float(maxA) / float(Price) - 1), "%,", Time[MAX1.index(maxA)])
        print("最小：", minA, ",", (1 - float(Price) / float(minA)), "%,", Time[MIN1.index(minA)])
        info.extend(
            [maxA, minA, (float(maxA) / float(Price) - 1), (1 - float(Price) / float(minA)), Time[MAX1.index(maxA)],
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
        self.notify.debug("Binanceチャート" + url)
        return url

    def tax_cul(self, dic):
        BNBprice = dic['BNB'] * float(self.binance_instance.get_price("BNBUSDT"))
        self.notify.debug("BNB" + str(BNBprice / self.cul_profit(dic) * 100) + "%全体保有")
        if BNBprice < self.cul_profit(dic) * 0.01:
            self.notify.info("BNBが不足のため買い足します", self.user)
            return True
        return False

    def do_maxmin(self, dic):
        time = dic['dt_now'].strftime("%Y/%m/%d %H:%M")
        max_min = {
            'coin': dic['usecoin'],
            'price': dic['price'],
            'start': datetime.strptime(time, '%Y/%m/%d %H:%M'),
            'end': None
        }
        return max_min

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

    def check_deadline(self):
        while True:
            r = gspread1.txt_readlist()
            notuse, coinlist = gspread1.coin_read()
            reslist = []
            tmp = {}
            paycoin = gspread1.usedpay_read()
            print("------------------------------")
            if r:
                for j, k in r.items():
                    dead = k + timedelta(hours=1)
                    now = datetime.now()
                    dicc = searchcoin.cul_tec(j)
                    if j == paycoin:
                        print("前回に決済に使われた通貨")
                    elif dead < now or dicc["crossoversell"] and not dicc["crossoverbuy"]:
                        if dicc["crossoversell"]:
                            print("下降トレンド", j)
                        if dead < now:
                            print("期限切れ", j)

                    else:
                        tmp[j] = k

            for i in coinlist:
                dicc = searchcoin.cul_tec(i)
                if i == paycoin:
                    print("追加無し", i)
                elif dicc["crossoversell"] and not dicc["crossoverbuy"]:
                    print("下降トレンドのため追加無し:", i)
                elif gspread1.time_read() + timedelta(hours=1) < datetime.now():
                    print("監視中通貨なし")
                else:
                    if len(tmp) < 8:
                        print(dicc)
                        tmp[i] = gspread1.time_read()
                        print("追加された通貨:", i)
                time.sleep(3)
            gspread1.txt_writelist(tmp)
            for a in tmp.keys():
                reslist.append(a)
            if reslist:
                return reslist
            time.sleep(5)

if __name__ == "__main__":
    print("")
