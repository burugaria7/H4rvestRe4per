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
        log_sp = sp.worksheet('決済履歴')
        pair_sp = sp.worksheet('自動通貨選択')
        test_sp = sp.worksheet('テスト用')

    def checkmaxmin_dictw(self, dic):
        with open('binary/checkmaxmin.binaryfile', 'wb') as web:
            pickle.dump(dic, web)

    def checkmaxmin_dictr(self):
        with open('binary/checkmaxmin.binaryfile', 'rb') as web:
            r = pickle.load(web)
            return r

    def checkmaxmin_listw(self, list):
        with open('binary/checkmaxminlist.binaryfile', 'wb') as web:
            pickle.dump(list, web)

    def checkmaxmin_listr(self):
        with open('binary/checkmaxminlist.binaryfile', 'rb') as web:
            r = pickle.load(web)
            return r

    def send_log_user1(self, data):
        raw_data = []

        # buy_date_insert
        cur_status = self.log_sp.row_values(4)
        buy_date = str(cur_status[0])
        buy_date_list = buy_date.split(' ')
        raw_data.append(str(buy_date_list[0]))
        raw_data.append(str(buy_date_list[1]))

        # sell_date_insert
        sell_date = str(data[0])
        sell_date_list = sell_date.split(' ')
        raw_data.append(str(sell_date_list[0]))
        raw_data.append(str(sell_date_list[1]))

        max_and_min = self.checkmaxmin_listr()
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

        self.log_sp.insert_row(raw_data, index=8, value_input_option='RAW')
