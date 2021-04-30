import BinanceController
import time
import Calculation
from datetime import datetime
from NotificationCenter import debug, info, warning, error, critical


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
                   'USDT' in i['symbol'] and 'DOWN' not in i['symbol'] and 'UP' not in i['symbol'] and float(
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
                except ConnectionResetError as e:
                    warning(e)
                except Exception as e:
                    critical(e)
                time.sleep(0.5)

            if choice:
                debug(str(choice))
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
    dic = {'user': 2, 'status': True, 'pair': 'BTCSTUSDT', 'amount': '6666666', 'buy_time': datetime(2021, 4, 29, 19, 4, 18, 337972), 'sell_time': None, 'buy_coin': '42.67300000', 'sell_coin': 0, 'profit': 0, 'mode': 0}
    print(Cal.calculation.sell_algorithm(dic))
