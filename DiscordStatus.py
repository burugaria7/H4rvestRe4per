from discord_webhook import DiscordWebhook
import discord
import threading
import asyncio
import time
from discord.ext import tasks

class DiscordStatusClass:
    def __init__(self):
        self.client = discord.Client()
        self.status = "starting up..."
        self.status_buf = "starting up..."

        @self.client.event
        async def on_ready():
            # 起動したらターミナルにログイン通知が表示される
            print('ログインしました')
            send_message_every.start()

        @tasks.loop(seconds=5)
        async def send_message_every():
            if self.status != self.status_buf:
                activity = discord.Activity(name=str(self.status), type=1)
                await self.client.change_presence(status=discord.Status.online, activity=activity)
                self.status_buf = self.status
                # activityvar = discord.Activity(type=discord.ActivityType.custom, state="NAMEOFMYACTIVITY")
                # await self.client.change_presence(activity=activityvar)

        # メッセージ受信時に動作する処理
        @self.client.event
        async def on_message(message):
            # メッセージ送信者がBotだった場合は無視する
            if message.author.bot:
                return
            # 「/neko」と発言したら「にゃーん」が返る処理
            if message.content == '/neko':
                await message.channel.send('にゃーん')
                activity = discord.Game(name="ABC", emoji=None, type=4)
                await self.client.change_presence(status=discord.Status.idle, activity=activity)

        def maindisbot():
            self.client.run("ODI2MDgxNjc3NjE1OTU1OTg4.YGHSgw.B-UGUmwaAlirqasXIgLHDNF-0EU")

        thread1 = threading.Thread(target=maindisbot)
        thread1.start()

    def set_status(self, status):
        self.status = status

if __name__ == "__main__":
    ins = DiscordStatusClass()
    time.sleep(5)