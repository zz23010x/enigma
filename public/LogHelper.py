import logging
from logging.handlers import RotatingFileHandler
import os.path
import time

class LogHelper(object):
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwd):
        if LogHelper.__instance is None:
            LogHelper.__instance = object.__new__(cls, *args, **kwd)
            LogHelper.__instance.__logger = logging.getLogger("logger1")
            LogHelper.__instance.__logger.setLevel(logging.INFO)
            formatter = logging.Formatter("[%(asctime)s]-[%(filename)s]-[line:%(lineno)d]-[%(funcName)s]-[%(levelname)s]: %(message)s")
            rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
            log_path = os.getcwd() + '/Logs/'
            if not os.path.isdir(log_path):
                os.makedirs(log_path)
            log_name = 'log' + rq + '.log'
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.ERROR)
            file_handler = RotatingFileHandler(filename=os.path.join(log_path,log_name), maxBytes=1024*1024*10, encoding='utf-8', backupCount=5)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            LogHelper.__instance.__logger.addHandler(stream_handler)
            LogHelper.__instance.__logger.addHandler(file_handler)
        return LogHelper.__instance
    
    @classmethod
    def instance(self):
        if LogHelper.__instance is None:
            LogHelper()
        return LogHelper.__instance.__logger

    def info(self, message):
        LogHelper.__instance.__logger.info(message)

    def error(self, message):
        LogHelper.__instance.__logger.error(message)

def logger():
    return LogHelper().instance()


# 级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
# debug : 打印全部的日志,详细的信息,通常只出现在诊断问题上
# info : 打印info,warning,error,critical级别的日志,确认一切按预期运行
# warning : 打印warning,error,critical级别的日志,一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”),这个软件还能按预期工作
# error : 打印error,critical级别的日志,更严重的问题,软件没能执行一些功能
# critical : 打印critical级别,一个严重的错误,这表明程序本身可能无法继续运行