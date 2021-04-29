import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from NotificationCenter import debug, info, warning, error, critical



class ScrapingManagerClass:

    def __init__(self):
        pass

    def get_tradingview_trend(self, period, pair):
        trend = {
            'sell': 0,
            'even': 0,
            'buy': 0,
        }
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        TARGET_URL = "https://jp.tradingview.com/symbols/" + pair + "/technicals/"
        driver.get(TARGET_URL)
        time.sleep(2)
        tab = driver.find_element_by_xpath(
            '//*[@id="technicals-root"]/div/div/div[1]/div/div/div/button[' + str(period) + ']')
        tab.click()
        time.sleep(1)

        sell_ele = driver.find_element_by_xpath(
            '//*[@id="technicals-root"]/div/div/div[2]/div[2]/div[2]/div[1]/span[1]')
        sell_val = sell_ele.text

        even_ele = driver.find_element_by_xpath(
            '//*[@id="technicals-root"]/div/div/div[2]/div[2]/div[2]/div[2]/span[1]')
        even_val = even_ele.text

        buy_ele = driver.find_element_by_xpath(
            '//*[@id="technicals-root"]/div/div/div[2]/div[2]/div[2]/div[3]/span[1]')
        buy_val = buy_ele.text

        driver.close()
        trend['sell'] = float(sell_val)
        trend['even'] = float(even_val)
        trend['buy'] = float(buy_val)
        # print("sell=", sell_val)
        # print("even=", even_val)
        # print("buy=", buy_val)
        return trend

    # period 1:1分足 2:5分足 3:15分足 4:1時間足
    def cul_trend_from_tradingview(self, period, pair):
        trend = self.get_tradingview_trend(period, pair)
        if float(trend['buy']) / sum(trend.values()) >= 0.6:
            print("買い")
            return True
        return False



    def cul_sell(self, period, pair):
        trend = self.get_tradingview_trend(period, pair)
        return trend['sell'] / sum(trend.values())

    def cul_buy(self, period, pair):
        trend = self.get_tradingview_trend(period, pair)
        return trend['buy'] / sum(trend.values())

if __name__ == "__main__":
    inst = ScrapingManagerClass()
    print(inst.cul_trend_from_tradingview(2, 'BTCUSDT'))