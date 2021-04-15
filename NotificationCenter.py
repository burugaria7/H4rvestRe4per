import sys
import logging
import LineBot


class NotificationCenterClass:
    # コンストラクタの定義
    def __init__(self):
        # LineBotインスタンスの初期化
        url = "https://notify-api.line.me/api/notify"
        access_token = 'athuyDTvtcVbV3HhlwiMA1Gg5jOUhmdJvGCAriRDYEK'
        self.line_account_1 = LineBot.LineBotClass(url, access_token)
        access_token = 'ADEmr8kryW8Z7hPR5LUOp5Mio5Wyokgi6wN8ZUQ3Svv'
        self.line_account_2 = LineBot.LineBotClass(url, access_token)

        print("こちらNotificationCenterのコンストラクタ応答せよ！！")

    def notify_to_line(self, msg, attribute, account_no):
        attribute = "[" + attribute + "]"
        msg = attribute + "\n" + msg
        if account_no == 1:
            self.line_account_1.send_msg(msg)
        if account_no == 2:
            self.line_account_2.send_msg(msg)
        if account_no == 3:
            self.line_account_1.send_msg(msg)
            self.line_account_2.send_msg(msg)


if __name__ == '__main__':
    notify = NotificationCenterClass()
    notify.notify_to_line("Hello", "ERROR", 3)
