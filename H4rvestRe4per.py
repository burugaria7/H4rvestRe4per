import subprocess

import BinanceController
import Calculation
import NotificationCenter
import ScrapingManager
import schedule
import time
import threading
import SheetController
import CacheManager as Cache
import CoinSelector
from datetime import date, datetime, timedelta


class H4rvestRe4perClass:
    position = False

    buy = 0.0
    sell = 0.0

    def __init__(self):
        self.account = {'1': {'api_key': "PDzV1ux2fLL0p0Ivs8KGk3PcxAXO5GJKYpsq0e5bI2TAjEKcBJJLr99iAty1GuPB",
                              'api_secret': "cYw3QPuWeah57wEn2ll1T7g5udOXVTmoBZP43mq4CEq2GTUWUW9yK9YTOnsrEEyi"
                              },
                        '2': {'api_key': "AzI7xoktKczaf6Ja6XIcVKmfiiIan3zdnrOYvBciTLzdTHzgCpIPqtpKMisdmkjZ",
                              'api_secret': "JHS2qqgDWWFSBBZNCLWgExEW78lwkCfjBIUW6Z5nT3Yxoubsc4rVNpTicWRIwKq3"
                              }}
        self.binance_instance = BinanceController.BinanceControllerClass('', '', 3)
        self.binance_instance_1 = BinanceController.BinanceControllerClass(self.account['1']['api_key'],
                                                                           self.account['1']['api_secret'], 1)
        self.binance_instance_2 = BinanceController.BinanceControllerClass(self.account['2']['api_key'],
                                                                           self.account['2']['api_secret'], 2)
        self.Calculation_instance = Calculation.CalculationClass(self.binance_instance, 3)
        self.Calculation_instance_1 = Calculation.CalculationClass(self.binance_instance_1, 1)
        self.Calculation_instance_2 = Calculation.CalculationClass(self.binance_instance_2, 2)
        self.ScrapingManager_instance_1 = Calculation.CalculationClass(self.binance_instance_1, 1)
        self.ScrapingManager_instance_2 = Calculation.CalculationClass(self.binance_instance_2, 2)
        self.notify = NotificationCenter.NotificationCenterClass("MainClass")
        self.scr = ScrapingManager.ScrapingManagerClass()
        self.sheet = SheetController.SheetControllerClass()
        self.selector = CoinSelector.CoinSelectorClass()
        self.coin_buffer = {}
        self.observe_que = Cache.get_monitoring_currency_cache()
        # 一回認識したら最低限監視する期間
        self.OBSERVE_TIME = timedelta(hours=1)
        # 監視するコインペアの上限値
        self.MAX_OBSERVE = 8
        # Falseで初期化することでそのAPIを使わない設定にできるよ☆
        self.available_api1 = True
        self.available_api2 = True

        self.notify.debug("[__init__]"+"Windowsの時刻を同期します")
        subprocess.run(['sync_date_time.bat'], stdout=subprocess.PIPE)
        time.sleep(3)

        self.notify.debug("[__init__]"+"coin_selectorスレッドを起動します")
        thread_selector = threading.Thread(target=self.selector.coin_selector)
        thread_selector.start()

        # ポジションを持っていたら売却スレッドをたてる
        for i in self.account:
            Dic = Cache.get_position_cache(int(i))
            if Dic['status']:
                # 未決済ポジションがあるため、売却スレッドを建てる
                self.notify.debug("[__init__]"+"未決済ポジションがあるため、売却スレッドを建てます" + str(i))
                thread_sell = threading.Thread(target=self.sell_bot, args=(i,))
                thread_sell.start()

        self.notify.debug("[__init__]"+"search_botスレッドを起動します")
        thread_search = threading.Thread(target=self.search_bot)
        thread_search.start()

    def search_bot(self):
        self.notify.debug("[search_bot]起動！")
        while True:
            tmp = {}
            if self.observe_que:
                # self.observe_que内の個数が変わってしまうためにitem()で回避している
                for i, j in self.observe_que.items():
                    dicc = self.Calculation_instance.cul_tec(i, 3)
                    if j < datetime.now() or dicc['detect_descent']:
                        if j < datetime.now():
                            self.notify.debug("[search_bot]"+str(i)+"を監視から外します(期限切れ)")
                        elif dicc['detect_descent']:
                            self.notify.debug("[search_bot]"+str(i)+"を監視から外します(下降トレンド)")
                    else:
                        tmp[i] = j
            self.observe_que = tmp
            # なんかコイン認識したら = なんか新しく認識したら回る
            if self.selector.get_selected_coin().keys() != self.observe_que.keys():
                self.coin_buffer = self.selector.get_selected_coin()
                for i in self.coin_buffer:
                    # 監視してるコインが上限値超えてたら、一旦休憩
                    if len(self.observe_que) > self.MAX_OBSERVE:
                        break
                    dicc = self.Calculation_instance.cul_tec(i, 3)
                    if dicc['detect_descent']:
                        self.notify.debug("[search_bot]"+str(i) + "を監視から外します(下降トレンド)")
                    elif self.selector.get_update_time() < datetime.now():
                        self.notify.debug("[search_bot]"+str(i) + "を監視から外します(期限切れ)")
                    elif i not in self.observe_que:
                        self.notify.debug("[search_bot]"+str(i) + "を監視キューに追加しスレッドを起動")
                        self.notify.debug(str(self.observe_que))
                        self.observe_que[i] = datetime.now() + self.OBSERVE_TIME
                        thread_observer = threading.Thread(target=self.coin_observer, args=(i,))
                        thread_observer.start()
                        # 　監視スレッド起動
                    time.sleep(0.5)
                Cache.set_monitoring_currency_cache(self.observe_que)
            time.sleep(1)

    def coin_observer(self, pair):
        self.notify.debug("[coin_observer, pair= " + str(pair) + "]起動！")
        while self.available_api1 or self.available_api2 and pair in self.observe_que:
            Tec = self.Calculation_instance.cul_tec(pair, 1)
            # self.notify.debug("[coin_observer]"+str(Tec))
            dict = {
                'user': 0,
                'status': False,
                'pair': pair,
                'amount': 0,
                'buy_time': None,
                'sell_time': None,
                'buy_coin': 0,
                'sell_coin': 0,
                'profit': 0,
                'mode': 0,
            }
            if Tec['choice']:
                self.notify.debug("[coin_observer]"+"買い処理をします")
                if self.available_api1:
                    dict['amount'] = self.binance_instance_1.buy_all(pair)
                    dict['buy_coin'] = self.binance_instance_1.get_price(pair)
                    dict['status'] = True
                    dict['user'] = 1
                    dict['buy_time'] = datetime.now()
                    Cache.set_position_cache(1, dict)
                    self.available_api1 = False
                    del self.observe_que[pair]
                    self.notify.debug("[coin_observer]"+"買い処理成功！")
                    self.sell_bot(1)
                elif self.available_api2:
                    dict['amount'] = self.binance_instance_2.buy_all(pair)
                    dict['buy_coin'] = self.binance_instance_2.get_price(pair)
                    dict['status'] = True
                    dict['user'] = 2
                    dict['buy_time'] = datetime.now()
                    Cache.set_position_cache(2, dict)
                    self.available_api2 = False
                    del self.observe_que[pair]
                    self.notify.debug("[coin_observer]"+"買い処理成功！")
                    self.sell_bot(2)
                return
            time.sleep(10)

    def sell_bot(self, user):
        self.notify.debug("[sell_bot, user= " + str(user) + "]起動！")
        while not self.available_api1 or not self.available_api2:
            dict = Cache.get_position_cache(user)
            Tec = self.Calculation_instance.cul_tec(dict['pair'], 1)
            if Tec['do_sell']:
                if user == 1:
                    dict['sell_coin'] = self.binance_instance_1.get_price(dict['pair'])
                    dict['status'] = False
                    dict['sell_time'] = datetime.now()
                    dict['profit'] = self.binance_instance_1.get_balance()
                    self.binance_instance_1.sell_all(dict['pair'])
                    self.available_api1 = True
                elif user == 2:
                    dict['sell_coin'] = self.binance_instance_2.get_price(dict['pair'])
                    dict['status'] = False
                    dict['sell_time'] = datetime.now()
                    dict['profit'] = self.binance_instance_2.get_balance()
                    self.binance_instance_2.sell_all(dict['pair'])
                    self.available_api1 = True
                self.sheet.post_log(user, self.Calculation_instance.prepare_log_data_set(dict))
                return
            time.sleep(10)


if __name__ == "__main__":
    hr = H4rvestRe4perClass()
    hr.coin_observer('XEMUSDT')
