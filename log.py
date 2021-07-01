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

        # 오늘 날짜 받은 후 str 전환
        today = date.today().strftime(DATEFMT)
        os.makedirs(LOGPATH, exist_ok=True)
        #os.makedirs(LOGPATH)
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

        logging.basicConfig(filename=self.filename,
                            level=self.loglevel,
                            format=basefmt,
                            datefmt='%H:%M:%S')

    def debug(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                logging.debug(msg)
                logging.debug(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                logging.debug(msg)
            elif (msg is None) and (code is not None):
                logging.debug(ERRCODEDICT[code])
            else:  # msg: None, code: None
                logging.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                logging.debug(msg + addmsg)
                logging.debug(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                logging.debug(msg + addmsg)
            elif (msg is None) and (code is not None):
                logging.debug(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                logging.warning(addmsg + 'No message...assign message or code!')

    def info(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                logging.info(msg)
                logging.info(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                logging.info(msg)
            elif (msg is None) and (code is not None):
                logging.info(ERRCODEDICT[code])
            else:  # msg: None, code: None
                logging.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                logging.info(msg + addmsg)
                logging.info(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                logging.info(msg + addmsg)
            elif (msg is None) and (code is not None):
                logging.info(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                logging.warning(addmsg + 'No message...assign message or code!')

    def warning(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                logging.warning(msg)
                logging.warning(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                logging.warning(msg)
            elif (msg is None) and (code is not None):
                logging.warning(ERRCODEDICT[code])
            else:  # msg: None, code: None
                logging.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                logging.warning(msg + addmsg)
                logging.warning(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                logging.warning(msg + addmsg)
            elif (msg is None) and (code is not None):
                logging.warning(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                logging.warning(addmsg + 'No message...assign message or code!')

    def error(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                logging.error(msg)
                logging.error(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                logging.error(msg)
            elif (msg is None) and (code is not None):
                logging.error(ERRCODEDICT[code])
            else:  # msg: None, code: None
                logging.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                logging.error(msg + addmsg)
                logging.error(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                logging.error(msg + addmsg)
            elif (msg is None) and (code is not None):
                logging.error(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                logging.warning(addmsg + 'No message...assign message or code!')

    def critical(self, msg=None, code=None, addmsg=None):
        if addmsg is None:
            if (msg is not None) and (code is not None):
                logging.critical(msg)
                logging.critical(ERRCODEDICT[code])
            elif (msg is not None) and (code is None):
                logging.critical(msg)
            elif (msg is None) and (code is not None):
                logging.critical(ERRCODEDICT[code])
            else:  # msg: None, code: None
                logging.warning('No message...assign message or code!')

        else:  # addmsg is not None
            # 괄호 형태로 string 변경
            addmsg = self.addmsgfmt.format(msg=addmsg)
            if (msg is not None) and (code is not None):
                logging.critical(msg + addmsg)
                logging.critical(ERRCODEDICT[code] + addmsg)
            elif (msg is not None) and (code is None):
                logging.critical(msg + addmsg)
            elif (msg is None) and (code is not None):
                logging.critical(ERRCODEDICT[code] + addmsg)
            else:  # msg: None, code: None
                logging.warning(addmsg + 'No message...assign message or code!')


if __name__ == '__main__':
    pass