from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from urllib import request


class MessageWidget(QWidget):
    def __init__(self, message):
        super(MessageWidget, self).__init__(None)
        self.row = QHBoxLayout()
        self.row.setSpacing(0)
        if message.isMyMessage():
            self.row.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
            self.addMessageLayout(message, True)
            self.addLittleTriangle(self.row, True)
        else:
            self.addLittleTriangle(self.row, False)
            self.addMessageLayout(message, False)
            self.row.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.setLayout(self.row)

    def downloadImage(self, url):
        if os.path.exists(url):
            return url
        saveDir = './images/dialogAttachments/' + url[11:].replace('/', '.')
        if os.path.exists(saveDir):
            return saveDir
        else:
            request.urlretrieve(url, saveDir)
            return saveDir
        pass

    def addMessageLayout(self, message, rightSide):
        backgroundColor = QWidget()
        if rightSide:
            backgroundColor.setStyleSheet("background-color: #59f296;"
                                          " border-top-left-radius: 15px;"
                                          " border-top-right-radius: 15px;"
                                          " border-bottom-left-radius: 15px;")
        else:
            backgroundColor.setStyleSheet("background-color: #59f296;"
                                          " border-top-left-radius: 15px;"
                                          " border-top-right-radius: 15px;"
                                          " border-bottom-right-radius: 15px;")
        messageLayout = QVBoxLayout(backgroundColor)

        for attach in message.getAttachments():
            if attach.isSticker() or attach.isPhoto():
                sctickersButton = QPushButton()
                if attach.isPhoto():
                    sctickersButton.setIconSize(QSize(256, 256))
                else:
                    sctickersButton.setIconSize(QSize(128, 128))
                sctickersButton.setIcon(QIcon(self.downloadImage(attach.getUrl())))
                sctickersButton.setStyleSheet("background-color: transparent;")
                messageLayout.addWidget(sctickersButton)
            elif attach.isAudio() or attach.isVideo():
                audio = QLabel(attach.getBody())
                audio.setWordWrap(True)
                audio.setStyleSheet("background-color: transparent;")
                audio.setScaledContents(True)
                messageLayout.addWidget(audio)

        if message.getText() != "":
            label = QLabel(message.getText())
            label.setWordWrap(True)
            label.setStyleSheet("background-color: transparent;")
            label.setScaledContents(True)
            messageLayout.addWidget(label)
        self.row.addWidget(backgroundColor)

    @staticmethod
    def addLittleTriangle(lay, rightSide):
        row = QVBoxLayout()
        row.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        icon = QLabel()
        if rightSide:
            icon.setPixmap(QPixmap("./resources/rightTriangle.png"))
        else:
            icon.setPixmap(QPixmap("./resources/leftTriangle.png"))

        icon.setStyleSheet("background-color: transparent;")
        row.addWidget(icon)
        lay.addLayout(row)


class DialogWidget(QWidget):
    def __init__(self, name, lastMessage, logo, parent=None):
        super(DialogWidget, self).__init__(parent)
        self.row = QHBoxLayout()
        rect = QRect(2, 2, 33, 33)
        region = QRegion(rect, QRegion.Ellipse)
        sctickersButton = QPushButton()
        sctickersButton.setIconSize(QSize(35, 35))
        sctickersButton.setMask(region)
        sctickersButton.setIcon(logo)
        sctickersButton.setStyleSheet("background-color: white;border-radius: 17px;")
        self.row.addWidget(sctickersButton)
        lay = QVBoxLayout()
        lay.addWidget(QLabel(name if len(name) < 15 else name[0:15] + '...'))
        lay.addWidget(QLabel(lastMessage if len(lastMessage) < 15 else lastMessage[0:15] + '...'))
        self.row.addLayout(lay)
        self.row.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.setLayout(self.row)


class MessengerWidget(QWidget):
    def __init__(self, name, logo, msgLogo, parent=None):
        super(MessengerWidget, self).__init__(parent)
        self.setStyleSheet("background-color: 	#ADD8E6;")
        bac = QHBoxLayout()
        backgroundColor = QWidget()
        self.row = QHBoxLayout(backgroundColor)
        bac.setContentsMargins(0, 0, 0, 0)
        sctickersButton = QPushButton()
        sctickersButton.setIconSize(QSize(50, 50))
        sctickersButton.setStyleSheet("background-color: transparent;")
        rect = QRect(6, 6, 47, 47)
        region = QRegion(rect, QRegion.Ellipse)
        sctickersButton.setMask(region)
        sctickersButton.setIcon(logo)
        self.row.addWidget(sctickersButton)
        nameLabel = QLabel(name)
        self.row.addWidget(nameLabel)

        self.row.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        downButton = QPushButton()
        downButton.setIconSize(QSize(35, 35))
        downButton.setStyleSheet("background-color: transparent;")
        downButton.setIcon(QIcon('./resources/down_arrow.png'))
        self.row.addWidget(downButton)
        bac.addWidget(backgroundColor)
        self.setLayout(bac)

        messengerBtn = QPushButton(self)
        messengerBtn.setIconSize(QSize(20, 20))
        messengerBtn.setIcon(QIcon(msgLogo))
        messengerBtn.setStyleSheet("background-color: transparent;")
        messengerBtn.move(10, 40)
        messengerBtn.show()


class UIInit(QMainWindow):
    __manager = None
    LOAD_BAR_SIZE_HALF = 128

    def __init__(self, manager):
        super().__init__()
        self.profileBtn = QPushButton('Profile')
        self.iconProfile = QPushButton()
        self.__manager = manager
        # self.statusBar().showMessage('Ready')
        self.resize(800, 600)
        self.setWindowTitle('Messenger')
        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.messageText = None
        mainLayout = QHBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        wid.setLayout(mainLayout)

        leftMenu = QVBoxLayout()
        self.rightMenu = QVBoxLayout()
        self.rightMenu.setSpacing(0)
        self.rightSubMenu = QVBoxLayout()
        mainLayout.addLayout(leftMenu)
        mainLayout.addLayout(self.rightMenu)
        self.dialogList = QListWidget()
        self.dialogList.clicked.connect(manager.loadUserDialog)
        self.dialogList.setStyleSheet("""QListWidget{border: 0;}
                                        QScrollBar::handle:vertical {
                                            background: #DCDCDC;
                                            border-radius: 10px;
                                            min-height: 20px;
                                        }""")
        self.dialogList.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        leftMenu.addWidget(self.dialogList)
        self.dialogList.setMaximumSize(300, 10000)
        self.MessageMenuInit()

        self.loadingIndicator = QLabel(self)
        self.loadingIndicatorMovie = QMovie("./resources/loader.gif")
        self.loadingIndicator.setMovie(self.loadingIndicatorMovie)
        # self.loadingIndicator.adjustSize()
        self.loadingIndicator.resize(256, 256)
        self.loadingIndicator.move(200, 200)
        self.stopLoadingIndicator()
        self.show()

    def clearMessageText(self):
        self.messageText.setText("")

    def getMessageText(self):
        return self.messageText.toPlainText()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())
        self.rightMenu.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        pass

    def clearMessageLayout(self):
        self.messageList.clear()

    def OpenSettings(self):
        self.clearLayout(self.rightMenu)
        msgInit = QPushButton('Close')
        msgInit.clicked.connect(self.__manager.MessageMenuInit)
        self.rightMenu.addWidget(msgInit)
        telegramLogin = QPushButton('Login throw Telegram')
        telegramLogin.clicked.connect(self.__manager.loginThrowTelegram)
        self.rightMenu.addWidget(telegramLogin)
        vkLogin = QPushButton('Login throw VK')
        vkLogin.clicked.connect(self.__manager.loginThrowVK)
        self.rightMenu.addWidget(vkLogin)
        vkLogin = QPushButton('Login VK Group')
        vkLogin.clicked.connect(self.__manager.loginThrowVKGroup)
        self.rightMenu.addWidget(vkLogin)
        facebookLogin = QPushButton('Login throw Facebook')
        facebookLogin.clicked.connect(self.__manager.loginThrowFacebook)
        self.rightMenu.addWidget(facebookLogin)
        pass

    def clearDialogs(self):
        self.dialogList.clear()

    def addDialogToLayout(self, dialog):
        itemN = QListWidgetItem()
        # itemN.setSizeHint(QSize(100, 100))
        self.dialogList.addItem(itemN)
        row = DialogWidget(dialog.getTitle(), dialog.getLastMessage(), QIcon(dialog.getIcon()))
        itemN.setSizeHint(row.minimumSizeHint())
        # Associate the custom widget to the list entry
        self.dialogList.setItemWidget(itemN, row)
        # layout.setItemWidget(itemN, widget)

    def addMessengerToLayout(self, info):
        itemN = QListWidgetItem()
        self.dialogList.addItem(itemN)
        row = MessengerWidget(info['name'], QIcon(info['icon']), info['messenger_icon'])
        itemN.setSizeHint(row.minimumSizeHint())
        self.dialogList.setItemWidget(itemN, row)

    def stopLoadingIndicator(self):
        self.loadingIndicatorMovie.stop()
        self.loadingIndicator.setVisible(False)
        pass

    def startLoadIndicator(self):
        self.loadingIndicatorMovie.start()
        self.loadingIndicator.setVisible(True)
        pass

    def MessageMenuInit(self):
        self.clearLayout(self.rightMenu)
        self.addUserSubMenu(self.rightSubMenu)
        self.addMessageLayout(self.rightSubMenu)
        self.MessageWriteMenu(self.rightSubMenu)
        self.rightMenu.addLayout(self.rightSubMenu)

    def MessageWriteMenu(self, layout):
        msgEnter = QWidget()
        msgEnter.setStyleSheet("background-color:#bef3eb;")
        rightMessageEnter = QHBoxLayout(msgEnter)
        rightMessageEnter.setContentsMargins(0, 0, 0, 0)
        attachButton = QPushButton()
        attachButton.setIcon(QIcon('./resources/attachmentIcon.png'))
        attachButton.setIconSize(QSize(40, 40))
        attachButton.setStyleSheet("background-color: transparent")
        rightMessageEnter.addWidget(attachButton)
        self.messageText = QTextEdit()
        self.messageText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.messageText.setStyleSheet("border: 1px solid black;border-radius:5px;background-color:white;")
        self.messageText.setMaximumSize(10000, 35)
        rightMessageEnter.addWidget(self.messageText)
        sctickersButton = QPushButton()
        sctickersButton.setIcon(QIcon('./resources/smileIcon.png'))
        sctickersButton.setIconSize(QSize(30, 30))
        sctickersButton.setStyleSheet("background-color: transparent")
        rightMessageEnter.addWidget(sctickersButton)
        sendButton = QPushButton()
        sendButton.clicked.connect(self.__manager.sendMessage)
        sendButton.setIcon(QIcon('./resources/sendMessageIcon.png'))
        sendButton.setIconSize(QSize(30, 30))
        sendButton.setStyleSheet("background-color: transparent;margin-right:15px;")
        rightMessageEnter.addWidget(sendButton)
        layout.addWidget(msgEnter)

    def setUserToMenu(self, name, image):
        self.profileBtn.setText(name)
        self.iconProfile.setIcon(QIcon(image))
        pass

    def addMessageLayout(self, layout):
        bcgColor2 = QWidget()
        bcgColor2.setStyleSheet("background-color: white")
        rightMessageHistory = QVBoxLayout(bcgColor2)
        # rightMessageHistory.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.messageList = QListWidget()
        rightMessageHistory.setContentsMargins(0, 0, 0, 0)
        self.messageList.setStyleSheet("""QListWidget{border: 0;}
                                QScrollBar::handle:vertical {
                                    background: #DCDCDC;
                                    border-radius: 10px;
                                    min-height: 20px;
                                }""")
        # widgetList.setFlow(Qt.AlignBottom)
        self.messageList.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.messageList.verticalScrollBar().setSingleStep(5)
        self.messageList.horizontalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        rightMessageHistory.addWidget(self.messageList)
        layout.addWidget(bcgColor2)

    def addMessageToLayoutToTop(self, message):
        itemN = QListWidgetItem()
        self.messageList.insertItem(0, itemN)
        widget = MessageWidget(message)
        itemN.setSizeHint(widget.sizeHint())
        self.messageList.setItemWidget(itemN, widget)

    def addMessageToLayoutToBottom(self, message):
        itemN = QListWidgetItem()
        self.messageList.insertItem(99999, itemN)
        widget = MessageWidget(message)
        itemN.setSizeHint(widget.sizeHint())
        self.messageList.setItemWidget(itemN, widget)

    def showFirstMessage(self):
        self.messageList.scrollToBottom()

    def addUserSubMenu(self, layout):
        self.profileBtn = QPushButton('Profile')
        self.iconProfile = QPushButton()
        backgroundColor = QWidget()
        backgroundColor.setStyleSheet("background-color: #e3dcd6")
        rightSubMenu = QHBoxLayout(backgroundColor)
        self.iconProfile.setIcon(QIcon('./resources/testProfileLogo.png'))
        self.iconProfile.setIconSize(QSize(35, 35))
        self.iconProfile.setStyleSheet("background-color: transparent;border-radius: 17px;")
        rightSubMenu.addWidget(self.iconProfile)
        self.profileBtn.setStyleSheet("background-color: transparent;border-radius: 20px;font-size: 10pt;")
        rightSubMenu.addWidget(self.profileBtn)
        rightSubMenu.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        settingsButton = QPushButton()
        settingsButton.clicked.connect(self.__manager.OpenSettings)
        settingsButton.setIcon(QIcon('./resources/settingsIcon.png'))
        settingsButton.setIconSize(QSize(30, 30))
        settingsButton.setStyleSheet("background-color: transparent;margin-right:15px;")
        rightSubMenu.addWidget(settingsButton)
        layout.addWidget(backgroundColor)

    def resizeEvent(self, event):
        print("resize")
        self.loadingIndicator.move((self.width() / 2) - self.LOAD_BAR_SIZE_HALF,
                                   (self.height() / 2) - self.LOAD_BAR_SIZE_HALF)
