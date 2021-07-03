from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from utils import *
from log import WriteLog
import sys
import os

# logging.basicConfig(level=LOGLEVEL)
# log를 위한 file name 추출
# extension 제외 file 이름만 추출
filename = os.path.basename(__file__)
filename = os.path.splitext(filename)[0]


class KiwoomLogin:
    def __init__(self, login=False):
        #logging.info('KiwoomLogin class init..')
        #print('KiwoomLogin class init..')

        # param setting
        self.app = None
        self.kiwoom = None
        self.writeLog = WriteLog(filename, self.__class__.__name__)
        self.event_loop = None
        self.connectSts = False
        self.app = None
        self.name = None

        self.writeLog.info('KiwoomLogin class init..')

        self.app = QApplication(sys.argv)  # application initialization
        self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
        self.event_slots()  # event handler previously open

        if login is True:
            self.connect_to_server()

    def connect_to_server(self):
        self.kiwoom.dynamicCall('CommConnect()')

        self.event_loop = QEventLoop()  # event loop 생성
        self.event_loop.exec_()         # login 작업이 끝날 때 까지 event loop로 대기 시켜둠

        self.writeLog.info('Connect to server complete...')
        #logging.info('Connect to server complete...')
        #print('Connect to server complete...')

    def event_slots(self):
        self.writeLog.info('event open..')
        self.kiwoom.OnEventConnect.connect(self._handler_login)

    def _handler_login(self, nErrCode):
        if nErrCode == 0:
            self.writeLog.info(code=nErrCode, addmsg='Login Success!!')
        else:
            self.writeLog.error(code=nErrCode)
            #print('process Success!!')

        self.event_loop.exit()


if __name__ == '__main__':
    kiwoomlogin = KiwoomLogin(login=False)

    kiwoomlogin.connect_to_server()

    kiwoomlogin.app.exec_()
