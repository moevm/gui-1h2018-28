import sys

from PyQt5.QtWidgets import *

from MessengerAPI.Authorization import Authorization
from MessengerAPI.MessengerAPI import MessengerAPI
from UIInit import UIInit


class Manager():
    __authorization = Authorization.getInstance()
    __messenger = None
    __dialogs = None
    __ui = None

    def __init__(self):
        try:
            app = QApplication(sys.argv)
            self.__ui = UIInit(self)
            self.__authorization.setWidget(self.__ui)
            self.__messenger = MessengerAPI(self.__authorization.getPrivateKeys())
            self.__dialogs = self.__messenger.loadDialogs()
            print(self.__dialogs)
            self.loadDialogs()
            sys.exit(app.exec_())
        except BaseException as e:
            print(e)
            raise e

    def OpenSettings(self):
        self.__ui.OpenSettings()
        pass

    def MessageMenuInit(self):
        self.__ui.MessageMenuInit()
        pass

    def loginThrowVK(self):
        self.__authorization.authorizationVK()
        pass

    def loadDialogs(self):
        for dialog in self.__dialogs:
            self.__ui.addDialogToLayout(dialog.getTitle())
        pass

    def loginThowTelegram(self):
        self.__authorization.authorizationTelegram()
        pass

    def loadUserDialog(self, user):
        print(user.row())
        self.__ui.clearMessageLayout()
        for message in self.__dialogs[user.row()].getMessages():
            print(message.getText())
            self.__ui.addMessageToLayout(message.getText(), message.isMyMessage())
        print("----")
        pass


if __name__ == '__main__':
    ex = Manager()
