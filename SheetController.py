import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime
import time
import pickle
from NotificationCenter import debug, info, warning, error, critical


class SheetControllerClass:

    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds']

        # ダウンロードしたjsonファイル名を記入
        json_file = 'autobot-307906-efae34e587fc.json'
        # スプレッドシートIDを記入
        sheet_id = '1FNsjdiefDbuWYtuZ2sncf6PJV09uhBePDDs2_3hvSas'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
        gc = gspread.authorize(credentials)
        sp = gc.open_by_key(sheet_id)
        self.log1_sp = sp.worksheet('決済履歴')
        self.log2_sp = sp.worksheet('決済履歴2')
        self.pair_sp = sp.worksheet('自動通貨選択')
        self.test_sp = sp.worksheet('テスト用')
        self.demo_sp = sp.worksheet('デモ')

    # この関数もキャッシュ全部ファイル化することで使わんくしたい
    def get_buy_date(self, user):
        buy_date = []
        cur_status = []
        # buy_date_insert
        if user == 1:
            cur_status = self.log1_sp.row_values(4)
        elif user == 2:
            cur_status = self.log2_sp.row_values(4)

        buy_date_time = str(cur_status[0])
        buy_date_split = buy_date_time.split(' ')
        buy_date.append(str(buy_date_split[0]))
        buy_date.append(str(buy_date_split[1]))
        return buy_date

    def post_log(self, user, data):
        print(data)
        if user == 1:
            self.log1_sp.insert_row(data, index=8, value_input_option='RAW')
        elif user == 2:
            self.log2_sp.insert_row(data, index=8, value_input_option='RAW')
        elif user == 0:
            self.demo_sp.insert_row(data, index=8, value_input_option='RAW')
