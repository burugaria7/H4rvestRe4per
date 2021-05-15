import pickle
import time
from datetime import datetime, timedelta
from NotificationCenter import debug, info, warning, error, critical
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import os

# Googleサービスを認証
gauth = GoogleAuth()

# 資格情報ロードするか、存在しない場合は空の資格情報を作成
gauth.LoadCredentialsFile("mycreds.txt")

# Googleサービスの資格情報がない場合
if gauth.credentials is None:
    # ユーザーから認証コードを自動的に受信しローカルWebサーバーを設定
    gauth.LocalWebserverAuth()
# アクセストークンが存在しないか、期限切れかの場合
elif gauth.access_token_expired:
    # Googleサービスを認証をリフレッシュする
    gauth.Refresh()
# どちらにも一致しない場合
else:
    # Googleサービスを承認する
    gauth.Authorize()
# 資格情報をtxt形式でファイルに保存する
gauth.SaveCredentialsFile("mycreds.txt")

# Googleドライブの認証処理
drive = GoogleDrive(gauth)


# 監視している通貨リスト
def get_monitoring_currency_cache():
    try:
        file_id = drive.ListFile({'q': 'title = "monitoring_currency_cache.bin"'}).GetList()[0]['id']
        f = drive.CreateFile({'id': file_id})
        f.GetContentFile('save/monitoring_currency_cache.bin')
        z = open('save/monitoring_currency_cache.bin', 'rb')
        r = pickle.load(z)
        return r
    except:
        data = {}
        set_monitoring_currency_cache(data)
        return data


def set_monitoring_currency_cache(data):
    z = open('save/monitoring_currency_cache.bin', 'wb')
    pickle.dump(data, z)
    z.close()
    f = drive.CreateFile()
    f.SetContentFile('save/monitoring_currency_cache.bin')
    # Googleドライブにアップロード
    f.Upload()


# 今取引しているコインについての情報
# 取引してないときはNULL？
# userは1or2
def get_position_cache(user):
    user = str(user)
    if user != '1' and user != '2':
        return
    try:
        file_id = drive.ListFile({'q': 'title = "position_cache' + str(user) + '.bin"'}).GetList()[0]['id']
        f = drive.CreateFile({'id': file_id})
        f.GetContentFile('save/position_cache' + str(user) + '.bin')
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
    f = drive.CreateFile()
    f.SetContentFile('save/position_cache' + str(user) + '.bin')
    # Googleドライブにアップロード
    f.Upload()


class CacheManagerClass:
    def __init__(self):
        pass


if __name__ == "__main__":
    print(type(get_monitoring_currency_cache()))
