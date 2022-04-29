import pickle
import time
from datetime import datetime, timedelta
from NotificationCenter import debug, info, warning, error, critical
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import os

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("h4rvestre4per-firebase-adminsdk-du65m-806725a0ef.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

drive_id = "0XXXXXXXXXXXXXVA"  # confirm from url
folder_id = "1_VpYpXiISNr-fFEJVfGa0UTTwFoXVh1K"  # confirm from url

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
        query = "'{}' in parents and trashed=false".format(folder_id)

        for file_list in drive.ListFile({'q': query}):
            for file in file_list:
                if file['title'] == 'monitoring_currency_cache.bin':
                    file.GetContentFile('save/monitoring_currency_cache.bin')
                    print("download")
                else:
                    print("pass")
        # f = drive.CreateFile({'id': file_id})
        # f.GetContentFile('save/monitoring_currency_cache.bin')
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

    file_metadata = {
        'id': "1f4PN92WgusiWjhS_UxwUkrgcSO9i8ive",
        'title': "monitoring_currency_cache.bin",
        'parents': [{
            'id': folder_id,
            'kind': 'drive#fileLink',
        }],
    }
    f = drive.CreateFile(file_metadata)
    # use SetContentFile for attach and upload
    f.SetContentFile('save/monitoring_currency_cache.bin')
    # always apply param when upload
    f.Upload(param={'supportsTeamDrives': True})
    print("uploaded")


# 今取引しているコインについての情報
# 取引してないときはNULL？
# userは1or2
def get_position_cache():
    try:
        query = "'{}' in parents and trashed=false".format(folder_id)

        for file_list in drive.ListFile({'q': query}):
            for file in file_list:
                if file['title'] == 'position_cache.bin':
                    file.GetContentFile('save/position_cache.bin')
                    print("download")
                else:
                    print("pass")
        path = 'save/position_cache.bin'
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
        set_position_cache(data)
        warning("[CacheManager]例外：ファイルがないので初期ファイルを作成します")
        return data


def set_position_cache(data):
    path = 'save/position_cache.bin'
    with open(path, 'wb') as web:
        pickle.dump(data, web)

    file_metadata = {
        'id': '1QDUlb164YvgfH76Zww8CVYIm4wL__sv9',
        'title': 'position_cache.bin',
        'parents': [{
            'id': folder_id,
            'kind': 'drive#fileLink',
        }],
    }
    f = drive.CreateFile(file_metadata)
    # use SetContentFile for attach and upload
    f.SetContentFile('save/position_cache.bin')
    # always apply param when upload
    f.Upload(param={'supportsTeamDrives': True})


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
    # set_position_cache(dict)
    # set_monitoring_currency_cache(data)
    print(get_position_cache())