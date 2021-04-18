import BinanceController
import Calculation
import NotificationCenter
import ScrapingManager
import schedule
import time
import threading


class H4rvestRe4perClass:
    position = False

    buy = 0.0
    sell = 0.0

    def __init__(self):
        account = {'account1': {'api_key': "PDzV1ux2fLL0p0Ivs8KGk3PcxAXO5GJKYpsq0e5bI2TAjEKcBJJLr99iAty1GuPB",
                                'api_secret': "cYw3QPuWeah57wEn2ll1T7g5udOXVTmoBZP43mq4CEq2GTUWUW9yK9YTOnsrEEyi"
                                },
                   'account2': {'api_key': "AzI7xoktKczaf6Ja6XIcVKmfiiIan3zdnrOYvBciTLzdTHzgCpIPqtpKMisdmkjZ",
                                'api_secret': "JHS2qqgDWWFSBBZNCLWgExEW78lwkCfjBIUW6Z5nT3Yxoubsc4rVNpTicWRIwKq3"
                                }}
        self.binance_instance_1 = BinanceController.BinanceControllerClass(account['account1']['api_key'],
                                                                           account['account1']['api_secret'], 1)
        self.binance_instance_2 = BinanceController.BinanceControllerClass(account['account2']['api_key'],
                                                                           account['account2']['api_secret'], 2)
        self.Calculation_instance_1 = Calculation.CalculationClass(self.binance_instance_1, 1)
        self.Calculation_instance_2 = Calculation.CalculationClass(self.binance_instance_2, 2)
        self.notify = NotificationCenter.NotificationCenterClass("MainClass")
        self.scr = ScrapingManager.ScrapingManagerClass()

    def coin_balance(self):
        a = self.binance_instance_1.get_balance()
        b = self.binance_instance_2.get_balance()
        print(a,b)
        self.notify.debug("1")

    def job(self):
        print("I'm working...")
        th1 = threading.Thread(target=self.th)
        th1.start()

    def th(self):
        if self.position:
            trend5 = self.scr.cul_sell(2, "BTCUSDT")
            trend15 = self.scr.cul_sell(3, "BTCUSDT")
            if trend5 > 0.6 and trend15 > 0.6:
                self.sell = self.scr.get_price("BTCUSDT")
                self.notify.debug("売ります: " + str(self.sell))
                self.notify.debug("損益差: " + str(self.buy - self.sell))
                self.position = False
        else:
            trend1 = self.scr.cul_buy(1, "BTCUSDT")
            trend5 = self.scr.cul_buy(2, "BTCUSDT")
            trend15 = self.scr.cul_buy(3, "BTCUSDT")
            if trend1 > 0.6 and trend5 > 0.6 and trend15 > 0.6:
                self.buy = self.scr.get_price("BTCUSDT")
                self.notify.debug("買います: " + str(self.buy))
                self.position = True


if __name__ == "__main__":
    hr = H4rvestRe4perClass()
    hr.coin_balance()
    # schedule.every(1).minutes.do(hr.job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
