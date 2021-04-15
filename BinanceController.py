from binance.client import Client
import ccxt


class BinanceControllorClass:
    def __init__(self,api_key,api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(api_key, api_secret)
        self.binance = ccxt.binance({'apiKey': str(api_key), 'secret': str(api_secret), })

    def get_price(self,coin):
        info = self.client.get_recent_trades(symbol=coin)
        coin = info[-1]['price']
        print("現在の価格:", coin)
        return coin

    def get_balance(self):
        bi_balance = self.binance.fetchBalance()
        dic = bi_balance['total']
        tmp = {}
        for key, value in dic.items():
            if value != 0:
                tmp[key] = value
        return tmp

    def buy_all(self, coin):
        dic = self.get_balance()
        qat = int(dic['USDT'] / float(self.get_price(coin)))
        order = self.client.order_market_buy(symbol=coin, quantity=qat)
        print(order["symbol"])
        print(order["side"])
        print("量：" + order["origQty"])

    def sell_all(self, coin):
        dic = self.get_balance()
        qat = int(dic[coin.replace('USDT', '')])
        order = self.client.order_market_sell(symbol=coin, quantity=qat)
        print(order["symbol"])
        print(order["side"])
        print("量：" + order["origQty"])

    def buy_piece(self, coin, qat):
        order = self.client.order_market_buy(symbol=coin, quantity=qat)
        print(order["symbol"])
        print(order["side"])
        print("量：" + order["origQty"])

    def sell_piece(self, coin, qat):
        order = self.client.order_market_sell(symbol=coin, quantity=qat)
        print(order["symbol"])
        print(order["side"])
        print("量：" + order["origQty"])


