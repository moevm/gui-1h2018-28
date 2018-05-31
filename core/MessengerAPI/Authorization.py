import pickle

import os.path
from PyQt5 import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton
from telethon import TelegramClient

from core.MessengerAPI.TelegramApi import TelegramApi


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
        self.resize(600, 400)


class FacebookAuth(Qt.QDialog):
    def __init__(self, window, authHandler):
        super().__init__(window)
        layout = Qt.QVBoxLayout(self)
        self.label = Qt.QLabel("")
        wv = QWebEngineView()
        wv.page().profile().cookieStore().deleteAllCookies()
        wv.urlChanged.connect(authHandler)
        wv.load(QUrl(
            "https://www.facebook.com/v3.0/dialog/oauth?client_id=1057443961071784&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=pages_messaging,user_friends"))
        layout.addWidget(wv)
        self.resize(600, 400)


class EnterDialog(Qt.QDialog):
    def __init__(self, window, hander, labelText, buttonText):
        super().__init__(window)
        layout = Qt.QVBoxLayout(self)
        layout.addWidget(QLabel(labelText))
        self.lineEdit = QLineEdit()
        btn = QPushButton(buttonText)
        btn.clicked.connect(hander)
        layout.addWidget(self.lineEdit)
        layout.addWidget(btn)


class Authorization:
    # Here will be the instance stored.
    __instance = None
    # Here will be the private keys VK stored and telegram : telethon clients
    __privateKeys = {"vk": [], "telegram": [], "facebook": []}
    # Dialog with login form
    __loginDialog = None
    # widget main window
    __window = None
    # auth handler
    __authHandler = None

    @staticmethod
    def getInstance(handler):
        """ Static access method. """
        if Authorization.__instance is None:
            Authorization(handler)
        return Authorization.__instance

    def __init__(self, authHandler):
        """ Virtually private constructor. """
        if Authorization.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Authorization.__instance = self
            self.__authHandler = authHandler
        # Parse file with privateKey
        if os.path.exists("privateKeys.pickle"):
            with open("privateKeys.pickle", "rb") as f:
                self.__privateKeys = pickle.load(f)
                print(self.__privateKeys)
            self.saveKeys()
        else:
            self.saveKeys()

    def setWidget(self, widget):
        self.__window = widget
        pass

    def getPrivateKeys(self):
        return self.__privateKeys

    def setTelephone(self):
        self.userTel = self.__loginDialog.lineEdit.text()
        print(self.userTel)
        self.__loginDialog.close()
        print(TelegramApi.api_id, TelegramApi.api_hash)
        try:
            self.__telegaClient = TelegramClient('telegram.' + self.userTel + '.session', TelegramApi.api_id,
                                                 TelegramApi.api_hash)
            self.__telegaClient.connect()
            self.__telegaClient.send_code_request(self.userTel)
            self.__loginDialog = EnterDialog(self.__window, self.codeSetHandler, str(self.userTel) + "\nEnter code:",
                                             "Ok")
            self.__loginDialog.show()
            self.__loginDialog.exec_()
        except Exception as e:
            print(e)

    def authorizationVKGroup(self):
        self.__loginDialog = EnterDialog(self.__window, self.groupApiKey, "Enter key", "Ok")
        self.__loginDialog.show()
        self.__loginDialog.exec_()
        print("loginThrowVKGroup")
        pass

    def groupApiKey(self):
        self.__privateKeys['vk'].append(self.__loginDialog.lineEdit.text())
        self.saveKeys()
        self.__authHandler.emit()
        self.__loginDialog.close()
        pass

    def codeSetHandler(self):
        try:
            self.__telegaClient.sign_in(self.userTel, self.__loginDialog.lineEdit.text())
            self.__privateKeys['telegram'].append('telegram.' + self.userTel + '.session')
            self.saveKeys()
            self.__loginDialog.close()
            self.__authHandler.emit()
        except Exception as e:
            print(e)
        finally:
            self.__loginDialog.close()
        # todo: check error, and save user phone

    def authorizationTelegram(self):
        self.__loginDialog = EnterDialog(self.__window, self.setTelephone, "Enter phone", "Ok")
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
        self.__authHandler.emit()

    def authorizationFacebook(self):
        self.__loginDialog = FacebookAuth(self.__window, self.facebookUrlChangeHandler)
        self.__loginDialog.show()
        self.__loginDialog.exec_()
        self.__authHandler.emit()

    def vkUrlChangeHandler(self, url):
        currentUrl = url.url()
        if currentUrl.find("https://oauth.vk.com/blank.html#access_token=") != -1:
            self.__privateKeys["vk"].append(currentUrl[45:currentUrl.find("&expires_in")])
            self.saveKeys()
            self.__loginDialog.close()

    def facebookUrlChangeHandler(self, url):
        currentUrl = url.url()
        print(currentUrl)
        if currentUrl.find("https://www.facebook.com/connect/login_success.html") != -1:
            print(currentUrl[57:])
            self.__privateKeys["facebook"].append(currentUrl[57:])
            self.saveKeys()
            self.__loginDialog.close()
