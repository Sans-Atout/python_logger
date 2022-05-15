from time import localtime, strftime
from os import path

from colorama import init
from colorama import Fore, Style

init()

_COLOR = {
        'INFO': Style.BRIGHT + Fore.BLUE,
        'DEBUG': Style.BRIGHT + Fore.MAGENTA,
        'DONE': Style.BRIGHT + Fore.GREEN,
        'GREY' : Style.BRIGHT + Fore.LIGHTBLACK_EX,
        'WARNING': Style.BRIGHT + Fore.YELLOW,
        'ERROR': Style.BRIGHT + Fore.RED,
        'FATAL': Style.BRIGHT + Fore.RED,
        'DEFAULT': Style.BRIGHT + Fore.WHITE,
        'END': Style.RESET_ALL,
    }

class VerboseLevel(object):
    """docstring for VerboseLevel."""
    DEV = 1
    PROD = 2
    PROD_EXTEND = 3

class Logger(object):
    """docstring for Logger."""

    def __init__(self,log_dir, verbose_level, service_name=None, log_extension=None, separator=';'):
        self.dir_path = log_dir if log_dir[-1] == '/' else log_dir+'/'
        self.log_extension = "."+log_extension if log_extension != None else ".log"
        self.service_name = "" if service_name == None else service_name
        self.separator = separator
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
        self.log_value = ("INFO",str(value))
        self.write()
        return

    def warning(self,value):
        self.log_value = ("WARNING",str(value))
        self.write()
        return

    def fatal(self,value):
        self.log_value = ("FATAL",str(value))
        self.print()
        exit(-1)

    def error(self, value):
        self.log_value = ("ERROR",str(value))
        self.write()
        return

    def debug(self, value):
        self.log_value = ("DEBUG",str(value))
        self.write()
        return

    def done(self, value):
        self.log_value = ("DONE",str(value))
        self.write()
        return

    def print(self):
        service = str(self.service_name).replace("_", " ")
        logLine = setColor("END")+"["+setColor("GREY")+getFormatedDate()+setColor("END")+"]\t["
        lvl = self.log_value[0] if(self.log_value[0] == "WARNING") else self.log_value[0]+'\t'
        logLine = logLine + setColor(self.log_value[0])+lvl+setColor("END")+"] ["+setColor("GREY")+service+setColor("END")+"]\t"
        print(logLine + self.log_value[1])
        return

    def write(self):
        self.print()
        line = getFormatedDate() + self.separator+self.log_value[0]+self.separator+self.log_value[1]
        file_name = strftime("%Y-%m-%d", localtime())+"-"+self.service_name
        file_name = file_name + self.log_extension
        path = self.dir_path+file_name
        f = open(path,'a')
        f.write(line+'\n')
        f.close()
        return

    def avancement(self,prcent,after="*"):
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
        print("\r"+setColor("END")+"["+setColor("GREY")+getFormatedDate()+setColor("END")+"]\t"+setColor("WARNING")+bar+" "+"{:.2%}".format(prcent/100) +"\t["+after+"]",end='')

def getFormatedDate():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def isVerboseLevel(possible):
    v = VerboseLevel()
    return v.DEV == possible or v.PROD == possible or v.PROD_EXTEND == possible
def setColor(cName):
    return _COLOR[cName]
