import os.path
import pickle

from PyQt5 import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton
from telethon import TelegramClient

from MessengerAPI.TelegramApi import TelegramApi


class VKAuth(Qt.QDialog):
    def __init__(self, window, authHandler):
        super().__init__(window)
        layout = Qt.QVBoxLayout(self)
        self.label = Qt.QLabel("")
        wv = QWebEngineView()
        wv.page().profile().cookieStore().deleteAllCookies()
        wv.urlChanged.connect(authHandler)
        wv.load(QUrl(
            "https://oauth.vk.com/authorize?client_id=6374130&display=page&redirect_uri=https://oauth.vk.com/"
            "blank.html&scope=friends,messages,offline&response_type=token&v=5.73"))
        layout.addWidget(wv)
        self.resize(400, 400)


class TelegramAuth(Qt.QDialog):
    def __init__(self, window, phoneSetHander):
        super().__init__(window)
        layout = Qt.QVBoxLayout(self)
        layout.addWidget(QLabel("Telephone number:"))
        self.lineEdit = QLineEdit()
        btn = QPushButton("Set telephone")
        btn.clicked.connect(phoneSetHander)
        layout.addWidget(self.lineEdit)
        layout.addWidget(btn)


class TelegramCheckCode(Qt.QDialog):
    def __init__(self, window, phone, codeSetHander):
        super().__init__(window)
        layout = Qt.QVBoxLayout(self)
        layout.addWidget(QLabel(str(phone)))
        layout.addWidget(QLabel("Enter code:"))
        self.lineEdit = QLineEdit()
        btn = QPushButton("Set telephone")
        btn.clicked.connect(codeSetHander)
        layout.addWidget(self.lineEdit)
        layout.addWidget(btn)

class Authorization:
    # Here will be the instance stored.
    __instance = None
    # Here will be the private keys stored.
    __privateKeys = {"vk": [], "telegram": []}
    # Dialog with login form
    __loginDialog = None
    # widget main window
    __window = None


    @staticmethod
    def getInstance():
        """ Static access method. """
        if Authorization.__instance is None:
            Authorization()
        return Authorization.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Authorization.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Authorization.__instance = self
        # Parse file with privateKey
        if os.path.exists("privateKeys.pickle"):
            with open("privateKeys.pickle", "rb") as f:
                self.__privateKeys = pickle.load(f)
                print(self.__privateKeys)
        else:
            self.saveKeys()

    def setWidget(self, widget):
        self.__window = widget

    def getPrivateKeys(self):
        return self.__privateKeys

    def setTelephone(self):
        self.userTel = self.__loginDialog.lineEdit.text()
        print(self.userTel)
        self.__loginDialog.close()
        print(TelegramApi.api_id, TelegramApi.api_hash)
        self.__telegaClient = TelegramClient('telegram.' + self.userTel + '.session', TelegramApi.api_id,
                                             TelegramApi.api_hash)
        self.__telegaClient.connect()
        self.__telegaClient.send_code_request(self.userTel)
        self.__loginDialog = TelegramCheckCode(self.__window, self.userTel, self.codeSetHandler)
        self.__loginDialog.show()
        self.__loginDialog.exec_()

    def codeSetHandler(self):
        print(self.__loginDialog.lineEdit.text())
        self.__telegaClient.sign_in(self.userTel, self.__loginDialog.lineEdit.text())
        # todo: check error, and save user phone

    def authorizationTelegram(self):
        self.__loginDialog = TelegramAuth(self.__window, self.setTelephone)
        self.__loginDialog.show()
        self.__loginDialog.exec_()

    def saveKeys(self):
        with open("privateKeys.pickle", "wb") as f:
            pickle.dump(self.__privateKeys, f)
        pass

    def authorizationVK(self):
        self.__loginDialog = VKAuth(self.__window, self.vkUrlChangeHandler)
        self.__loginDialog.show()
        self.__loginDialog.exec_()

    def vkUrlChangeHandler(self, url):
        currentUrl = url.url()
        if currentUrl.find("https://oauth.vk.com/blank.html#access_token=") != -1:
            self.__privateKeys["vk"].append(currentUrl[45:currentUrl.find("&expires_in")])
            self.saveKeys()
            self.__loginDialog.close()