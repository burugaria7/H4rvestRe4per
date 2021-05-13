import discord
import random
import paypay
import buyonly
import gspread1
import watchprocess
import time
from discord.ext import tasks
client = discord.Client()

CHANNEL_ID = 825642205678272522 # 任意のチャンネルID(int)
@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)
    await greet()  # 挨拶する非同期関数を実行

async def greet():
    channel = client.get_channel(CHANNEL_ID)

@client.event
async def on_message(message):
    # 送信者がbotである場合は弾く
    if message.author.bot:
        return

    if message.content == "!show":
        paypay.myself_info2()
        # チャンネルに送る
        await message.channel.send(str(paypay.myself_info2()))
    elif message.content == "!profit":
        profit = buyonly.cul_profit(paypay.myself_info2())
        await message.channel.send("￥"+str(profit))
    elif message.content == "!status":
        status = gspread1.dis_readlist()
        await message.channel.send(str(status))
    elif message.content == "!log":
        log = watchprocess.dicord_logr()
        await message.channel.send(str(log))



client.run("ODI2MDgxNjc3NjE1OTU1OTg4.YGHSgw.B-UGUmwaAlirqasXIgLHDNF-0EU")