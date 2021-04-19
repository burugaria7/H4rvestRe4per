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
# メインAPI用
# 取引してないときはNULL？
def get_position_cache1():
    with open('save/position_cache1.txt') as f:
        data = f.read()
        f.close()
        return data


def set_position_cache1(data):
    f = open('save/position_cache1.txt', 'w')
    f.write(data)
    return f.close()


# 今取引しているコインについての情報
# サブAPI用
# 取引してないときはNULL？
def get_position_cache2():
    with open('save/position_cache2.txt') as f:
        data = f.read()
        f.close()
        return data


def set_position_cache2(data):
    f = open('save/position_cache2.txt', 'w')
    f.write(data)
    return f.close()


class CacheManagerClass:
    pass
