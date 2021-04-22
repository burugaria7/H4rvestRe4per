# 監視している通貨リスト
def get_monitoring_currency_cache():
    with open('save/monitoring_currency_cache.txt') as f:
        data = f.read()
        f.close()
        return data


def set_monitoring_currency_cache(data):
    f = open('save/monitoring_currency_cache.txt', 'w')
    f.write(data)
    return f.close()


# 今取引しているコインについての情報
# 取引してないときはNULL？
# userは1or2
def get_position_cache(user):
    if user != 1 and user != 2:
        return
    str = 'save/position_cache' + str(user) + '.txt'
    with open(str) as f:
        data = f.read()
        f.close()
        return data


def set_position_cache(user, data):
    if user != 1 and user != 2:
        return
    str = 'save/position_cache' + str(user) + '.txt'
    f = open(str, 'w')
    f.write(data)
    return f.close()


class CacheManagerClass:
    pass
