import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime
import time
import pickle


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
        log1_sp = sp.worksheet('決済履歴')
        log2_sp = sp.worksheet('決済履歴2')
        pair_sp = sp.worksheet('自動通貨選択')
        test_sp = sp.worksheet('テスト用')

    # この関数もキャッシュ全部ファイル化することで使わんくしたい
    def get_buy_date(self, user):
        buy_date = []
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

    def send_log(self, user, data):

        if user != 1 and user != 2:
            return

        raw_data = self.get_buy_date(user)

        # sell_date_insert
        sell_date = str(data[0])
        sell_date_list = sell_date.split(' ')
        raw_data.append(str(sell_date_list[0]))
        raw_data.append(str(sell_date_list[1]))

        # max_minの計算を修正する↓
        # max min は外で計算してdataで渡すのが良さそう
        k = 0
        for i in data:
            if k > 0:
                raw_data.append(i)
            k += 1

        if data[2] <= data[3]:
            percent = (float(data[3]) / float(data[2]) - 1)
            raw_data.append(percent)
        else:
            percent = (1 - float(data[2]) / float(data[3]))
            raw_data.append(percent)
        for j in max_and_min:
            if isinstance(j, type(max_and_min[-1])):
                raw_data.append(str(j))
            else:
                raw_data.append(j)

        self.log1_sp.insert_row(raw_data, index=8, value_input_option='RAW')
