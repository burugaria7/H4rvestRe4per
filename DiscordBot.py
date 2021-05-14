from discord_webhook import DiscordWebhook
import discord
import threading
import asyncio
import time
from discord.ext import tasks

class DiscordBotClass:
    def __init__(self, url):
        self.url = url
        self.client = discord.Client()

        self.status = "starting..."


        @self.client.event
        async def on_ready():
            # 起動したらターミナルにログイン通知が表示される
            print('ログインしました')
            send_message_every_10sec.start()

        @tasks.loop(seconds=30)
        async def send_message_every_10sec():
            print("a")
            activity = discord.Activity(name=self.status,type=discord.ActivityType.custom)
            await self.client.change_presence(status=discord.Status.idle, activity=activity)

        # メッセージ受信時に動作する処理
        @self.client.event
        async def on_message(message):
            # メッセージ送信者がBotだった場合は無視する
            if message.author.bot:
                return
            # 「/neko」と発言したら「にゃーん」が返る処理
            if message.content == '/neko':
                await message.channel.send('にゃーん')
                activity = discord.Game(name="ABC", type=3)
                await self.client.change_presence(status=discord.Status.idle, activity=activity)

        def maindisbot():
            self.client.run("ODI2MDgxNjc3NjE1OTU1OTg4.YGHSgw.B-UGUmwaAlirqasXIgLHDNF-0EU")


        thread1 = threading.Thread(target=maindisbot)
        thread1.start()


    def send_msg(self, msg):
        webhook = DiscordWebhook(url=self.url, content=msg)
        response = webhook.execute()

if __name__ == "__main__":
    ins = DiscordBotClass("https://discord.com/api/webhooks/828983577470435328/o9C2zgxcyp5CQqRwi01BAukgmbs5gArrZgxjo4waEg9E' \
      '-h6yRTdzqPLWw6xwajNwC-Sg")
    time.sleep(5)