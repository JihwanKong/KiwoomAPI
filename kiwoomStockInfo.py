from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import date, datetime, timedelta
from utils import *


class KiwoombasicInfo:
    def __init__(self):
        print('KiwoombasicInfo class init..')

        # param setting
        self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
        self.name = None
        self.event_loop = None
        self.infodict = {}
        self.code = IniRead(INISECT['Basic'], INIKEY['code'])

    def getInfo(self):
        code = self.code
        self.event_slots()
        self.sendTrData(code)

        self.infodict['name'] = self.name.strip()  # strip(): 문자열 공백 제거

        return self.infodict

    def event_slots(self):
        self.kiwoom.OnReceiveTrData.connect(self.recvTrData)

    def sendTrData(self, _code):
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

        self.name = self.kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            trcode, rqname, 0, '종목명')

        self.event_loop.exit()


class KiwoomPriceInfo:
    def __init__(self):
        print('KiwoomPriceInfo class init..')

        # param setting
        self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
        self.event_loop = None
        self.infodict = {}
        self.code = IniRead(INISECT['Basic'], INIKEY['code'])
        self.startdate = None  # date type
        self.todaymode = int(IniRead(INISECT['Date'], INIKEY['mode']))
        self.open, self.close = [], []
        self.high, self.low = [], []
        self.date, self.volume = [], []
        self.period = int(IniRead(INISECT['Date'], INIKEY['period']))

        #todaymode option boolean 형태로 변환
        #ini file read 시 string 형태로 갖고옴
        self.todaymode = bool(self.todaymode)

        if self.todaymode is True:
            # date type
            self.startdate = date.today()
        else:
            startdate = IniRead(INISECT['Date'], INIKEY['start'])
            # date으로 형변환
            # strptime datetime.datetime(class) return
            self.startdate = datetime.strptime(startdate, DATEFRM).date()

    def getInfo(self):
        period = self.period - 1  # today 포함이므로 priod보다 하나 작은 수 뺌
        code = self.code
        startdate = self.startdate
        enddate = startdate - timedelta(period)

        self.event_slots()

        _daydelta = 0
        while True:
            _date = startdate - timedelta(days=_daydelta)

            date_str = _date.strftime(DATEFRM)

            #send / recv에 문제있어 50msec sleep
            msecSleep(50)
            self.sendTrData(code, date_str)

            # list에서 string 받은 후 date type으로 형변환
            earlistdate = self.date[0]
            earlistdate = datetime.strptime(earlistdate, DATEFRM).date()

            # list 날짜에 period에 포함되지 않는 날짜(앞선날짜) 제거
            if earlistdate == enddate:
                break
            elif earlistdate < enddate:
                tempearl = earlistdate
                while tempearl < enddate:
                    self.date.pop(0), self.open.pop(0)
                    self.close.pop(0), self.high.pop(0)
                    self.low.pop(0), self.volume.pop(0)
                    # list에서 string받고 date type으로 형변환
                    strearl = self.date[0]
                    tempearl = datetime.strptime(strearl, DATEFRM).date()
                break
            else:
                '''earlist date 보다 하루전 data 
                부터 receive 할수도있도록 delta 값 조정'''
                tempearl = startdate - (earlistdate - timedelta(days=1))
                _daydelta = tempearl.days

        self.infodict['date'] = self.date
        self.infodict['open'] = self.open
        self.infodict['high'] = self.high
        self.infodict['low'] = self.low
        self.infodict['close'] = self.close
        self.infodict['volme'] = self.volume

        return self.infodict

    def event_slots(self):
        self.kiwoom.OnReceiveTrData.connect(self.recvTrData)

    def sendTrData(self, _code, _date):
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

            # list의 가장 앞쪽에 data insert
            # 값을 받아올 떄 stirp()으로 각 값의 공백 제거
            self.date.insert(0, _date.strip())
            self.open.insert(0, abs(int(_open)))
            self.high.insert(0, abs(int(_high)))
            self.low.insert(0, abs(int(_low)))
            self.close.insert(0, abs(int(_close)))
            self.volume.insert(0, abs(int(_volume)))

        self.event_loop.exit()
