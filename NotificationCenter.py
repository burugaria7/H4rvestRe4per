import sys
import logging
import LineBot
import DiscordBot


class NotificationCenterClass:
    # コンストラクタの定義
    def __init__(self):
        print("こちらNotificationCenterのコンストラクタ応答せよ！！")

        # LineBotインスタンスの初期化
        url = "https://notify-api.line.me/api/notify"
        access_token = 'athuyDTvtcVbV3HhlwiMA1Gg5jOUhmdJvGCAriRDYEK'
        self.line_account_1 = LineBot.LineBotClass(url, access_token)
        access_token = 'ADEmr8kryW8Z7hPR5LUOp5Mio5Wyokgi6wN8ZUQ3Svv'
        self.line_account_2 = LineBot.LineBotClass(url, access_token)

        # DiscordBotインスタンスの初期化
        url = 'https://discord.com/api/webhooks/828983577470435328/o9C2zgxcyp5CQqRwi01BAukgmbs5gArrZgxjo4waEg9E' \
              '-h6yRTdzqPLWw6xwajNwC-Sg'
        self.discord_account_1 = DiscordBot.DiscordBotClass(url)
        url = 'https://discord.com/api/webhooks/831200616100659260/j0oR_VSrxokkFRaM2UNCZlwqhIbRYBr8ysU09HQksf80tjGaK7' \
              '-spRd1ZKs2dzY6sK4a'
        self.discord_account_2 = DiscordBot.DiscordBotClass(url)

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

    def notify_to_discord(self, msg, attribute, account_no):
        attribute = "[" + attribute + "]"
        msg = attribute + "\n" + msg
        if account_no == 1:
            self.discord_account_1.send_msg(msg)
        if account_no == 2:
            self.discord_account_2.send_msg(msg)
        if account_no == 3:
            self.discord_account_1.send_msg(msg)
            self.discord_account_2.send_msg(msg)


if __name__ == '__main__':
    notify = NotificationCenterClass()
    notify.notify_to_discord("Hello", "ERROR", 3)
