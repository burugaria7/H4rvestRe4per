import BinanceController
import Calculation
from datetime import datetime


class H4rvestRe4perClass:
    def __init__(self):
        account = {'accout1':0,'account2':0}
        account['accout1']={'api_key': "PDzV1ux2fLL0p0Ivs8KGk3PcxAXO5GJKYpsq0e5bI2TAjEKcBJJLr99iAty1GuPB",
                            'api_secret': "cYw3QPuWeah57wEn2ll1T7g5udOXVTmoBZP43mq4CEq2GTUWUW9yK9YTOnsrEEyi"
                            }
        account['accout2'] = {'api_key': "AzI7xoktKczaf6Ja6XIcVKmfiiIan3zdnrOYvBciTLzdTHzgCpIPqtpKMisdmkjZ",
                              'api_secret': "JHS2qqgDWWFSBBZNCLWgExEW78lwkCfjBIUW6Z5nT3Yxoubsc4rVNpTicWRIwKq3"
                              }
        self.binance_instance_1 = BinanceController.BinanceControllorClass(account['accout1']['api_key'],account['accout1']['api_secret'])
        self.binance_instance_2 = BinanceController.BinanceControllorClass(account['accout2']['api_key'],account['accout2']['api_secret'])
        self.Calculation = Calculation.CalculationClass(self.binance_instance_1)
    def coin_balance(self):
        print(self.binance_instance_1.coin_raw_1min("XEMUSDT"))
        print(self.binance_instance_2.get_balance())
    def coin_test(self):
        start = datetime(2021, 4, 15, 10, 37)
        print(type(start))
        end = datetime(2021, 4, 15, 12, 35)
        price = 3.14817
        coin = "WRXUSDT"
        if isinstance(start, type(start)):
            print(self.Calculation.maxmin_auto(coin, start, end, price))
        else:
            print("error")


if __name__ == "__main__":
    B = H4rvestRe4perClass()
    B.coin_balance()