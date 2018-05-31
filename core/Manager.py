import sys
import threading

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import *

from core.MessengerAPI.Authorization import Authorization
from core.MessengerAPI.MessengerAPI import Dialog, Message
from core.MessengerAPI.MessengerAPI import MessengerAPI
from core.UIInit import UIInit


class Manager(QObject):
    dialogsLoadedSignal = QtCore.pyqtSignal(list)
    loadUserDialogSignal = QtCore.pyqtSignal(list)
    reloadDialogsSignal = QtCore.pyqtSignal()

    onSettingsTab = False

    __authorization = None
    __messenger = None
    __ui = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentDial = None
        app = QApplication(sys.argv)
        # Handlers connect
        self.loadUserDialogSignal.connect(self.loadUserDialogHandler)
        self.dialogsLoadedSignal.connect(self.dialogsLoadedHandler)
        self.reloadDialogsSignal.connect(self.reloadDialogsHAndler)
        self.__authorization = Authorization.getInstance(self.reloadDialogsSignal)
        self.__ui = UIInit(self)
        self.__authorization.setWidget(self.__ui)
        self.__reloadDialogs()
        sys.exit(app.exec_())

    def __reloadDialogs(self):
        self.__ui.startLoadIndicator()
        self.__messenger = MessengerAPI(self.__authorization.getPrivateKeys())
        self.__ui.clearDialogs()
        threading.Thread(target=MessengerAPI.loadDialogs,
                         args=(self.__messenger, self.dialogsLoadedSignal)).start()

    def OpenSettings(self):
        self.onSettingsTab = True
        self.__ui.OpenSettings()
        pass

    def MessageMenuInit(self):
        self.onSettingsTab = False
        self.__ui.MessageMenuInit()
        pass

    def loginThrowVKGroup(self):
        self.__authorization.authorizationVKGroup()
        self.__reloadDialogs()
        pass

    def loginThrowFacebook(self):
        self.__authorization.authorizationFacebook()
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

    def sendMessage(self):
        if self.currentDial is not None:
            message = self.__ui.getMessageText()
            print(message)
            msgClass = Message({"text": message, "from_id": 0, "my_message": True,"attachments":[]})
            self.currentDial.sendMessage(msgClass)
            self.__ui.addMessageToLayoutToBottom(msgClass)
            self.__ui.clearMessageText()
            self.__ui.showFirstMessage()
        print("clicked")

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
            if self.onSettingsTab:
                self.MessageMenuInit()
            self.currentDial = self.__messenger[curr]['dialogs'][row - 1]
            self.__ui.startLoadIndicator()
            print(self.currentDial.__dict__)
            threading.Thread(target=Dialog.getMessages,
                             args=(self.currentDial, self.loadUserDialogSignal)).start()
            self.__ui.setUserToMenu(self.currentDial.getTitle(), self.currentDial.getIcon())
        print("----")
        pass

    @Slot(list, name="dialogsLoadedHandler")
    def dialogsLoadedHandler(self, mess):
        self.__messenger = mess
        self.loadDialogs()
        self.__ui.stopLoadingIndicator()

    @Slot(name="reloadDialogs")
    def reloadDialogsHAndler(self):
        print("emited")
        self.__reloadDialogs()

    @Slot(list,name="loadUserDialogHandler")
    def loadUserDialogHandler(self, messages):
        self.__ui.clearMessageLayout()
        for message in messages:
            self.__ui.addMessageToLayoutToTop(message)
        self.__ui.showFirstMessage()
        self.__ui.stopLoadingIndicator()


def main():
    ex = Manager()

if __name__ == '__main__':
    ex = Manager()
