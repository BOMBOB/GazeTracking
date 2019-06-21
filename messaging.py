from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError


class Line:
    def __init__(self, key, recipient, dry):
        self.key = key
        self.recipient = recipient
        self.dry = dry
        self.api = LineBotApi(key)

    def send(self, text):
        try:
            if not self.dry:
                self.api.push_message(self.recipient, TextSendMessage(text=text))
            print('LINE message sent.', text)
        except LineBotApiError as e:
            print(e)
