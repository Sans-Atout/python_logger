from time import localtime, strftime
from os import path

# Define nice print function
_BASE_COLOR = "\033["
_RED = _BASE_COLOR+"31m"
_GREEN = _BASE_COLOR+"32m"
_YELLOW = _BASE_COLOR+"33m"
_BLUE = _BASE_COLOR+"34m"
_PURPLE = _BASE_COLOR+"35m"
_LBLUE = _BASE_COLOR+"36m"
_WHITE = _BASE_COLOR+"37m"
_RESET = _BASE_COLOR+"0m"

_PATERN = r"\033[[0-9]+m"

class VerboseLevel(object):
    """docstring for VerboseLevel."""
    DEV = 1
    PROD = 2
    PROD_EXTEND = 3

class Logger(object):
    """docstring for Logger."""

    def __init__(self,log_dir, verbose_level, service_name=None, log_extension=None):
        self.dir_path = log_dir if log_dir[-1] == '/' else log_dir+'/'
        self.log_extension = "."+log_extension if log_extension != None else ".log"
        self.service_name = "" if service_name == None else service_name +"-"
        if not path.isdir(self.dir_path):
            self.fatal("The path to the log folder does not exist")

        if isVerboseLevel(verbose_level):
            self.verbose_level = verbose_level
        else:
            v = VerboseLevel()
            self.verbose_level = v.PROD
            self.error("You have set the wrong log level. Only level 1, 2 or 3 are tolerated!")
            self.warning("Default level verbose: PROD")



    def info(self,value):
        self.log_value = "[INFO\t\t] "+_RESET+str(value)
        self.write(_LBLUE)
        return

    def warning(self,value):
        self.log_value = "[WARNING] "+str(value)
        self.write(_YELLOW)
        return

    def fatal(self,value):
        self.log_value = "[FATAL\t] "+str(value)
        self.print(_RED)
        exit(-1)

    def error(self, value):
        self.log_value = "[ERROR\t] "+str(value)
        self.write(_RED)
        return

    def debug(self, value):
        self.log_value = "[DEBUG\t] "+_RESET+str(value)
        self.write(_PURPLE)
        return

    def done(self, value):
        self.log_value = "[DONE\t\t] "+_RESET+str(value)
        self.write(_GREEN)
        return

    def print(self, color):
        print(_RESET + getBaseLog()+color+self.log_value.replace("\t\t",'\t'))
        return

    def write(self, color):
        self.print(color)
        line = getBaseLog()+self.log_value.replace(_RESET,'')
        file_name = self.service_name+strftime("%Y-%m-%d", localtime())
        file_name = file_name + self.log_extension
        path = self.dir_path+file_name
        f = open(path,'a')
        f.write(line+'\n')
        f.close()
        return

    def avancement(prcent,after="*"):
        length = 33
        before="*"
        empty = "-"
        bar = "["
        full = "#"
        for i in range(length):
            if i <= prcent / (100/length):
                bar = bar + full
            else:
                bar = bar + empty
        bar = bar + "]"
        print("\r"+getFormatedDate+_YELLOW+bar+" "+"{:.2%}".format(prcent/100) +"\t["+after+"]",end='')
        #if prcent >= 100:
        #    self.log_value = bar+" "+"{:.2%}".format(prcent/100) +"\t["+after+"]",end='')

def getBaseLog():
    return "["+getFormatedDate()+"]\t"

def getFormatedDate():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def isVerboseLevel(possible):
    v = VerboseLevel()
    return v.DEV == possible or v.PROD == possible or v.PROD_EXTEND == possible
