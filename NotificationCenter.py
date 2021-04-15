import sys
import logging
import LineBot


class NotificationCenter:
    # コンストラクタの定義
    def __init__(self):
        # LineBotインスタンスの初期化
        url = "https://notify-api.line.me/api/notify"
        access_token = '3jgVGsjkOAsuiGL9UgKGPeHm5Zn2yFkgJWRd6v97TXg'
        self.line_account_1 = LineBot(url, access_token)
        access_token = 'athuyDTvtcVbV3HhlwiMA1Gg5jOUhmdJvGCAriRDYEK'
        self.line_account_2 = LineBot(url, access_token)

        print("こちらNotificationCenterのコンストラクタ応答せよ！！")

    def notify_to_line(self, msg, type, account_no):
        if account_no == 1:
            self.line_account_1.send_msg(msg)
        if account_no == 2:
            self.line_account_2.send_msg(msg)
        if account_no == 3:
            self.line_account_1.send_msg(msg)
            self.line_account_2.send_msg(msg)


if __name__ == '__main__':
    notif = NotificationCenter()
    notif.notify_to_line("Hello", 1, 3)
