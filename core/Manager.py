import sys

from PyQt5.QtWidgets import *

from MessengerAPI.Authorization import Authorization
from MessengerAPI.MessengerAPI import MessengerAPI, Dialog
from UIInit import UIInit


class Manager:
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
            self.loadDialogs()
            sys.exit(app.exec_())
        except BaseException as e:
            print(e)
            raise e

    def __reloadDialogs(self):
        self.__messenger = MessengerAPI(self.__authorization.getPrivateKeys())
        self.__ui.clearDialogs()
        self.__dialogs = self.__messenger.loadDialogs()
        print(self.__dialogs)
        self.loadDialogs()

    def OpenSettings(self):
        self.__ui.OpenSettings()
        pass

    def MessageMenuInit(self):
        self.__ui.MessageMenuInit()
        pass

    def loginThrowVKGroup(self):
        self.__authorization.loginThrowVKGroup()
        self.__reloadDialogs()
        pass

    def loginThrowVK(self):
        self.__authorization.authorizationVK()
        self.__reloadDialogs()
        pass

    def loginThowTelegram(self):
        self.__authorization.authorizationTelegram()
        self.__reloadDialogs()
        pass

    def loadDialogs(self):
        for dialog in self.__dialogs:
            if isinstance(dialog, Dialog):
                self.__ui.addDialogToLayout(dialog.getTitle())
            else:
                self.__ui.addMessengerToLayout(dialog)
        pass

    def loadUserDialog(self, user):
        print(user.row())
        if not isinstance(self.__dialogs[user.row()], Dialog):
            return
        self.__ui.clearMessageLayout()
        for message in self.__dialogs[user.row()].getMessages():
            self.__ui.addMessageToLayout(message.getText(), message.isMyMessage())

        print("----")
        pass


if __name__ == '__main__':
    ex = Manager()
