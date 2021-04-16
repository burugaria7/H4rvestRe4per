import BinanceController
from binance.client import Client
from datetime import  datetime

import NotificationCenter


class CalculationClass:
    def __init__(self,binance_instance):
        self.binance_instance: BinanceController = binance_instance
        self.notfy = NotificationCenter.NotificationCenterClass("CalculationClass")
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

if __name__ == "__main__":
    print("")
