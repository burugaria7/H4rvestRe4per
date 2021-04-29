import sys
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


# LineBotインスタンスの初期化
url = "https://notify-api.line.me/api/notify"
access_token = 'athuyDTvtcVbV3HhlwiMA1Gg5jOUhmdJvGCAriRDYEK'
line_account_1 = LineBot.LineBotClass(url, access_token)
access_token = 'ADEmr8kryW8Z7hPR5LUOp5Mio5Wyokgi6wN8ZUQ3Svv'
line_account_2 = LineBot.LineBotClass(url, access_token)

# DiscordBotインスタンスの初期化
url = 'https://discord.com/api/webhooks/828983577470435328/o9C2zgxcyp5CQqRwi01BAukgmbs5gArrZgxjo4waEg9E' \
      '-h6yRTdzqPLWw6xwajNwC-Sg'
discord_account_1 = DiscordBot.DiscordBotClass(url)
url = 'https://discord.com/api/webhooks/831200616100659260/j0oR_VSrxokkFRaM2UNCZlwqhIbRYBr8ysU09HQksf80tjGaK7' \
      '-spRd1ZKs2dzY6sK4a'
discord_account_2 = DiscordBot.DiscordBotClass(url)

class_name = "log/log.log"
# ベースのログ設定
# logging.basicConfig(filename=class_name, level=logging.WARNING)
# 独自のログ設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_file = logging.FileHandler(class_name)
logger.addHandler(log_file)


def notify_to_line(msg, level, account_no):
    level = "[" + level + "]"
    msg = level + "\n" + msg
    if account_no == 1:
        line_account_1.send_msg(msg)
    if account_no == 2:
        line_account_2.send_msg(msg)
    if account_no == 3:
        line_account_1.send_msg(msg)
        line_account_2.send_msg(msg)


def notify_to_discord(msg, level, account_no):
    level = "[" + level + "]"
    msg = level + "\n" + msg
    if account_no == 1:
        discord_account_1.send_msg(msg)
    if account_no == 2:
        discord_account_2.send_msg(msg)
    if account_no == 3:
        discord_account_1.send_msg(msg)
        discord_account_2.send_msg(msg)
    debug("こちらNotificationCenterのコンストラクタ応答せよ！！")


def debug(msg):
    msg = str(msg)
    dt_now = datetime.datetime.now()
    logger.debug(str(dt_now) + "\t[DEBUG]\t" + msg)
    print(str(dt_now) + "\t[DEBUG]\t" + msg)


def info(*args):
    user = 3
    if len(args) > 1:
        user = args[1]
    msg = str(args[0])
    dt_now = datetime.datetime.now()
    print(str(dt_now) + pycolor.BLUE + "\t[INFO]\t" + pycolor.END + msg)
    notify_to_discord(msg, "INFO", user)
    notify_to_line(msg, "INFO", user)


def warning(msg):
    msg = str(msg)
    dt_now = datetime.datetime.now()
    print(str(dt_now) + pycolor.YELLOW + "\t[WARNING]\t" + pycolor.END + msg)


def error(*args):
    user = 3
    if len(args) > 1:
        user = args[1]
    msg = str(args[0])
    dt_now = datetime.datetime.now()
    print(str(dt_now) + pycolor.RED + "\t[ERROR]\t" + pycolor.END + msg)
    notify_to_discord(msg, "ERROR", user)
    notify_to_line(msg, "ERROR", user)


def critical(*args):
    user = 3
    if len(args) > 1:
        user = args[1]
    msg = str(args[0])
    dt_now = datetime.datetime.now()
    print(str(dt_now) + "\t" + pycolor.RED_FLASH + "[CRITICAL]" + pycolor.END + "\t" + msg)
    notify_to_discord(msg, "CRITICAL", user)
    notify_to_line(msg, "CRITICAL", user)


if __name__ == '__main__':
    notify = NotificationCenterClass("test")
    # notify.notify_to_discord("Hello", "ERROR", 3)
    notify.debug("Hello")
    # notify.info("Hello", 3)
    # notify.warning("Hello")
    # notify.error("Hello")
    # notify.critical("Hello")
