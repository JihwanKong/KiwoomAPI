from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import date, datetime
from utils import *
from log import WriteLog
import os

# logging.basicConfig(level=LOGLEVEL)
filename = os.path.basename(__file__)
filename = os.path.splitext(filename)[0]


class KiwoombasicInfo:
    def __init__(self):
        #logging.info('KiwoombasicInfo class init..')
        #print('KiwoombasicInfo class init..')

        # param setting
        self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
        self.writeLog = WriteLog(filename, self.__class__.__name__)
        self.name = None
        self.event_loop = None
        self.infodict = {}
        self.code = IniCfgRead(INISECT['Basic'], INIKEY['code'])

        self.writeLog.info('KiwoombasicInfo class init..')

    def getInfo(self):
        code = self.code
        self.event_slots()
        self.sendTrData(code)

        self.infodict['name'] = self.name.strip()  # strip(): 문자열 공백 제거

        self.writeLog.info('get information complete..')

        return self.infodict

    def event_slots(self):
        self.writeLog.info('event open..')
        self.kiwoom.OnReceiveTrData.connect(self.recvTrData)

    def sendTrData(self, _code):
        self.writeLog.info('send transaction data..')
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '종목코드', _code)
        self.kiwoom.dynamicCall('CommRqData(QString, QString, int, QString)',
                                'rq_opt10001', 'opt10001', 0, '0101')

        # event loop 생성 후 receive data event 일어날 때까지 대기
        # event loop exit은 receive data event 에서 처리
        self.event_loop = QEventLoop()
        self.event_loop.exec_()

    def recvTrData(self, scrNo, rqname, trcode, recName,
                   prevnext, dataLen, errCode, msg, splmMsg):
        self.writeLog.info('receive transaction data..')
        self.name = self.kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            trcode, rqname, 0, '종목명')

        self.event_loop.exit()


class KiwoomPriceInfo:
    def __init__(self):
        #logging.info('KiwoomPriceInfo class init..')
        #print('KiwoomPriceInfo class init..')

        # param setting
        self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
        self.writeLog = WriteLog(filename, self.__class__.__name__)
        self.event_loop = None
        self.infodict = {}
        self.code = IniCfgRead(INISECT['Basic'], INIKEY['code'])
        self.startdate = None  # date type
        self.enddate = None    # date type
        self.todaymode = bool(int(IniCfgRead(
            INISECT['Date'], INIKEY['mode'])))
        self.contdatamode = False
        self.date, self.open = [], []
        self.high, self.low = [], []
        self.close, self.volume = [], []
        self.memories = [self.date, self.open,
                         self.high, self.low,
                         self.close, self.volume]

        self.writeLog.info('KiwoomPriceInfo class init..')

        startdate = IniCfgRead(INISECT['Date'], INIKEY['start'])
        # date으로 형변환
        # strptime datetime.datetime(class) return
        self.startdate = datetime.strptime(startdate, DATEFMT).date()

        self.writeLog.info('todaymode: {}'.format(str(self.todaymode)))

        if self.todaymode is True:
            # date type
            self.enddate = date.today()
        else:
            enddate = IniCfgRead(INISECT['Date'], INIKEY['end'])
            # date으로 형변환
            # strptime datetime.datetime(class) return
            self.enddate = datetime.strptime(enddate, DATEFMT).date()

    def getInfo(self):
        code = self.code
        startdate = self.startdate
        enddate = self.enddate

        self.event_slots()

        enddate_str = enddate.strftime(DATEFMT)
        self.sendTrData(code, enddate_str)
        earldate = datetime.strptime(self.date[0], DATEFMT).date()

        while (self.contdatamode is True) and (earldate > startdate):
            msecSleep(50)  # send / recv에 문제있어 50msec sleep
            # 처음 data send 후 end date 기준으로 연속 데이터 확인요청
            self.sendTrData(code, enddate_str, _prevnext=2)
            earldate = datetime.strptime(self.date[0], DATEFMT).date()

        while earldate < startdate:
            for listdata in self.memories:
                listdata.pop(0)
            earldate = datetime.strptime(self.date[0], DATEFMT).date()

        columns = ['date', 'open', 'high', 'low', 'close', 'volume']

        for i, col in enumerate(columns):
            self.infodict[col] = self.memories[i]

        self.writeLog.info('get information complete..')

        return self.infodict

    def event_slots(self):
        self.writeLog.info('event open..')
        self.kiwoom.OnReceiveTrData.connect(self.recvTrData)

    def sendTrData(self, _code, _date, _prevnext=0):
        self.writeLog.info('send transaction data..',
                           addmsg='code:{} / continuous data mode:{}'
                           .format(_code, self.contdatamode))
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '종목코드', _code)
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '조회일자', _date)
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '표시구분', '0')
        self.kiwoom.dynamicCall('CommRqData(QString, QString, int, QString)',
                                'rq_opt10086', 'opt10086', _prevnext, '0101')

        # event loop 생성 후 receive data event 일어날 때까지 대기
        # event loop exit은 receive data event 에서 처리
        self.event_loop = QEventLoop()
        self.event_loop.exec_()

    def recvTrData(self, scrNo, rqname, trcode, recName,
                   prevnext, dataLen, errCode, msg, splmMsg):
        self.writeLog.info('receive transaction data..')
        datarptcnt = self.kiwoom.dynamicCall(
            'GetRepeatCnt(QString, QString)', trcode, rqname)
        for idx in range(datarptcnt):
            _date = self.kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            trcode, rqname, idx, '날짜')
            _open = self.kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            trcode, rqname, idx, '시가')
            _high = self.kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            trcode, rqname, idx, '고가')
            _low = self.kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                           trcode, rqname, idx, '저가')
            _close = self.kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                             trcode, rqname, idx, '종가')
            _volume = self.kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                              trcode, rqname, idx, '거래량')

            # 값을 받아올 떄 문자열은 strip()으로 공백 제거
            # 상수 값은 string->constant 변경 후 절대 값 처리
            alldata = [_date.strip(), abs(int(_open)), abs(int(_high)),
                       abs(int(_low)), abs(int(_close)), abs(int(_volume))]
            # list의 가장 앞쪽에 data insert
            for i, data in enumerate(alldata):
                self.memories[i].insert(0, data)

            if self.startdate >= (datetime.strptime(_date.strip(), DATEFMT).date()):
                self.contdatamode = False
                break

        if prevnext == '2':  # prevnext=='2': 연속 data 존재
            self.contdatamode = True
        else:  # prevnext=='0': 연속 data 없음
            self.contdatamode = False

        self.event_loop.exit()


