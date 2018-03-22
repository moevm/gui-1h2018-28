import vk_api


class VKApi:
    __myId = None

    def __init__(self, authToken):
        self.vk_session = vk_api.VkApi(token=authToken)
        self.vkApi = self.vk_session.get_api()
        self.__myId = self.vkApi.users.get()[0]['id']
        pass

    def getDialog(self, user):
        pass

    def getMessagesByChat(self, chatId, offset):
        msg = self.getMessagesById("2000000000" + chatId, offset)
        print(msg)
        return msg



    def getMessagesById(self, userId, offset):
        '''
        [{
            "text": text,
            "attach":attach,
            "from_id":id
            "my_id":myId ...]
        '''
        messages = self.vkApi.messages.getHistory(user_id=userId, offset=offset)['items']
        msgToReturn = []
        for msg in messages:
            msgToReturn.append({'text': msg['body'],
                                'from_id': str(msg['from_id']), 'my_message': msg['from_id'] == self.__myId})

        return msgToReturn

    def getUserById(self, user_ids):
        return self.vkApi.users.get(user_ids=','.join(user_ids))

    def getGroupById(self, group_ids):
        return self.vkApi.groups.getById(group_ids=','.join(group_ids))

    def getMyDialogs(self):
        '''
        Format return v0.1
        [{
            "dialog_id":99999 (user_id or chat_id)
            "dialog_title":"Title"
            "last_message":Message
            "getMessages":Method to get more messages
        },...]
        '''
        dialogs = self.vkApi.messages.getDialogs()
        usersId = []
        groupsId = []
        itemsToReturn = []
        for dialog in dialogs['items']:
            if 'chat_id' in dialog['message']:
                itemsToReturn.append(
                    {"dialog_id": dialog['message']['chat_id'], "getMessages": self.getMessagesByChat,
                     "dialog_title": dialog['message']['title']})
            else:
                itemsToReturn.append({"dialog_id": dialog['message']['user_id'], "getMessages": self.getMessagesById,
                                      "dialog_title": "Unknown"})
                userHelpId = str(dialog['message']['user_id'])
                if userHelpId[0:1] != '-':
                    usersId.append(userHelpId)
                else:
                    groupsId.append(userHelpId[1:])
        userInfo = self.getUserById(usersId)
        groupInfo = self.getGroupById(groupsId)
        numUser = 0
        numGroup = 0
        for n, dialog in enumerate(dialogs['items']):
            if len(userInfo) > numUser:
                if userInfo[numUser]['id'] == dialog['message']['user_id']:
                    itemsToReturn[n]['dialog_title'] = userInfo[numUser]['first_name'] + ' ' + userInfo[numUser][
                        'last_name']
                    numUser += 1
            if len(groupInfo) > numGroup:
                if str(groupInfo[numGroup]['id']) == str(dialog['message']['user_id'])[1:]:
                    itemsToReturn[n]['dialog_title'] = groupInfo[numGroup]['name']
                    numGroup += 1

        return itemsToReturn

    def userInfo(self, user):
        pass

    def sendMessage(self, message):
        pass
