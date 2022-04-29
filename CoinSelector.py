import BinanceController
import time
import Calculation
from datetime import datetime
from NotificationCenter import debug, info, warning, error, critical
import traceback
import sys


class CoinSelectorClass:
    def __init__(self):
        self.binance_instance = BinanceController.BinanceControllerClass("", "", 3)
        self.calculation = Calculation.CalculationClass(self.binance_instance, 3)
        self.selected_coin = {}
        self.update_time = None

    def get_selected_coin(self):
        return self.selected_coin

    def get_update_time(self):
        return self.update_time

    def coin_selector(self):
        while True:
            prices = self.binance_instance.get_ticker()
            tmp = [i['symbol'] for i in prices if
                   i['symbol'].endswith('USDT') and 'DOWN' not in i['symbol'] and 'UP' not in i['symbol'] and float(
                       i['price']) <= 100 and not i['symbol'].startswith('USD')]
            choice = []
            # up = 0
            # down = 0
            for i in tmp:
                try:
                    dic = self.calculation.cul_tec(i, 3)
                    # debug(str(i) + str(dic))
                    if dic['choice']:
                        choice.append(i)
                except Exception as e:
                    debug(str(e))
                time.sleep(0.5)

            if choice:
                # debug(str(choice))
                decision = [self.calculation.check_1minute(i) for i in choice if
                            float(self.calculation.check_1minute(i)) >= 20]
                res = [i for i in choice if float(self.calculation.check_1minute(i)) >= 20]
                if res:
                    debug(str(decision))
                    debug(str(res))
                    dic = {key: val for key, val in zip(res, decision)}
                    sorted_dic = sorted(dic.items(), key=lambda x: -x[1])
                    self.update_time = datetime.now()
                    self.selected_coin = dict(sorted_dic)
                    debug(str(self.selected_coin))
                    debug(str(self.update_time))
                else:
                    debug("[coin_selector]" + "15分足上昇コイン検出なし")
            else:
                debug("[coin_selector]" + "15分足上昇コイン検出なし")

    def coin_selector_MACD_RSI(self, period):
        if period not in [1, 5, 15, 30, 60]:
            sys.exit()
        while True:
            if datetime.now().minute % period == 0:
                print("in")
                prices = self.binance_instance.get_ticker()
                tmp = [i['symbol'] for i in prices if
                       i['symbol'].endswith('USDT') and 'DOWN' not in i['symbol'] and 'UP' not in i['symbol'] and float(
                           i['price']) <= 100 and not i['symbol'].startswith('USD')]
                choice = []
                # up = 0
                # down = 0
                for i in tmp:
                    try:
                        dic = self.calculation.cul_tec(i, 3)
                        # debug(str(i) + str(dic))
                        if dic['choice']:
                            choice.append(i)
                    except Exception as e:
                        debug(str(e))
                    time.sleep(0.5)

                if choice:
                    # debug(str(choice))
                    decision = [self.calculation.check_1minute(i) for i in choice if
                                float(self.calculation.check_1minute(i)) >= 20]
                    res = [i for i in choice if float(self.calculation.check_1minute(i)) >= 20]
                    if res:
                        debug(str(decision))
                        debug(str(res))
                        dic = {key: val for key, val in zip(res, decision)}
                        sorted_dic = sorted(dic.items(), key=lambda x: -x[1])
                        self.update_time = datetime.now()
                        self.selected_coin = dict(sorted_dic)
                        debug(str(self.selected_coin))
                        debug(str(self.update_time))
                    else:
                        debug("[coin_selector]" + "15分足上昇コイン検出なし")
                else:
                    debug("[coin_selector]" + "15分足上昇コイン検出なし")


if __name__ == "__main__":
    Cal = CoinSelectorClass()
    Cal.coin_selector_MACD_RSI(1)
