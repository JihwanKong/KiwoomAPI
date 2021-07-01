from time import sleep
from configparser import *
import json

INIFILENAME = './config/kiwoomcfg.ini'
DATEFMT = '%Y%m%d'
INISECT = {'Basic': 'BasicInfo', 'Date': 'DateInfo', 'File': 'FileInfo', 'Log': 'LogInfo'}
INIKEY = {
    # Basic info key
    'code': 'stockcode',
    # Date info key
    'mode': 'todaymode', 'period': 'period', 'start': 'startdate',
    # File info key
    'traderpath': 'traderexecpath', 'ver': 'dataver',
    # Log info key
    'level': 'loglevel', 'path': 'logpath'
}
NUMRECVPRICEDATA = 20


##########################function##########################
def msecSleep(msec):
    time = msec / 1000
    sleep(time)


def IniCfgRead(section, key):
    parser = ConfigParser()
    parser.read(INIFILENAME, encoding='utf-8')

    return parser[section][key]


def getjsonData(filename):
    with open(filename, 'r') as f:
        jsondata = json.load(f)
    return jsondata


##########################function##########################


##########################dict key type change##########################
dictdata = getjsonData('./config/errorcode.json')
dictmdf = {}
for k, v in dictdata.items():
    dictmdf[int(k)] = dictdata[k]
##########################dict key type change##########################

ERRCODEDICT = dictmdf  # errorcode.json 파일의 내용 받아옴
DATASAVEPATH = '{execpath}/data/{vername}'.format(
    execpath=IniCfgRead(INISECT['File'], INIKEY['traderpath']),
    vername=IniCfgRead(INISECT['File'], INIKEY['ver'])
)
LOGLEVEL = int(IniCfgRead(INISECT['Log'], INIKEY['level']))
LOGPATH = IniCfgRead(INISECT['Log'], INIKEY['path'])
