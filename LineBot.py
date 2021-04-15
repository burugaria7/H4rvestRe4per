import requests


class LineBotClass:

    def __init__(self, url, access_token):
        self.url = url
        self.access_token = access_token
        self.headers = {'Authorization': 'Bearer ' + access_token}
        print("こちらLineBot: "+self.access_token+" どうぞー？")

    def send_msg(self, msg):
        payload = {'message': msg}
        requests.post(self.url, headers=self.headers, params=payload)

    def send_img(self, msg, path):
        files = {'imageFile': open(path, 'rb')}
        payload = {'message': msg}
        requests.post(self.url, headers=self.headers, params=payload, files=files, )
