from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import date, datetime, timedelta
from utils import *
from log import *
import logging

# logging.basicConfig(level=LOGLEVEL)
filename = os.path.basename(__file__)
filename = os.path.splitext(filename)[0]


class KiwoombasicInfo:
    def __init__(self):
        logging.info('KiwoombasicInfo class init..')
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
        self.todaymode = int(IniCfgRead(INISECT['Date'], INIKEY['mode']))
        self.date, self.open = [], []
        self.high, self.low = [], []
        self.close, self.volume = [], []
        self.memories = [self.date, self.open,
                         self.high, self.low,
                         self.close, self.volume]
        self.period = int(IniCfgRead(INISECT['Date'], INIKEY['period']))

        self.writeLog.info('KiwoomPriceInfo class init..')

        #todaymode option boolean 형태로 변환
        #ini file read 시 string 형태로 갖고옴
        self.todaymode = bool(self.todaymode)

        self.writeLog.info('todaymode: {}'.format(str(self.todaymode)))

        if self.todaymode is True:
            # date type
            self.startdate = date.today()
        else:
            startdate = IniCfgRead(INISECT['Date'], INIKEY['start'])
            # date으로 형변환
            # strptime datetime.datetime(class) return
            self.startdate = datetime.strptime(startdate, DATEFMT).date()

    def getInfo(self):
        period = self.period - 1  # today 포함이므로 priod보다 하나 작은 수 뺌
        code = self.code
        startdate = self.startdate
        enddate = startdate - timedelta(period)

        self.event_slots()

        _daydelta = 0
        while True:
            _date = startdate - timedelta(days=_daydelta)

            date_str = _date.strftime(DATEFMT)

            #send / recv에 문제있어 50msec sleep
            msecSleep(50)
            self.sendTrData(code, date_str)

            # list에서 string 받은 후 date type으로 형변환
            earlistdate = self.date[0]
            earlistdate = datetime.strptime(earlistdate, DATEFMT).date()

            # list 날짜에 period에 포함되지 않는 날짜(앞선날짜) 제거
            if earlistdate == enddate:
                break
            elif earlistdate < enddate:
                tempearl = earlistdate
                while tempearl < enddate:
                    # 모든 memory에서 가장 앞 data 제거
                    for listdata in self.memories:
                        listdata.pop(0)
                    # list에서 string받고 date type으로 형변환
                    strearl = self.date[0]
                    tempearl = datetime.strptime(strearl, DATEFMT).date()
                break
            else:
                '''earlist date 보다 하루전 data 
                부터 receive 할수도있도록 delta 값 조정'''
                tempearl = startdate - (earlistdate - timedelta(days=1))
                _daydelta = tempearl.days

        columns = ['date', 'open', 'high', 'low', 'close', 'volume']

        for i, col in enumerate(columns):
            self.infodict[col] = self.memories[i]

        self.writeLog.info('get information complete..')

        return self.infodict

    def event_slots(self):
        self.writeLog.info('event open..')
        self.kiwoom.OnReceiveTrData.connect(self.recvTrData)

    def sendTrData(self, _code, _date):
        self.writeLog.info('send transaction data..')
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '종목코드', _code)
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '조회일자', _date)
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '표시구분', '0')
        self.kiwoom.dynamicCall('CommRqData(QString, QString, int, QString)',
                                'rq_opt10086', 'opt10086', 0, '0101')

        # event loop 생성 후 receive data event 일어날 때까지 대기
        # event loop exit은 receive data event 에서 처리
        self.event_loop = QEventLoop()
        self.event_loop.exec_()

    def recvTrData(self, scrNo, rqname, trcode, recName,
                   prevnext, dataLen, errCode, msg, splmMsg):
        self.writeLog.info('receive transaction data..')
        for idx in range(NUMRECVPRICEDATA):
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

        self.event_loop.exit()
