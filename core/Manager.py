import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from MessengerAPI.Authorization import Authorization

class Manager(QMainWindow):
    __authorization = Authorization.getInstance()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.authVK()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.resize(600, 500)
        self.setWindowTitle('Messenger')
        self.show()
        pass   
    def authVK(self):
        self.__authorization.authorizationVK(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Manager()
    sys.exit(app.exec_())