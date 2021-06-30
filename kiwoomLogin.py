from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class KiwoomLogin:
    def __init__(self, login=False):
        print('KiwoomLogin class init..')

        # param setting
        self.event_loop = None
        self.connectSts = False
        self.app = None
        self.name = None

        self.app = QApplication(sys.argv)      # application initialization
        self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')

        self.event_slots()  # event handler previously open

        if login is True:
            self.connect_to_server()

    def connect_to_server(self):
        self.kiwoom.dynamicCall('CommConnect()')
        #self.dynamicCall('CommConnect()')

        self.event_loop = QEventLoop()  # event loop 생성
        self.event_loop.exec_()         # login 작업이 끝날 때 까지 event loop로 대기 시켜둠

        print('Connect to server complete...')

    def event_slots(self):
        self.kiwoom.OnEventConnect.connect(self._handler_login)
        #self.OnEventConnect.connect(self._handler_login)

    def _handler_login(self, nErrCode):
        if nErrCode == -100:
            print('user information exchnage fail')
        elif nErrCode == -101:
            print('server connection fail')
        elif nErrCode == -102:
            print('version processing fail')
        else:   # nErrCode == 0
            print('login Success!!')

        self.event_loop.exit()


if __name__ == '__main__':
    kiwoomlogin = KiwoomLogin(login=False)

    kiwoomlogin.connect_to_server()

    kiwoomlogin.app.exec_()
