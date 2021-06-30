from time import sleep
from configparser import *


INIFILENAME = 'kiwoomcfg.ini'
DATEFRM = '%Y%m%d'
INISECT = {'Basic': 'BasicInfo', 'Date': 'DateInfo', 'File': 'FileInfo'}
INIKEY = {
    # Basic info key
    'code': 'stockcode',
    # Date info key
    'mode': 'todaymode', 'period': 'period', 'start': 'startdate',
    # File info key
    'traderpath': 'traderexecpath', 'ver': 'dataver'
    }
NUMRECVPRICEDATA = 20


def msecSleep(msec):
    time = msec / 1000
    sleep(time)


def IniRead(section, key):
    parser = ConfigParser()
    parser.read(INIFILENAME, encoding='utf-8')

    return parser[section][key]


DATASAVEPATH_V1 = IniRead(INISECT['File'], INIKEY['traderpath']) + '/data/v1/'
DATASAVEPATH_V2 = IniRead(INISECT['File'], INIKEY['traderpath']) + '/data/v2/'


if __name__ == '__main__':
    print(DATASAVEPATH_V1)