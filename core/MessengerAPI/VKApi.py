import vk_api
import json


class VKApi:
    def __init__(self, authToken):
        self.vk_session = vk_api.VkApi(token=authToken)
        self.vkApi = self.vk_session.get_api()
        pass

    def getDialog(self, user):
        pass

    def getMessagesByChat(self, chatId, offset):
        return self.getMessagesById("2000000000" + chatId, offset)

    def getMessagesById(self, userId, offset):
        return self.vkApi.messages.getHistory(user_id=userId, offset=offset)

    def getUserById(self, user_ids):
        return self.vkApi.users.get(user_ids=','.join(user_ids))

    def getGroupById(self, group_ids):
        return self.vkApi.groups.getById(group_ids=','.join(group_ids))

    '''
    Format return v0.1
    [{
        "dialog_id":99999 (user_id or chat_id)
        "dialog_title":"Title"
        "last_message":Message
        "getMessages":Method to get more messages
    },...]
    '''

    def getMyDialogs(self):
        dialogs = self.vkApi.messages.getDialogs()
        print(dialogs)
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
        print(groupInfo)
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
