import logging
import os
from datetime import date
from utils import *


class WriteLog:
    def __init__(self, mdlname=None, clsname=None):
        # param setting
        self.filename = None
        self.loglevel = LOGLEVEL
        self.addmsgfmt = '({msg})'
        self.logger = self.get_logger(mdlname, clsname)

    def get_logger(self, mdlname=None, clsname=None):
        logger = logging.getLogger('logger')
        # 이전에 썼던 file handler 삭제 함 -> 로그 중복 방지
        logger.handlers.clear()

        # 오늘 날짜 받은 후 str 전환
        today = date.today().strftime(DATEFMT)
        os.makedirs(LOGPATH, exist_ok=True)
        # os.makedirs(LOGPATH)
        self.filename = '{path}/{name}.log'.format(path=LOGPATH, name=today)

        basefmt = '[%(asctime)s.%(msecs)03d][%(levelname)s]' \
                  '{processfmt}: %(message)s'
        processfmt = '[{mdl}{cls}]'

        if (mdlname is None) and (clsname is None):
            processfmt = ''
        elif (mdlname is not None) and (clsname is None):
            clsname = ''
            processfmt = processfmt.format(mdl=mdlname, cls=clsname)
        elif (mdlname is None) and (clsname is not None):
            mdlname = ''
            clsname = '##' + clsname
            processfmt = processfmt.format(mdl=mdlname, cls=clsname)
        else:  # (mdlname is not None) and (clsname is not None)
            clsname = '##' + clsname
            processfmt = processfmt.format(mdl=mdlname, cls=clsname)

        basefmt = basefmt.format(processfmt=processfmt)

        '''
        # 새로운 module에서 각각 다른 log format을 쓰려면
        # Root logger 를 사용하면 안됨
        self.logging.basicConfig(filename=self.filename,
                                 level=self.loglevel,
                                 format=basefmt,
                                 datefmt='%H:%M:%S')
        '''

        '''
        logger의 level 만 설정 할 시, handler의 level 동일
        handler level 따로 설정 가능
        '''
        # logger log level 설정
        logger.setLevel(self.loglevel)
        # file 경로 설정 및 handler의 format 설정
        file_handler = logging.FileHandler(self.filename, encoding='utf-8')
        formatter = logging.Formatter(basefmt, '%H:%M:%S')
        file_handler.setFormatter(formatter)
        # handler list에 추가
        logger.addHandler(file_handler)

        return logger

    def debug(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                self.logger.debug(msg)
                self.logger.debug(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                self.logger.debug(msg)
            elif (msg is None) and (code is not None):
                self.logger.debug(ERRCODEDICT[code])
            else:  # msg: None, code: None
                self.logger.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                self.logger.debug(msg + addmsg)
                self.logger.debug(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                self.logger.debug(msg + addmsg)
            elif (msg is None) and (code is not None):
                self.logger.debug(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                self.logger.warning(addmsg + 'No message...assign message or code!')

    def info(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                self.logger.info(msg)
                self.logger.info(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                self.logger.info(msg)
            elif (msg is None) and (code is not None):
                self.logger.info(ERRCODEDICT[code])
            else:  # msg: None, code: None
                self.logger.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                self.logger.info(msg + addmsg)
                self.logger.info(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                self.logger.info(msg + addmsg)
            elif (msg is None) and (code is not None):
                self.logger.info(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                self.logger.warning(addmsg + 'No message...assign message or code!')

    def warning(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                self.logger.warning(msg)
                self.logger.warning(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                self.logger.warning(msg)
            elif (msg is None) and (code is not None):
                self.logger.warning(ERRCODEDICT[code])
            else:  # msg: None, code: None
                self.logger.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                self.logger.warning(msg + addmsg)
                self.logger.warning(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                self.logger.warning(msg + addmsg)
            elif (msg is None) and (code is not None):
                self.logger.warning(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                self.logger.warning(addmsg + 'No message...assign message or code!')

    def error(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                self.logger.error(msg)
                self.logger.error(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                self.logger.error(msg)
            elif (msg is None) and (code is not None):
                self.logger.error(ERRCODEDICT[code])
            else:  # msg: None, code: None
                self.logger.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                self.logger.error(msg + addmsg)
                self.logger.error(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                self.logger.error(msg + addmsg)
            elif (msg is None) and (code is not None):
                self.logger.error(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                self.logger.warning(addmsg + 'No message...assign message or code!')

    def critical(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                self.logger.critical(msg)
                self.logger.critical(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                self.logger.critical(msg)
            elif (msg is None) and (code is not None):
                self.logger.critical(ERRCODEDICT[code])
            else:  # msg: None, code: None
                self.logger.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                self.logger.critical(msg + addmsg)
                self.logger.critical(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                self.logger.critical(msg + addmsg)
            elif (msg is None) and (code is not None):
                self.logger.critical(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                self.logger.warning(addmsg + 'No message...assign message or code!')


if __name__ == '__main__':
    pass