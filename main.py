from kiwoomLogin import *
from kiwoomStockInfo import *
from utils import *
import pandas as pd
import os


class Login:
    def __init__(self):
        print('Login Init...')

        self.login = KiwoomLogin()
        self.login.connect_to_server()  # connect to API Server

        # self.login.app.exec_()  # event loop 끝내지 않고 계속 유지


class StockInfo(Login):
    def __init__(self):
        super().__init__()
        print('Get stock Information')

        self.basicinfo = KiwoombasicInfo()
        self.priceinfo = KiwoomPriceInfo()

    def GetbasicInfo(self):
        infodict = self.basicinfo.getInfo()
        return infodict

    def GetPriceInfo(self):
        infodict = self.priceinfo.getInfo()
        return infodict


if __name__ == '__main__':
    infocls = StockInfo()
    info = infocls.GetPriceInfo()
    dfinfo = pd.DataFrame(info)
    code = IniRead(INISECT['Basic'], INIKEY['code'])
    version = IniRead(INISECT['File'], INIKEY['ver'])
    filename = code + '.csv'

    if version == 'v1':
        savepath = DATASAVEPATH_V1
        os.makedirs(DATASAVEPATH_V1, exist_ok=True)
    else:  # version: v2
        savepath = DATASAVEPATH_V2
        os.makedirs(DATASAVEPATH_V2, exist_ok=True)

    filepath = savepath + filename
    dfinfo.to_csv(filepath, mode='w')
