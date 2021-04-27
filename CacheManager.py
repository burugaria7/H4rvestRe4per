import pickle


# 監視している通貨リスト
def get_monitoring_currency_cache():
    with open('save/monitoring_currency_cache.bin') as f:
        data = f.read()
        f.close()
        return data


def set_monitoring_currency_cache(data):
    f = open('save/monitoring_currency_cache.bin', 'w')
    f.write(data)
    return f.close()


# 今取引しているコインについての情報
# 取引してないときはNULL？
# userは1or2
def get_position_cache(user):
    if user != 1 and user != 2:
        return
    path = 'save/position_cache' + str(user) + '.bin'
    with open(path, 'rb') as web:
        r = pickle.load(web)
        return r


def set_position_cache(user, data):
    if user != 1 and user != 2:
        return
    path = 'save/position_cache' + str(user) + '.bin'
    with open(path, 'wb') as web:
        pickle.dump(data, web)


class CacheManagerClass:
    def __init__(self):
        pass

if __name__ == "__main__":
    dict = {
        'status': True,
        'dt_now': None,
        'price': 0,
        'usecoin': None,
        'amount': 0,
        'wasOverbuy': False,
        'wasOversold': False,
        'crossoverbuy': False,
        'crossoversold': False,
        'buycoin': 0,
        'sellcoin': 0,
        'mode': 0,
    }
    set_position_cache(1,dict)
    print(get_position_cache(1))
