import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from MessengerAPI.Authorization import Authorization


class Manager(QMainWindow):
    __authorization = Authorization.getInstance()

    def __init__(self):
        super().__init__()
        self.rightSubMenu = QVBoxLayout()
        self.initUI()
<<<<<<< HEAD
        print()

    def initUI(self):
=======

    def initUI(self):
        # self.statusBar().showMessage('Ready')
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
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

        mainLayout.addLayout(leftMenu)
        mainLayout.addLayout(self.rightMenu)
<<<<<<< HEAD

        leftWidgetList = QListWidget()
        leftWidgetList.setMaximumSize(300, 10000)
        leftWidgetList.clicked.connect(self.loadDialogMessage)
        leftWidgetList.setStyleSheet("""QListWidget{border: 0;}
                                        QScrollBar::handle:vertical {
                                            background: #DCDCDC;
                                            border-radius: 10px;
                                            min-height: 20px;
                                        }""")
        leftMenu.addWidget(leftWidgetList)
        self.loadDialogs(leftWidgetList)
=======
        leftMenu.addWidget(QPushButton('Friend1btn2'))
        leftMenu.addWidget(QPushButton('Friend2btn3'))
        leftMenu.addItem(QSpacerItem(220, 0, QSizePolicy.Fixed, QSizePolicy.Expanding))
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
        self.rightMenu.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.MessageMenuInit()
        self.show()
        pass

<<<<<<< HEAD
    def loadDialogMessage(self, item):
        print(item.row())
        self.messageList.clear()
        msgs = self.__authorization.getMessageByN(item.row(), 0)
        print(msgs)
        for msg in msgs['items']:
            self.addMessageToLayout(msg['body'], self.messageList, msg['from_id'] == msg['user_id'])
        pass

    def loadDialogs(self, layout):
        dialogs = self.__authorization.getMessengerClassesVK().getDialogs()
        print(dialogs[0].getTitle())
        for n, dialog in enumerate(dialogs):
            self.addDialogToLayout(layout, dialog.getTitle())
        pass

    def clearLayout(self, layout):
=======
    def clearLayout(self,layout):
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())
        self.rightMenu.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

<<<<<<< HEAD
    def addDialogToLayout(self, layout, text):
        itemN = QListWidgetItem(text)
        itemN.setSizeHint(QSize(70, 50))
        layout.addItem(itemN)
        # layout.setItemWidget(itemN, widget)

=======
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
    def OpenSettings(self):
        self.clearLayout(self.rightMenu)
        msgInit = QPushButton('Close')
        msgInit.clicked.connect(self.MessageMenuInit)
        self.rightMenu.addWidget(msgInit)
        vkLogin = QPushButton('Login throw VK')
        vkLogin.clicked.connect(self.loginThrowVK)
        self.rightMenu.addWidget(vkLogin)

<<<<<<< HEAD
=======

>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
    def loginThrowVK(self):
        self.__authorization.authorizationVK(self)
        pass

<<<<<<< HEAD
=======

>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
    def MessageMenuInit(self):
        self.clearLayout(self.rightMenu)
        self.addUserSubMenu(self.rightSubMenu)
        self.addMessageLayout(self.rightSubMenu)
        self.MessageWriteMenu(self.rightSubMenu)
        self.rightMenu.addLayout(self.rightSubMenu)

<<<<<<< HEAD
    def MessageWriteMenu(self, layout):
=======
    def MessageWriteMenu(self,layout):
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
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
<<<<<<< HEAD
        self.messageList = QListWidget()
        rightMessageHistory.setContentsMargins(0, 0, 0, 0)
        self.messageList.setStyleSheet("""QListWidget{border: 0;}
=======
        widgetList = QListWidget()
        rightMessageHistory.setContentsMargins(0, 0, 0, 0)
        widgetList.setStyleSheet("""QListWidget{border: 0;}
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
                                QScrollBar::handle:vertical {
                                    background: #DCDCDC;
                                    border-radius: 10px;
                                    min-height: 20px;
                                }""")
        # widgetList.setFlow(Qt.AlignBottom)
<<<<<<< HEAD
        rightMessageHistory.addWidget(self.messageList)
        for x in range(0, 50):
            self.addMessageToLayout("test " + str(x), self.messageList, True)
            self.addMessageToLayout("test " + str(x), self.messageList, False)
=======
        rightMessageHistory.addWidget(widgetList)
        for x in range(0, 50):
            self.addMessageToLayout("test " + str(x), widgetList, True)
            self.addMessageToLayout("test " + str(x), widgetList, False)
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59

        layout.addWidget(bcgColor2)

    '''
        sideMessage
            True - my message
            False - message from friend
    '''
<<<<<<< HEAD

=======
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
    def addMessageToLayout(self, message, layout, sideMessage):
        helpWidget = QWidget()
        msg = QGridLayout(helpWidget)
        msg.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        msgButton = QPushButton(message)
        msgButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        msg.addWidget(msgButton, 0, 0, Qt.AlignRight)
        if sideMessage:
            msg.addWidget(msgButton, 0, 0, Qt.AlignRight)
        else:
            msg.addWidget(msgButton, 0, 0, Qt.AlignLeft)

        itemN = QListWidgetItem()
        itemN.setSizeHint(QSize(0, 50))
<<<<<<< HEAD
        layout.insertItem(0,itemN)
=======
        layout.addItem(itemN)
>>>>>>> 8cc603d005f8948c9b8e2b8e389a2cff5a738d59
        layout.setItemWidget(itemN, helpWidget)

    def addUserSubMenu(self, layout):
        backgroundColor = QWidget()
        backgroundColor.setStyleSheet("background-color: #e3dcd6")
        rightSubMenu = QHBoxLayout(backgroundColor)
        iconProfile = QPushButton()
        iconProfile.setIcon(QIcon('../resources/testProfileLogo.png'))
        iconProfile.setIconSize(QSize(35, 35))
        iconProfile.setStyleSheet("background-color: white;border-radius: 17px;")
        rightSubMenu.addWidget(iconProfile)
        profileBtn = QPushButton('Dude profile')
        profileBtn.setStyleSheet("background-color: transparent;border-radius: 20px;font-size: 10pt;")
        rightSubMenu.addWidget(profileBtn)
        rightSubMenu.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        settingsButton = QPushButton()
        settingsButton.clicked.connect(self.OpenSettings)
        settingsButton.setIcon(QIcon('../resources/settingsIcon.png'))
        settingsButton.setIconSize(QSize(30, 30))
        settingsButton.setStyleSheet("background-color: transparent;margin-right:15px;")
        rightSubMenu.addWidget(settingsButton)
        layout.addWidget(backgroundColor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Manager()
    sys.exit(app.exec_())
