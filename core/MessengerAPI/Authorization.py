import sys
import os.path

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import Qt
import json
import pickle
from MessengerAPI.VKApi import VKApi
from MessengerAPI.MessengerAPI import MessengerAPI


class VKAuth(Qt.QDialog):
    def __init__(self, window, authHandler):
        super().__init__(window)
        layout = Qt.QVBoxLayout(self)
        self.label = Qt.QLabel("")
        wv = QWebEngineView()
        wv.page().profile().cookieStore().deleteAllCookies()
        wv.urlChanged.connect(authHandler)
        wv.load(QUrl(
            "https://oauth.vk.com/authorize?client_id=6374130&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,messages,offline&response_type=token&v=5.73"))
        layout.addWidget(wv)
        self.resize(400, 400)


class Authorization:
    # Here will be the instance stored.
    __instance = None
    # Here will be the private keys stored.
    __privateKeys = {"vk": [], "telegram": []}
    # Dialog with login form
    __loginDialog = None

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

    def getPrivateKeys(self):
        return self.__privateKeys



    def saveKeys(self):
        with open("privateKeys.pickle", "wb") as f:
            pickle.dump(self.__privateKeys, f)
        pass

    def authorizationVK(self, parent):
        self.__loginDialog = VKAuth(parent, self.vkUrlChangeHandler)
        self.__loginDialog.show()
        self.__loginDialog.exec_()

    def vkUrlChangeHandler(self, url):
        currentUrl = url.url()
        if currentUrl.find("https://oauth.vk.com/blank.html#access_token=") != -1:
            self.__privateKeys["vk"].append(currentUrl[45:currentUrl.find("&expires_in")])
            self.saveKeys()
            self.__loginDialog.close()