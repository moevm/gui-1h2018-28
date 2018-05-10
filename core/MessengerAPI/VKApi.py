import os
from urllib import request

import vk_api


class VKApi:
    __myId = None

    def __init__(self, authToken):
        self.vk_session = vk_api.VkApi(token=authToken)
        self.vkApi = self.vk_session.get_api()
        userName = self.vkApi.users.get(fields='photo_50')
        self.__userIcon = '../resources/testProfileLogo.png'
        if len(userName) is 0:
            group = self.vkApi.groups.getById()
            self.__myId = group[0]['id']
            self.__userIcon = self.downloadImage(group[0]['photo_50'])
            self.__userName = group[0]['name']
            print(group)
        else:
            self.__myId = userName[0]['id']
            self.__userIcon = self.downloadImage(userName[0]['photo_50'])
            self.__userName = userName[0]['first_name'] + ' ' + userName[0]['last_name']
            print(userName)
        pass

    def downloadImage(self, url):
        saveDir = './images/vkAPI/' + url[11:].replace('/', '.')
        if os.path.exists(saveDir):
            return saveDir
        else:
            request.urlretrieve(url, saveDir)
            return saveDir
        pass

    def getName(self):
        return self.__userName

    def getPathIcon(self):
        return self.__userIcon

    def sendMessage(self):
        print("ggg")
        pass

    def getDialog(self, user):
        pass

    def getMessagesByChat(self, chatId, offset):
        print("chat")
        print(chatId)
        msg = self.getMessagesById(str(2000000000 + int(chatId)), offset)
        return msg

    def getMessagesById(self, userId, offset):
        messages = self.vkApi.messages.getHistory(user_id=userId, offset=int(offset))['items']
        msgToReturn = []
        for msg in messages:
            attachments = []
            if 'attachments' in msg:
                for attach in msg['attachments']:
                    if attach['type'] == 'sticker':
                        attachments.append({"type": 'sticker', "url": attach['sticker']['photo_256']})
                    elif attach['type'] == 'audio':
                        attachments.append(
                            {"type": 'audio', "duration": attach['audio']['duration'],
                             "body": attach['audio']['artist'] + '-' + attach['audio']['title'],
                             "url": attach['audio']['url']})
                    elif attach['type'] == 'video':
                        print(attach)
                        attachments.append({"type": 'video', "body": attach['video']['title'], "url": "Hmm"})
                    elif attach['type'] == 'photo':
                        attachments.append({"type": 'photo', "url": attach['photo']['photo_604']})

            msgToReturn.append({'text': msg['body'],
                                "attachments": attachments,
                                'from_id': str(msg['from_id']), 'my_message': msg['out'] == 1})

        return msgToReturn

    def getUserById(self, user_ids):
        return self.vkApi.users.get(user_ids=','.join(user_ids), fields='photo_50')

    def getGroupById(self, group_ids):
        return self.vkApi.groups.getById(group_ids=','.join(group_ids), fields='photo_50')

    def getMyDialogs(self):
        dialogs = self.vkApi.messages.getDialogs()
        usersId = []
        groupsId = []
        itemsToReturn = []
        for dialog in dialogs['items']:
            if 'chat_id' in dialog['message']:
                itemsToReturn.append(
                    {"dialog_id": dialog['message']['chat_id'],
                     "message": dialog['message']['body'],
                     "dialog_photo": self.downloadImage(dialog['message']['photo_50'])
                     if 'photo_50' in dialog['message'] else '../resources/testProfileLogo.png',
                     "sendMessage": self.sendMessageToChat,
                     "getMessages": self.getMessagesByChat, "dialog_title": dialog['message']['title']})
            else:
                itemsToReturn.append({"dialog_id": dialog['message']['user_id'], "getMessages": self.getMessagesById,
                                      "message": dialog['message']['body'],
                                      "dialog_photo": '../resources/testProfileLogo.png',
                                      "sendMessage": self.sendMessage,
                                      "dialog_title": "Unknown"})
                userHelpId = str(dialog['message']['user_id'])
                if userHelpId[0:1] != '-':
                    usersId.append(userHelpId)
                else:
                    groupsId.append(userHelpId[1:])
        if len(usersId) > 0:
            userInfo = self.getUserById(usersId)
        else:
            userInfo = []
        if len(groupsId) > 0:
            groupInfo = self.getGroupById(groupsId)
        else:
            groupInfo = []
        numUser = 0
        numGroup = 0
        for n, dialog in enumerate(dialogs['items']):
            if len(userInfo) > numUser:
                if 'chat_id' not in dialog['message'] and userInfo[numUser]['id'] == dialog['message']['user_id']:
                    itemsToReturn[n]['dialog_title'] = userInfo[numUser]['first_name'] + ' ' + userInfo[numUser][
                        'last_name']
                    itemsToReturn[n]['dialog_photo'] = self.downloadImage(userInfo[numUser]['photo_50'])
                    numUser += 1
            if len(groupInfo) > numGroup:
                if str(groupInfo[numGroup]['id']) == str(dialog['message']['user_id'])[1:]:
                    itemsToReturn[n]['dialog_title'] = groupInfo[numGroup]['name']
                    itemsToReturn[n]['dialog_photo'] = self.downloadImage(groupInfo[numGroup]['photo_50'])
                    numGroup += 1
        print(itemsToReturn)
        return itemsToReturn

    def getMessengerIcon(self):
        return '../resources/vk_logo.png'

    def userInfo(self, user):
        pass

    def sendMessageToChat(self, id, message):
        self.sendMessage(str(2000000000 + int(id)), message)

    # def sendMessageToGroup(self, id, message):
    #   self.sendMessage('-' + str(id), message)

    def sendMessage(self, id, message):
        self.vkApi.messages.send(user_id=id, message=message)
        pass
