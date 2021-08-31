import requests

class Slack():
    def __init__(self):
        self.token = '####'
        self.channel = '#bot_test'

    def notification(self, text=None):
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={'Authorization':'Bearer '+self.token},
            data={'channel':self.channel, 'text':text})
        print('slack_connect status : ', response)

        