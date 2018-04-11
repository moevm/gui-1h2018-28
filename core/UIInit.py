from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class messageWiget(QWidget):
    def __init__(self, message):
        super(messageWiget, self).__init__(None)
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
            icon.setPixmap(QPixmap("../resources/rightTriangle.png"))
        else:
            icon.setPixmap(QPixmap("../resources/leftTriangle.png"))

        icon.setStyleSheet("background-color: transparent;")
        row.addWidget(icon)
        lay.addLayout(row)


class MyCustomWidget(QWidget):
    def __init__(self, name, lastMessage, logo, parent=None):
        super(MyCustomWidget, self).__init__(parent)
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
        self.row = QHBoxLayout()
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
        downButton.setIcon(QIcon('../resources/down_arrow.png'))
        self.row.addWidget(downButton)
        self.setLayout(self.row)

        messengerBtn = QPushButton(self)
        messengerBtn.setIconSize(QSize(20, 20))
        messengerBtn.setIcon(QIcon(msgLogo))
        messengerBtn.setStyleSheet("background-color: transparent;")
        messengerBtn.move(10, 40)
        messengerBtn.show()


class UIInit(QMainWindow):
    __manager = None

    def __init__(self, manager):
        super().__init__()
        self.__manager = manager
        # self.statusBar().showMessage('Ready')
        self.resize(800, 600)
        self.setWindowTitle('Messenger')
        wid = QWidget(self)
        self.setCentralWidget(wid)

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
        leftMenu.addWidget(self.dialogList)
        self.dialogList.setMaximumSize(300, 10000)
        self.MessageMenuInit()

        self.loadingIndicator = QLabel()
        # TODO loading indictor need realization

        self.show()
        pass

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
        pass

    def clearDialogs(self):
        self.dialogList.clear()

    def addDialogToLayout(self, dialog):
        itemN = QListWidgetItem()
        # itemN.setSizeHint(QSize(100, 100))
        self.dialogList.addItem(itemN)
        row = MyCustomWidget(dialog.getTitle(), dialog.getLastMessage(), QIcon(dialog.getIcon()))
        itemN.setSizeHint(row.minimumSizeHint())
        # Associate the custom widget to the list entry
        self.dialogList.setItemWidget(itemN, row)
        # layout.setItemWidget(itemN, widget)

    def addMessengerToLayout(self, info):
        '''
        Adding user profile in messenger to layout
        :param info:
        :return:
        '''
        itemN = QListWidgetItem()
        self.dialogList.addItem(itemN)
        row = MessengerWidget(info['name'], QIcon(info['icon']), info['messenger_icon'])
        itemN.setSizeHint(row.minimumSizeHint())
        self.dialogList.setItemWidget(itemN, row)

    def startLoadIndicator(self):
        # TODO need realization
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
        attachButton.setIcon(QIcon('../resources/attachmentIcon.png'))
        attachButton.setIconSize(QSize(40, 40))
        attachButton.setStyleSheet("background-color: transparent")
        rightMessageEnter.addWidget(attachButton)
        lineEdit = QTextEdit()
        lineEdit.setPlainText("Enter message...")
        lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        lineEdit.setStyleSheet("border: 1px solid black;border-radius:5px;background-color:white;")
        lineEdit.setMaximumSize(10000, 35)
        rightMessageEnter.addWidget(lineEdit)
        sctickersButton = QPushButton()
        sctickersButton.setIcon(QIcon('../resources/smileIcon.png'))
        sctickersButton.setIconSize(QSize(30, 30))
        sctickersButton.setStyleSheet("background-color: transparent")
        rightMessageEnter.addWidget(sctickersButton)
        sendButton = QPushButton()
        sendButton.setIcon(QIcon('../resources/sendMessageIcon.png'))
        sendButton.setIconSize(QSize(30, 30))
        sendButton.setStyleSheet("background-color: transparent;margin-right:15px;")
        rightMessageEnter.addWidget(sendButton)
        layout.addWidget(msgEnter)

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
        rightMessageHistory.addWidget(self.messageList)
        layout.addWidget(bcgColor2)

    def addMessageToLayout(self, message):
        itemN = QListWidgetItem()
        self.messageList.insertItem(0, itemN)
        widget = messageWiget(message)
        itemN.setSizeHint(widget.sizeHint())
        self.messageList.setItemWidget(itemN, widget)

    def showFirstMessage(self):
        self.messageList.scrollToBottom()

    def addUserSubMenu(self, layout):
        backgroundColor = QWidget()
        backgroundColor.setStyleSheet("background-color: #e3dcd6")
        rightSubMenu = QHBoxLayout(backgroundColor)
        iconProfile = QPushButton()
        iconProfile.setIcon(QIcon('../resources/testProfileLogo.png'))
        iconProfile.setIconSize(QSize(35, 35))
        iconProfile.setStyleSheet("background-color: white;border-radius: 17px;")
        rightSubMenu.addWidget(iconProfile)
        profileBtn = QPushButton('Profile')
        profileBtn.setStyleSheet("background-color: transparent;border-radius: 20px;font-size: 10pt;")
        rightSubMenu.addWidget(profileBtn)
        rightSubMenu.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        settingsButton = QPushButton()
        settingsButton.clicked.connect(self.__manager.OpenSettings)
        settingsButton.setIcon(QIcon('../resources/settingsIcon.png'))
        settingsButton.setIconSize(QSize(30, 30))
        settingsButton.setStyleSheet("background-color: transparent;margin-right:15px;")
        rightSubMenu.addWidget(settingsButton)
        layout.addWidget(backgroundColor)
