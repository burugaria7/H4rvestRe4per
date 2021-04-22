import BinanceController
import Calculation
import NotificationCenter
import ScrapingManager
import schedule
import time
import threading
import SheetController
import CacheManager as Cache


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
        self.binance_instance_1 = BinanceController.BinanceControllerClass(self.account['1']['api_key'],
                                                                           self.account['1']['api_secret'], 1)
        self.binance_instance_2 = BinanceController.BinanceControllerClass(self.account['2']['api_key'],
                                                                           self.account['2']['api_secret'], 2)
        self.Calculation_instance_1 = Calculation.CalculationClass(self.binance_instance_1, 1)
        self.Calculation_instance_2 = Calculation.CalculationClass(self.binance_instance_2, 2)
        self.ScrapingManager_instance_1 = Calculation.CalculationClass(self.binance_instance_1, 1)
        self.ScrapingManager_instance_2 = Calculation.CalculationClass(self.binance_instance_2, 2)
        self.notify = NotificationCenter.NotificationCenterClass("MainClass")
        self.scr = ScrapingManager.ScrapingManagerClass()
        self.sheet = SheetController.SheetControllerClass()

    def coin_balance(self):
        # a = self.binance_instance_1.get_balance()
        b = self.binance_instance_2.get_balance()
        self.notify.debug("1")

    def main_bot(self):
        for i in self.account:
            dict = {
                'status': False,
                'dt_now': None,
                'price': 0,
                'usecoin': currentcoin,
                'amount': 0,
                'wasOverbuy': False,
                'wasOversold': False,
                'crossoverbuy': False,
                'crossoversold': False,
                'buycoin': 0,
                'sellcoin': 0,
                'mode': 0,
            }
            dict = Cache.get_position_cache(i)
            if len(dict) > 0:

            else:




        while True:
            notuse, coinlist1 = gspread1.coin_read()
            coinlist = check_deadline()
            print("------------------------------")
            print("検出通貨:", coinlist)
            for usecoin in coinlist:
                dict['usecoin'] = usecoin
                print("------------------------------")
                print("監視中:", usecoin)
                gspread1.txt_write(usecoin)
                dict['dt_now'] = datetime.now()
                print("------------------------------")
                print(dict['dt_now'])
                RSISoldLevel = 30
                RSIBuyLevel = 70
                dict['crossoverbuy'] = False
                dict['crossoversold'] = False
                dict = info(dict, usecoin)
                print("チェック中")
                # 全期間のビットコインの価格を取得する
                Price, Time = coin.maxmin_day(usecoin)
                items = pd.DataFrame({'Value': Price, 'Time': Time})

                # データをnumpy行列に変換する
                price = np.array(items['Value'], dtype='f8')
                date = np.array(items['Time'])
                macd, macdsignal, macdhist = talib.MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
                rsi14 = talib.RSI(price, timeperiod=14)
                tec['rsi14'] = rsi14[-1]
                plt.clf()
                plt.close('all')
                plot_main(date, price, macd, macdsignal, macdhist, rsi14)

                macdline = macd - macdsignal
                tec['macdlineAfter'] = macdline[-1]
                tec['macdlineBefore'] = macdline[-2]
                print("RSI14:", tec['rsi14'])
                print("macdlineAfter:", tec['macdlineAfter'])
                print("macdlineBefore:", tec['macdlineBefore'])

                if rsi14[-1] >= RSIBuyLevel or rsi14[-2] >= RSIBuyLevel or rsi14[-3] >= RSIBuyLevel or rsi14[
                    -4] >= RSIBuyLevel or rsi14[-5] >= RSIBuyLevel or rsi14[-6] >= RSIBuyLevel:
                    dict['wasOverbuy'] = True
                    print("現在は買われすぎです")
                    line.send_line_notify("現在は買われすぎです")

                if rsi14[-1] <= RSISoldLevel:
                    dict['wasOversold'] = True
                    print("現在は売られすぎです")
                    line.send_line_notify("現在は売られすぎです")

                if macdhist[-1] >= 0 and macdline[-1] > 0 and macdline[-2] < 0:
                    dict['crossoverbuy'] = True
                    print("クロスオーバー:買い時")
                    line.send_line_notify("クロスオーバー:買い時")
                if macdhist[-1] <= 0 and macdline[-1] < 0 and macdline[-2] > 0:
                    dict['crossoversold'] = True
                    print("クロスオーバー:売り時")
                    line.send_line_notify("クロスオーバー:売り時")

                if dict['wasOversold'] and dict['crossoverbuy'] and not dict['status']:
                    if self.scr.cul_trend_from_tradingview(2, "BTCUSDT") and self.scr.cul_trend_from_tradingview(2,
                                                                                                                 dict[
                                                                                                                     'usecoin']):
                        print("買い注文最終確定・・・")
                        r = gspread1.txt_readlist()
                        r[usecoin] = datetime.now()
                        gspread1.txt_writelist(r)
                        dict['amount'] = paypay.marketbuy()
                        print(dict['price'], "で買いました")
                        line.send_line_notify(str(dict['price']) + "で買いました(おおよそ)")
                        dict['status'] = True
                        dict['buycoin'] = dict['price']
                        dict['sellcoin'] = 0
                        dict['mode'] = 0
                        do_maxmin(dict)
                        buylist.append(dict['price'])
                        show_pay(buylist, selllist)
                        show_coin()
                        set_chart_url(dict['usecoin'])
                        spread_input(dict, cul_profit(paypay.myself_info2()), usecoin)
                        gspread1.deta_write4(usecoin)
                        gspread1.line1_send()
                        gspread1.usedpay_write(str(gspread1.current_read()))
                        sellonly.auto_ST()
                    elif not self.scr.cul_trend_from_tradingview(2, dict['usecoin']):
                        print("買いの判定がありませんでした")
                        line.send_line_notify2("買いの判定がありませんでした")
                    else:
                        print("BTCの強い売りにより買い注文実行中止・・")
                        line.send_line_notify2("BTCの強い売りにより買い注文実行中止・・")
                if dict['wasOverbuy'] or dict['wasOversold'] or dict['crossoverbuy'] or dict['crossoversold']:
                    line.send_line_gazo("現在のチャート")
                    line.send_line_notify("\n" + sugoi_json_dumps(dict))
                    line.send_line_notify("\n" + sugoi_json_dumps(tec))
                gspread1.dis_writelist(dict)
                time.sleep(60 / len(coinlist))

    def sell_bot(self):
        print()


if __name__ == "__main__":
    hr = H4rvestRe4perClass()
    hr.coin_balance()
    # schedule.every(1).minutes.do(hr.job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
