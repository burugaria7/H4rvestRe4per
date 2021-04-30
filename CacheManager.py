import pickle
from datetime import datetime, timedelta
from NotificationCenter import debug, info, warning, error, critical


# 監視している通貨リスト
def get_monitoring_currency_cache():
    try:
        f = open('save/monitoring_currency_cache.bin', 'rb')
        r = pickle.load(f)
        return r
    except:
        data = {}
        set_monitoring_currency_cache(data)
        return data


def set_monitoring_currency_cache(data):
    f = open('save/monitoring_currency_cache.bin', 'wb')
    pickle.dump(data, f)
    f.close()


# 今取引しているコインについての情報
# 取引してないときはNULL？
# userは1or2
def get_position_cache(user):
    user = str(user)
    if user != '1' and user != '2':
        return
    try:
        path = 'save/position_cache' + str(user) + '.bin'
        with open(path, 'rb') as web:
            r = pickle.load(web)
            return r
    except:
        data = {
                'user': 0,
                'status': False,
                'pair': None,
                'amount': 0,
                'buy_time': None,
                'sell_time': None,
                'buy_coin': 0,
                'sell_coin': 0,
                'profit': 0,
                'mode': 0,
            }
        set_position_cache(user, data)
        warning("[CacheManager]例外：ファイルがないので初期ファイルを作成します")
        return data


def set_position_cache(user, data):
    user = str(user)
    if user != '1' and user != '2':
        return
    path = 'save/position_cache' + str(user) + '.bin'
    with open(path, 'wb') as web:
        pickle.dump(data, web)


class CacheManagerClass:
    def __init__(self):
        pass


if __name__ == "__main__":
    dict = {
        'status': False,
        'dt_now': None,
        'price': 0,
        'usecoin': None,
        'amount': 0,
        'wasOverbuy': False,
        'wasOversold': False,
        'crossoverbuy': False,
        'crossoversold': False,
        'buy_coin': 0,
        'sell_coin': 0,
        'mode': 0,
    }
    data = {'XEMUSDT': datetime.now() + timedelta(hours=1),
            'BATUSDT': datetime.now() + timedelta(hours=1)
            }
    # set_position_cache(1, dict)
    # set_monitoring_currency_cache(data)
    print(get_position_cache(1))
    print(get_position_cache(2))
