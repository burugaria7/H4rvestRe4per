from discord_webhook import DiscordWebhook

class DiscordBotClass:
    def __init__(self, url):
        self.url = url

    def send_msg(self, msg):
        webhook = DiscordWebhook(url=self.url, content=msg)
        response = webhook.execute()
