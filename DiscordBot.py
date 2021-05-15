from discord_webhook import DiscordWebhook
import discord
import threading
import asyncio
import time
from discord.ext import tasks

class DiscordBotClass:
    def __init__(self, url):
        self.url = url

    def send_msg(self, msg):
        webhook = DiscordWebhook(url=self.url, content=msg)
        response = webhook.execute()
