import sys
import threading

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import *

from MessengerAPI.Authorization import Authorization
from MessengerAPI.MessengerAPI import Dialog
from MessengerAPI.MessengerAPI import MessengerAPI
from UIInit import UIInit


class Manager(QObject):
    dialogsLoadedSignal = QtCore.pyqtSignal(list)
    loadUserDialogSignal = QtCore.pyqtSignal(list)

    __authorization = Authorization.getInstance(loadUserDialogSignal)
    __messenger = None
    __ui = None

    def __init__(self, parent=None):
        super().__init__(parent)
        app = QApplication(sys.argv)
        # Handlers connect
        self.loadUserDialogSignal.connect(self.loadUserDialogHandler)
        self.dialogsLoadedSignal.connect(self.dialogsLoadedHandler)

        self.__ui = UIInit(self)
        self.__authorization.setWidget(self.__ui)
        self.__reloadDialogs()
        sys.exit(app.exec_())

    def __reloadDialogs(self):
        self.__messenger = MessengerAPI(self.__authorization.getPrivateKeys())
        self.__ui.clearDialogs()
        threading.Thread(target=MessengerAPI.loadDialogs,
                         args=(self.__messenger, self.dialogsLoadedSignal)).start()

    @Slot(list, name="dialogsLoadedHandler")
    def dialogsLoadedHandler(self, mess):
        self.__messenger = mess
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

    def loginThrowTelegram(self):
        self.__authorization.authorizationTelegram()
        self.__reloadDialogs()
        pass

    def loadDialogs(self):
        for messenger in self.__messenger:
            self.__ui.addMessengerToLayout(messenger)
            if messenger['visibility'] is True:
                for dialog in messenger['dialogs']:
                    self.__ui.addDialogToLayout(dialog)
        pass

    def messengerSetHide(self, num, status):
        self.__messenger[num]['visibility'] = status
        self.__ui.clearDialogs()
        self.loadDialogs()

    @Slot(list, name="loadUserDialogHandler")
    def loadUserDialogHandler(self, messages):
        self.__ui.clearMessageLayout()
        for message in messages:
            self.__ui.addMessageToLayout(message)
        self.__ui.showFirstMessage()

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
            threading.Thread(target=Dialog.getMessages,
                             args=(self.__messenger[curr]['dialogs'][row - 1], self.loadUserDialogSignal)).start()
        print("----")
        pass


if __name__ == '__main__':
    ex = Manager()
