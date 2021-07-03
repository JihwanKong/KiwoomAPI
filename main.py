from kiwoomLogin import *
from kiwoomStockInfo import *
from utils import *
from log import WriteLog
import pandas as pd
import os

#logging.basicConfig(level=LOGLEVEL)
filename = os.path.basename(__file__)
filename = os.path.splitext(filename)[0]


class Login:
    def __init__(self):
        #logging.info('Login Init...')
        #print('Login Init...')
        #param setting
        self.writeLog = WriteLog(filename, self.__class__.__name__)
        self.login = KiwoomLogin()
        self.writeLog.info('Login start.')

        self.login.connect_to_server()  # connect to API Server

        # self.login.app.exec_()  # event loop 끝내지 않고 계속 유지


class StockInfo(Login):
    def __init__(self):
        super().__init__()
        #logging.info('Get stock Information')
        #print('Get stock Information')

        # param setting
        self.writeLog = WriteLog(filename, self.__class__.__name__)
        self.basicinfo = None
        self.priceinfo = None

        self.writeLog.info('getting stock information start.')

    def GetbasicInfo(self):
        self.basicinfo = KiwoombasicInfo()
        infodict = self.basicinfo.getInfo()
        return infodict

    def GetPriceInfo(self):
        self.priceinfo = KiwoomPriceInfo()
        infodict = self.priceinfo.getInfo()
        return infodict


if __name__ == '__main__':
    infocls = StockInfo()
    info = infocls.GetPriceInfo()
    dfinfo = pd.DataFrame(info)
    code = IniCfgRead(INISECT['Basic'], INIKEY['code'])

    filename = '{}.csv'.format(code)

    savepath = DATASAVEPATH
    os.makedirs(DATASAVEPATH, exist_ok=True)

    filepath = '{path}/{name}'.format(path=savepath, name=filename)
    dfinfo.to_csv(filepath, mode='w', index=False)
