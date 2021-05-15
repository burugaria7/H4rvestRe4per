import subprocess

import BinanceController
import Calculation
import ScrapingManager
import schedule
import time
import threading
import SheetController
import CloudCacheManager as Cache
import CoinSelector
import DiscordStatus
from datetime import date, datetime, timedelta
from NotificationCenter import debug, info, warning, error, critical


class H4rvestRe4perClass:
    position = False

    buy = 0.0
    sell = 0.0

    def __init__(self):
        self.account = {'api_key': "AzI7xoktKczaf6Ja6XIcVKmfiiIan3zdnrOYvBciTLzdTHzgCpIPqtpKMisdmkjZ",
                        'api_secret': "JHS2qqgDWWFSBBZNCLWgExEW78lwkCfjBIUW6Z5nT3Yxoubsc4rVNpTicWRIwKq3"
                        }
        self.binance_instance = BinanceController.BinanceControllerClass('', '', 3)
        self.binance_instance_1 = BinanceController.BinanceControllerClass(self.account['api_key'],
                                                                           self.account['api_secret'], 2)
        self.Calculation_instance = Calculation.CalculationClass(self.binance_instance, 3)
        self.Calculation_instance_1 = Calculation.CalculationClass(self.binance_instance_1, 2)
        self.scraping = ScrapingManager.ScrapingManagerClass()
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

        self.discord_status_instance = DiscordStatus.DiscordStatusClass()

        print(self.binance_instance_1.get_USDJPY())
        print(self.binance_instance_1.get_balance())
        print(self.Calculation_instance.cul_profit(
            self.binance_instance_1.get_balance()) * self.binance_instance_1.get_USDJPY())

        debug("[__init__]" + "Windowsの時刻を同期します")
        subprocess.run(['sync_date_time.bat'], stdout=subprocess.PIPE)
        time.sleep(3)

        debug("[__init__]" + "coin_selectorスレッドを起動します")
        thread_selector = threading.Thread(target=self.selector.coin_selector)
        thread_selector.start()

        # ポジションを持っていたら売却スレッドをたてる
        Dic = Cache.get_position_cache()
        if Dic['status']:
            self.available_api1 = False
            # 未決済ポジションがあるため、売却スレッドを建てる
            debug("[__init__]" + "未決済ポジションがあるため、売却スレッドを建てます" + str(1))
            self.discord_status_instance.set_status(Dic['pair'])
            thread_sell = threading.Thread(target=self.sell_bot, args=(1,))
            self.discord_status_instance.set_status("Observing")
            thread_sell.start()

        debug("[__init__]" + "search_botスレッドを起動します")
        thread_search = threading.Thread(target=self.search_bot)
        thread_search.start()

    def search_bot(self):
        debug("[search_bot]起動！")
        while True:
            tmp = {}
            if self.observe_que:
                # self.observe_que内の個数が変わってしまうためにitem()で回避している
                for i, j in list(self.observe_que.items()):
                    dicc = self.Calculation_instance.cul_tec(i, 3)
                    if j < datetime.now() or dicc['detect_descent']:
                        if j < datetime.now():
                            debug("[search_bot]" + str(i) + "を監視から外します(期限切れ)")
                        elif dicc['detect_descent']:
                            debug("[search_bot]" + str(i) + "を監視から外します(下降トレンド)")
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
                        debug("[search_bot]" + str(i) + "を監視から外します(下降トレンド)")
                    elif self.selector.get_update_time() + self.OBSERVE_TIME < datetime.now():
                        debug("[search_bot]" + str(i) + "を監視から外します(期限切れ)")
                    elif i not in self.observe_que:
                        debug("[search_bot]" + str(i) + "を監視キューに追加しスレッドを起動")
                        debug(str(self.observe_que))
                        self.observe_que[i] = datetime.now() + self.OBSERVE_TIME
                        thread_observer = threading.Thread(target=self.coin_observer, args=(i,))
                        thread_observer.start()
                        # 　監視スレッド起動
                    time.sleep(0.5)
                Cache.set_monitoring_currency_cache(self.observe_que)
            time.sleep(5)

    def coin_observer(self, pair):
        debug("[coin_observer, pair= " + str(pair) + "]起動！")
        while self.available_api1 and pair in self.observe_que:
            Tec = self.Calculation_instance.cul_tec(pair, 1)
            # debug("[coin_observer]"+str(Tec))
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
            # if Tec['choice'] and self.scraping.cul_trend_from_tradingview(1,
            #                                                               pair) and self.scraping.cul_trend_from_tradingview(
            #     2, pair):
            # if Tec['choice']:
            if Tec['crossover_buy']:
                debug("[coin_observer]" + "買い処理をします")
                if self.available_api1:
                    dict['amount'] = '6666666'
                    # dict['amount'] = self.binance_instance_2.buy_all(pair)
                    dict['buy_coin'] = self.binance_instance_1.get_price(pair)
                    dict['status'] = True
                    dict['user'] = 2
                    dict['buy_time'] = datetime.now()
                    Cache.set_position_cache(dict)
                    self.available_api1 = False
                    del self.observe_que[pair]
                    info("買いました", 2)
                    info(str(dict), 2)
                    debug("[coin_observer]" + "買い処理成功！（２）")
                    self.discord_status_instance.set_status(pair)
                    self.sell_bot(2)
                return
            time.sleep(10)

    def sell_bot(self, user):
        user = int(user)
        debug("[sell_bot, user= " + str(user) + "]起動！")
        while not self.available_api1:
            dict = Cache.get_position_cache()
            sell_algorithm = self.Calculation_instance.sell_algorithm(dict)
            Tec_1min = self.Calculation_instance.cul_tec(dict['pair'], 1)
            Tec_15min = self.Calculation_instance.cul_tec(dict['pair'], 3)
            if Tec_15min['detect_descent'] or Tec_1min['do_sell'] or sell_algorithm['win'] or sell_algorithm['loss']:
                debug("[sell_bot]" + "売り処理をします")

                if Tec_15min['detect_descent']:
                    dict['mode'] = 1
                    info("15分足売り時検知（MACD）", user)
                elif sell_algorithm['win']:
                    dict['mode'] = 2
                    info("利確検知（+3%）", user)
                elif sell_algorithm['loss']:
                    dict['mode'] = 3
                    info("ロスカット検知（-3%）", user)
                elif Tec_1min['do_sell']:
                    dict['mode'] = 4
                    info("1分足売り時検知（MACD+RSI）", user)

                dict['sell_coin'] = self.binance_instance_1.get_price(dict['pair'])
                dict['status'] = False
                dict['sell_time'] = datetime.now()
                dict['profit'] = self.Calculation_instance.cul_profit(self.binance_instance_1.get_balance())
                # self.binance_instance_1.sell_all(dict['pair'])
                info("売りました", 2)
                info(str(dict), 2)
                debug("[sell_bot]" + "売り処理成功！（１）")
                self.available_api1 = True
                Cache.set_position_cache(dict)
                self.sheet.post_log(user, self.Calculation_instance.prepare_log_data_set(dict))
                self.discord_status_instance.set_status("Observing")
                return
            time.sleep(5)


if __name__ == "__main__":
    hr = H4rvestRe4perClass()
