import PyQt5
from PyQt5.QtCore import pyqtSignal as Signal

from core.MessengerAPI.TelegramApi import TelegramApi
from core.MessengerAPI.VKApi import VKApi


class Dialog:
    __dialogId = None
    __title = None
    __api = None
    getMessagesSignal = Signal(PyQt5.QtCore.pyqtBoundSignal)

    def __init__(self, dialog):
        # super().__init__(parent)
        self.__messages = []
        self.__lastMessage = dialog['message']
        self.__iconPath = dialog['dialog_photo']
        self.__title = dialog['dialog_title']
        self.__getMess = dialog['getMessages']
        self.__sendMess = dialog['sendMessage']
        self.__dialogId = str(dialog['dialog_id'])

    def getLastMessage(self):
        return self.__lastMessage

    def getTitle(self):
        return self.__title

    def loadMessages(self, offset):
        for msg in self.__getMess(self.__dialogId, offset):
            self.__messages.append(Message(msg))
        pass

    def getMessages(self, signal):
        # self.__messages.clear()
        self.loadMessages(len(self.__messages))
        print(type(self.__messages))
        signal.emit(self.__messages)

    def getIcon(self):
        return self.__iconPath

    def sendMessage(self, message):
        print("sendMessage to id-" + str(self.__dialogId))
        self.__lastMessage = message.getText()
        self.__messages.insert(0, message)
        self.__sendMess(self.__dialogId, message.getText())


class Message:
    __text = "Unknown"
    __fromId = "Unknown"
    __myMessage = False
    __attachments = None

    def __init__(self, message):
        self.__text = message['text']
        self.__fromId = message['from_id']
        self.__myMessage = message['my_message']
        self.__attachments = []
        for attach in message['attachments']:
            self.__attachments.append(Attachment(attach))

    def getAttachments(self):
        return self.__attachments

    def getText(self):
        return self.__text

    def isMyMessage(self):
        return self.__myMessage

    def fromId(self):
        return self.__fromId


class Attachment:

    def __init__(self, json):
        print(json)
        self.__type = json['type']
        self.__url = json['url']
        if 'body' in json:
            self.__body = json['body']
        pass

    def isSticker(self):
        return self.__type == "sticker"

    def isPhoto(self):
        return self.__type == "photo"

    def isAudio(self):
        return self.__type == "audio"

    def isVideo(self):
        return self.__type == "video"

    def getUrl(self):
        return self.__url

    def getBody(self):
        return self.__body

class MessengerAPI:
    def __init__(self, authTokens):
        self.__messengerAPI = {'vk': [], 'telegram': [], 'facebook': []}
        self.__createMessengerClasses(authTokens)
        pass

    def loadDialogs(self, handler):
        dialogs = []
        for api in self.__messengerAPI:
            for mess in self.__messengerAPI[api]:
                dial = mess.getMyDialogs()
                dialogs.append(
                    {'name': mess.getName(), 'messenger_icon': mess.getMessengerIcon(), 'visibility': True,
                     'size': len(dial) + 1, 'icon': mess.getPathIcon(),
                     'dialogs': []})
                for dialog in dial:
                    dd = Dialog(dialog)
                    dialogs[-1]['dialogs'].append(dd)
        handler.emit(dialogs)

    def __createMessengerClasses(self, authTokens):
        for mess in authTokens:
            for key in authTokens[mess]:
                if mess == "vk":
                    self.__messengerAPI['vk'].append(VKApi(key))
                if mess == "telegram":
                    self.__messengerAPI['telegram'].append(TelegramApi(key))

    def userInfo(self, user):
        pass

    def sendMessage(self, message):
        pass
