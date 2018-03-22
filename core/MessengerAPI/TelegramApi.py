import telethon
from telethon import TelegramClient


class TelegramApi:
    api_id = 223447
    api_hash = '1827d8b0aa6334c8efc32f941d3559dc'

    def __init__(self, pathToSession):
        self.client = TelegramClient(pathToSession, self.api_id, self.api_hash)
        print(self.client.connect())
        self.client.get_dialogs()
        pass

    def getDialog(self, user):
        pass

    def getMessagesByChat(self, chatId, offset):
        return []

    '''
    [{
        "text": text,
        "attach":attach,
        "from_id":id
        "my_id":myId ...]
    '''

    def getMessagesById(self, userId, offset):
        return []

    def getUserById(self, user_ids):
        return []

    def getGroupById(self, group_ids):
        return []

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
        dialogs = []
        for dialog in self.client.get_dialogs(limit=10):
            print(dialog.entity.__dict__)
            if isinstance(dialog.entity, telethon.tl.types.User):
                dialogs.append({
                    "dialog_id": dialog.entity.id,
                    "dialog_title": str(dialog.entity.first_name) + str(dialog.entity.last_name),
                    "last_message": "last message",
                    "getMessages": self.getMessagesById
                })
            else:
                dialogs.append({
                    "dialog_id": dialog.entity.id,
                    "dialog_title": dialog.entity.title,
                    "last_message": "last message",
                    "getMessages": self.getMessagesById
                })
        return dialogs

    def userInfo(self, user):
        pass

    def sendMessage(self, message):
        pass
