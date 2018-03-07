import json

class Message():
    def __init__(self,json):
        if json['messenger'] == "VK":
            self.parseMessageVK(json)
            return
        if json['messenger'] == "Telegram":
            self.parseMessageTelegram(json)
            return
        pass
    
    def parseMessageVK(self,json):
        pass

    def parseMessageTelegram(self,json):
        pass