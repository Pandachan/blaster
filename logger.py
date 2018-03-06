'''
Created on Jul 22, 2014

@author: M1Ni
'''
import logging

DefaultLoggerName = "logger"
DefaultLoggerLevel = logging.DEBUG

class Logger(object):
    '''
    classdocs
    '''
    def __init__(self, loggerName = DefaultLoggerName):
        '''
        Constructor
        '''
        loggerName = loggerName + ".log"
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)
        self.fileHandler = logging.FileHandler(loggerName)
        self.fileHandler.setLevel(logging.DEBUG)
        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s')
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.streamHandler)
    # >>> End of init

    def Debug(self, logMsg = ""):
        self.logger.debug(logMsg)
    # >>> End of logDebug

    def Info(self, logMsg = ""):
        self.logger.info(logMsg)
    # >>> End of logInfo

    def Error(self, logMsg = ""):
        self.logger.error(logMsg)
    # >>> End of logError

    def Warning(self, logMsg = ""):
        self.logger.warn(logMsg)
    # >>> End of logWarning

    def Critical(self, logMsg = ""):
        self.logger.critical(logMsg)
    # >>> End of logCritical
# >>> End of Class
