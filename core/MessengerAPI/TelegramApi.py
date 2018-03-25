import telethon
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel


class TelegramApi:
    api_id = 223447
    api_hash = '1827d8b0aa6334c8efc32f941d3559dc'

    def __init__(self, pathToSession):
        self.client = TelegramClient(pathToSession, self.api_id, self.api_hash)
        print(self.client.connect())
        pass

    def getName(self):
        return "telegram testName"

    def getPathIcon(self):
        return '../resources/telegram_logo.png'

    def getDialog(self, user):
        pass

    def getMessagesByChat(self, chatId, offset):
        print(chatId)
        return []


    def getMessagesById(self, userId, offset):
        """
        [{
            "text": text,
            "attach":attach,
            "from_id":id
            "my_id":myId ...]
        """
        print(userId)
        print(PeerUser(userId))
        print(self.client.get_message_history(userId))
        return []

    def getMessagesByChannelId(self, userId, offset):
        print("get by channel id")
        return self.getMsgsByPeer(PeerChannel(int(userId)))

    def getMessagesByChatId(self, userId, offset):
        print("get by chat id")
        return self.getMsgsByPeer(PeerChat(int(userId)))

    def getMessagesByUserId(self, userId, offset):
        print("get by user id")
        return self.getMsgsByPeer(PeerUser(int(userId)))

    def getMsgsByPeer(self, peer):
        msgs = self.client.get_message_history(self.client.get_entity(peer))
        return [{"text": self.parseMessage(x), "my_message": True, "from_id": 1} for x in msgs]

    def parseMessage(self, msg):
        if getattr(msg, 'media', None):
            print("---------- MEDIA -----------")
            print(msg.media.__dict__)
            print("---------- END -----------")
            return '<{}> {}'.format(type(msg.media).__name__, msg.message)
        elif hasattr(msg, 'message'):
            print("---------- MESSAGE -----------")
            print(msg.message)
            print("---------- END -----------")
            return msg.message
        elif hasattr(msg, 'action'):
            print("---------- ACTION -----------")
            print(msg.action.__dict__)
            print("---------- END -----------")
            return str(msg.action)
        else:
            # Unknown message, simply print its class name
            print("---------- Unknown -----------")
            print(msg.__dict__)
            print("---------- END -----------")
            return type(msg).__name__


    def getUserById(self, user_ids):
        return []

    def getGroupById(self, group_ids):
        return []

    def getMyDialogs(self):
        """
        Format return v0.1
        [{
            "dialog_id":99999 (user_id or chat_id)
            "dialog_title":"Title"
            "last_message":Message
            "getMessages":Method to get more messages
        },...]
        """
        dialogs = []
        for dialog in self.client.get_dialogs(limit=10):
            print(dialog.entity.__dict__)
            if isinstance(dialog.entity, telethon.tl.types.User):
                dialogs.append({
                    "dialog_id": dialog.dialog.peer.user_id,
                    "dialog_title": str(dialog.entity.first_name) +' '+ str(dialog.entity.last_name),
                    "last_message": "last message",
                    "getMessages": self.getMessagesByUserId
                })
            else:
                if isinstance(dialog.entity, telethon.tl.types.Channel):
                    dialogs.append({
                        "dialog_id": dialog.dialog.peer.channel_id,
                        "dialog_title": dialog.entity.title,
                        "last_message": "last message",
                        "getMessages": self.getMessagesByChannelId
                    })
                else:
                    dialogs.append({
                        "dialog_id": dialog.dialog.peer.chat_id,
                        "dialog_title": dialog.entity.title,
                        "last_message": "last message",
                        "getMessages": self.getMessagesByChatId
                    })
        return dialogs

    def userInfo(self, user):
        pass

    def sendMessage(self, message):
        pass
