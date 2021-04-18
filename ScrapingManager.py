import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import NotificationCenter


class ScrapingManagerClass:

    def __init__(self):
        self.notify = NotificationCenter.NotificationCenterClass("ScrapingManagerClass")

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
            '//*[@id="technicals-root"]/div/div/div[1]/div/div/div[1]/div/div/div[' + str(period) + ']')
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

    def get_price(self, pair):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        TARGET_URL = "https://jp.tradingview.com/symbols/" + pair + "/technicals/"
        driver.get(TARGET_URL)
        time.sleep(2)
        price = driver.find_element_by_xpath(
            '//*[@id="anchor-page-1"]/div/div[3]/div[1]/div/div/div/div[1]/div[1]')
        return int(price.text)

    def cul_trend_from_tradingview(self, period, pair):
        trend = self.get_tradingview_trend(period, pair)
        if trend['sell'] / sum(trend.values()) >= 0.7:
            print("強い売り")
            return False
        elif trend['sell'] / sum(trend.values()) <= 0.3:
            print("強い買い")
        return True

    def cul_sell(self, period, pair):
        trend = self.get_tradingview_trend(period, pair)
        return trend['sell'] / sum(trend.values())

    def cul_buy(self, period, pair):
        trend = self.get_tradingview_trend(period, pair)
        return trend['buy'] / sum(trend.values())

if __name__ == "__main__":
    inst = ScrapingManagerClass()
    print(str(inst.get_price("BTCUSDT")))