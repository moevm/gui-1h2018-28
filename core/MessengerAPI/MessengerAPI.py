from MessengerAPI.VKApi import VKApi


class Dialog:
    __dialogId = None
    __title = None
    __lastMessage = None
    __messages = None
    __api = None

    def __init__(self, dialog, api):
        self.__title = dialog['dialog_title']
        self.__getMess = dialog['getMessages']
        self.__dialogId = str(dialog['dialog_id'])
        print(dialog)
        pass

    def getTitle(self):
        return self.__title

    def getMessages(self, offset):
        return self.__getMess(self.__dialogId, offset)
        pass


class Message:
    def __init__(self, json):
        if json['messenger'] == "VK":
            self.parseMessageVK(json)
            return
        if json['messenger'] == "Telegram":
            self.parseMessageTelegram(json)
            return
        pass

    def parseMessageVK(self, json):
        pass

    def parseMessageTelegram(self, json):
        pass


class Attachments:
    def __init__(self, json):
        pass


class MessengerAPI:
    __messengerAPI = {'vk': [], 'telegram': []}
    __dialogs = []

    def __init__(self, authTokens):
        self.__createmessengerClasses(authTokens)
        self.loadDialogs()
        pass

    def loadDialogs(self):
        self.__dialogs = []

        for api in self.__messengerAPI:
            for mess in self.__messengerAPI[api]:
                print(mess.getMyDialogs())
                for dialog in mess.getMyDialogs():
                    self.__dialogs.append(Dialog(dialog, mess))

    def getDialogs(self):
        return self.__dialogs

    def getMessageByN(self, n, offset):
        return self.__dialogs[n].getMessages(offset)

    def __createmessengerClasses(self, authTokens):
        for mess in authTokens:
            for key in authTokens[mess]:
                if mess == "vk":
                    self.__messengerAPI['vk'].append(VKApi(key))

    def userInfo(self, user):
        pass

    def sendMessage(self, message):
        pass
