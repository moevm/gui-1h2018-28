import sys

from PyQt5.QtWidgets import *

from MessengerAPI.Authorization import Authorization
from MessengerAPI.MessengerAPI import MessengerAPI, Dialog
from UIInit import UIInit


class Manager:
    __authorization = Authorization.getInstance()
    __messenger = None
    __ui = None

    def __init__(self):
        try:
            app = QApplication(sys.argv)
            self.__ui = UIInit(self)
            self.__authorization.setWidget(self.__ui)
            self.__messenger = MessengerAPI(self.__authorization.getPrivateKeys())
            self.__messenger = self.__messenger.loadDialogs()
            self.loadDialogs()
            sys.exit(app.exec_())
        except BaseException as e:
            print(e)
            raise e

    def __reloadDialogs(self):
        self.__messenger = MessengerAPI(self.__authorization.getPrivateKeys())
        self.__ui.clearDialogs()
        self.__messenger = self.__messenger.loadDialogs()
        print(self.__messenger)
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
        for messenger in self.__messenger:
            self.__ui.addMessengerToLayout(messenger)
            if messenger['visibility'] is True:
                for dialog in messenger['dialogs']:
                    self.__ui.addDialogToLayout(dialog.getTitle())
        pass

    def messengerSetHide(self, num, status):
        self.__messenger[num]['visibility'] = status
        self.__ui.clearDialogs()
        self.loadDialogs()

    def loadUserDialog(self, user):
        print(user.row())
        row = user.row()
        curr = 0
        while row >= self.__messenger[curr]['size'] or (self.__messenger[curr]['visibility'] is False and row is not 0):
            if self.__messenger[curr]['visibility'] is True:
                row -= self.__messenger[curr]['size']
            else:
                row -= 1
            curr += 1
        if row == 0:
            self.messengerSetHide(curr, not self.__messenger[curr]['visibility'])
        else:
            self.__ui.clearMessageLayout()
            for message in self.__messenger[curr]['dialogs'][row - 1].getMessages():
                self.__ui.addMessageToLayout(message.getText(), message.isMyMessage())
        print("----")
        pass


if __name__ == '__main__':
    ex = Manager()
