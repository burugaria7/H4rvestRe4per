import sys
import logging
import LineBot
import DiscordBot
import datetime
import logging


class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RETURN = '\033[07m'  # 反転
    ACCENT = '\033[01m'  # 強調
    FLASH = '\033[05m'  # 点滅
    RED_FLASH = '\033[05;41m'  # 赤背景+点滅
    END = '\033[0m'


class NotificationCenterClass:
    # コンストラクタの定義
    def __init__(self):
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

        # ベースのログ設定
        logging.basicConfig(filename='test.log', level=logging.WARNING)
        # 独自のログ設定
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        log_file = logging.FileHandler('test.log')
        self.logger.addHandler(log_file)

    def notify_to_line(self, msg, level, account_no):
        level = "[" + level + "]"
        msg = level + "\n" + msg
        if account_no == 1:
            self.line_account_1.send_msg(msg)
        if account_no == 2:
            self.line_account_2.send_msg(msg)
        if account_no == 3:
            self.line_account_1.send_msg(msg)
            self.line_account_2.send_msg(msg)

    def notify_to_discord(self, msg, level, account_no):
        level = "[" + level + "]"
        msg = level + "\n" + msg
        if account_no == 1:
            self.discord_account_1.send_msg(msg)
        if account_no == 2:
            self.discord_account_2.send_msg(msg)
        if account_no == 3:
            self.discord_account_1.send_msg(msg)
            self.discord_account_2.send_msg(msg)
        self.debug("こちらNotificationCenterのコンストラクタ応答せよ！！")

    def debug(self, msg):
        msg = str(msg)
        dt_now = datetime.datetime.now()
        self.logger.debug(str(dt_now) + "\t[DEBUG]\t" + msg)
        print(str(dt_now) + "\t[DEBUG]\t" + msg)

    def info(self, msg, user):
        msg = str(msg)
        dt_now = datetime.datetime.now()
        print(str(dt_now) + pycolor.BLUE + "\t[INFO]\t" + pycolor.END + msg)
        self.notify_to_discord(msg, "INFO", user)
        self.notify_to_line(msg, "INFO", user)

    def warning(self, msg):
        msg = str(msg)
        dt_now = datetime.datetime.now()
        print(str(dt_now) + pycolor.YELLOW + "\t[WARNING]\t" + pycolor.END + msg)

    def error(self, msg, user):
        msg = str(msg)
        dt_now = datetime.datetime.now()
        print(str(dt_now) + pycolor.RED + "\t[ERROR]\t" + pycolor.END + msg)
        self.notify_to_discord(msg, "ERROR", user)
        self.notify_to_line(msg, "ERROR", user)

    def critical(self, msg, user):
        msg = str(msg)
        dt_now = datetime.datetime.now()
        print(str(dt_now) + "\t" + pycolor.RED_FLASH + "[CRITICAL]" + pycolor.END + "\t" + msg)
        self.notify_to_discord(msg, "CRITICAL", user)
        self.notify_to_line(msg, "CRITICAL", user)


if __name__ == '__main__':
    notify = NotificationCenterClass()
    # notify.notify_to_discord("Hello", "ERROR", 3)
    notify.debug("Hello")
    # notify.info("Hello", 3)
    # notify.warning("Hello")
    # notify.error("Hello")
    # notify.critical("Hello")
