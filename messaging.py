from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError


class Line:
    def __init__(self, key, recipient):
        self.key = key
        self.recipient = recipient
        self.api = LineBotApi(key)

    def send(self, text):
        try:
            self.api.push_message(self.recipient, TextSendMessage(text=text))
        except LineBotApiError as e:
            print(e)
