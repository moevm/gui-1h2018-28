from MessengerAPI.TelegramApi import TelegramApi
from MessengerAPI.VKApi import VKApi


class Dialog:
    __dialogId = None
    __title = None
    __api = None

    def __init__(self, dialog):
        self.__messages = []
        self.__title = dialog['dialog_title']
        self.__getMess = dialog['getMessages']
        self.__dialogId = str(dialog['dialog_id'])
        pass

    def getTitle(self):
        return self.__title

    def loadMessages(self, offset):
        for msg in self.__getMess(self.__dialogId, offset):
            self.__messages.append(Message(msg))
        pass

    def getMessages(self):
        self.loadMessages(len(self.__messages))
        return self.__messages


class Message:
    __text = "Unknown"
    __fromId = "Unknown"
    __myMessage = False
    __attachments = None

    def __init__(self, message):
        self.__text = message['text']
        self.__fromId = message['from_id']
        self.__myMessage = message['my_message']
        pass

    def getText(self):
        return self.__text

    def isMyMessage(self):
        return self.__myMessage

    def fromId(self):
        return self.__fromId


class Attachments:
    def __init__(self, json):
        pass


class MessengerAPI:
    def __init__(self, authTokens):
        self.__messengerAPI = {'vk': [], 'telegram': []}
        self.__createmessengerClasses(authTokens)
        pass

    def loadDialogs(self):
        dialogs = []
        for api in self.__messengerAPI:
            for mess in self.__messengerAPI[api]:
                dial = mess.getMyDialogs()
                dialogs.append(
                    {'name': mess.getName(), 'visibility': True, 'size': len(dial) + 1, 'icon': mess.getPathIcon(),
                     'dialogs': []})
                for dialog in dial:
                    dialogs[-1]['dialogs'].append(Dialog(dialog))
        return dialogs

    def __createmessengerClasses(self, authTokens):
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
