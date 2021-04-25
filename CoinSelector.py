import BinanceController
import time
import Calculation
import NotificationCenter


class CoinSelectorClass:
    def __init__(self):
        self.binance_instance = BinanceController.BinanceControllerClass("",
                                                                         "", 3)
        self.calculation = Calculation.CalculationClass(self.binance_instance, 3)
        self.notify = NotificationCenter.NotificationCenterClass("CoinSelectorClass")
        self.selected_coin = {}

    def get_selected_coin(self):
        return self.selected_coin

    def coin_selector(self):
        while True:
            prices = self.binance_instance.get_ticker()
            tmp = [i['symbol'] for i in prices if
                   'USDT' in i['symbol'] and 'DOWN' not in i['symbol'] and 'UP' not in i['symbol'] and float(
                       i['price']) <= 200 and not i['symbol'].startswith('USD')]
            choice = []
            # up = 0
            # down = 0
            for i in tmp:
                try:
                    dic = self.calculation.cul_tec(i, 3)
                    self.notify.debug(str(i) + str(dic))
                    if dic['choice']:
                        choice.append(i)
                    break
                except Exception as e:
                    self.notify.critical(e)
                    break
                # if dic['macdlineAfter'] >= 0:
                #     up += 1
                # else:
                #     down += 1
                time.sleep(0.5)
            # if down > up:
            #     par = down / (down + up)
            #     print(str(par * 100), "%が下降")
            #     if par >= 0.9:
            #         line.send_line_notify2(str(par * 100) + "%の下降検知")
            #         print(str(par * 100), "%の下降検知")
            # else:
            #     par = up / (down + up)
            #     print(str(par * 100), "%が上昇")

            if choice:
                self.notify.debug(str(choice))
                decision = [self.calculation.check_1minute(i) for i in choice if float(self.calculation.check_1minute(i)) >= 20]
                res = [i for i in choice if float(self.calculation.check_1minute(i)) >= 20]
                if res:
                    self.notify.debug(str(decision))
                    self.notify.debug(str(res))
                    dic = dict(zip(res, decision))
                    sorted_dic = sorted(dic.items(), key=lambda x: -x[1])
                    self.notify.debug(str(sorted_dic))
                    self.selected_coin = sorted_dic
                else:
                    self.notify.debug("検出なし")
            else:
                self.notify.debug("検出なし")

