#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# Version 0.01 08/04/2010:  Starting
# ####################################################################################################################
# http://stackoverflow.com/questions/13649664/how-to-use-logging-with-pythons-fileconfig-and-configure-the-logfile-filename
import sys, os
import logging
import logging.config # obbligatorio altrimenti da' l'errore: <'module' object has no attribute 'config'>
import inspect

gPackageQualifiers = 0
isLoggerActive = False   # variabile globale accessibile anche dall'esterno



_logMODULE  = False
_logCONSOLE = False
_logACTIVE  = False


# ###########################################################
# - LnLogger(object)
# ###########################################################
class LnLogger(loggingLogger):
    def __init__(self, iniLogFile, logFileName, package, logCONSOLE=False, logMODULE=False, logACTIVE=False, packageQualifiers=2):
            # ----- defaults
        self._filename          = logFileName
        self._description       = None
        self._author            = None
        self._family            = None
        self._bcast             = None
        self._netmask           = None
        self._subnet            = None
        self._table             = None
        self._gatewayAddress    = None
        self._gatewayMAC        = None
        self._isGatewayDefault  = None
        self._isGatewayPinging  = False



    # ========================================================
    # - INIT del log. Chiamato solo dal MAIN program
    # ========================================================
def initLogger(iniLogFile, logFileName, package, logCONSOLE=False, logMODULE=False, logACTIVE=False, packageQualifiers=2):
    global gPackageQualifiers
    global _logMODULE, _logCONSOLE, _logACTIVE

    _logMODULE  = logMODULE
    _logCONSOLE = logCONSOLE
    _logACTIVE  = logACTIVE

    gPackageQualifiers = packageQualifiers

    if not os.path.isfile(iniLogFile):
        print (iniLogFile, "... NOT FOUND")
        sys.exit()

    logging.config.fileConfig(iniLogFile, disable_existing_loggers=False, defaults={'rotateLogFile': logFileName})
    logger      = logging.getLogger(package)
    LnFilter    = ContextFilter()
    logger.addFilter(LnFilter)

    savedLevel  = logger.getEffectiveLevel()

    logger.setLevel(logging.INFO)
    for i in range(1,10):   logger.info(' ')
    for i in range(1,5):    logger.info('-'*40 + 'Start LOGging' + '-'*20)
    logger.setLevel(savedLevel)

    logFileName = logging.getLoggerClass().root.handlers[0].baseFilename
    # print ("    {0:<32}: {1}".format('LOG file', logFileName))

    return logFileName




















# http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """
    def __init__(self):
        self._line  = None
        self._stack = 5    # default

    def setLineNO(self, number):
        self._line = number

    def setStack(self, number):
        self._stack = number

    def filter(self, record):
        if self._line:
            record.lineno = self._line
        else:
            # record.name   = sys._getframe(stack).f_code.co_name
            record.lineno = sys._getframe(self._stack).f_lineno
        return True



###############################################
#
###############################################
def getCaller(deepLevel=0, funcName=None):
    try:
        caller  = inspect.stack()[deepLevel]
    except Exception as why:
        return '{0}'.format(why)   # potrebbe essere out of stack ma ritorniamo comunque la stringa

    # print ('..........caller', caller)
    programFile = caller[1]
    lineNumber  = caller[2]
    if not funcName:
        funcName    = caller[3]
    lineCode    = caller[4]
    fname       = os.path.basename(programFile).split('.')[0]

    if funcName == '<module>':
        data = "[{0}:{1}]".format(fname, lineNumber)
    else:
        data = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)
    return data




def setNullLogger(package=None):
    global isLoggerActive

    ##############################################################################
    # - classe che mi permette di lavorare nel caso il logger non sia richiesto
    ##############################################################################

    class nullLogger():
            def __init__(self, package=None, stackNum=1):
                pass
            def info(self, data):   pass
            def debug(self, data):  pass
            def error(self, data):  pass
            def warning(self, data):  pass

    isLoggerActive = False
    return nullLogger()


# ====================================================================================
# richiamando questa funzione posso dirottare l'out della log su CONSOLE previa
# impostazione del logger.ini con:
#
#        [logger_LnConsole]
#            handlers=consoleHandler
#            level=DEBUG
#            qualname=LnConsole
#            propagate=0
#
#  call: logger = gv.LN.consoleLOG(gv, __name__)
#  call: logger = gv.LN.consoleLOG(gv, __name__, funcName=sys._getframe().f_code.co_name)
#                   utile quando si hanno più funzioni all'interno dello stesso modulo
#
# ====================================================================================
# def setLogger(gv, package, CONSOLE=None, stackNum=0):
def setLogger(package, stackNum=0):
    # global isLoggerActive

    if _logMODULE or _logACTIVE:
        stackLevel = 1                          # stackLevel di base
        stackLevel += stackNum                  # aggiungiamo quello richiesto dal caller

        funcName    = sys._getframe(stackLevel).f_code.co_name
        funcLineNO  = sys._getframe(stackLevel).f_lineno
        if funcName == '<module>': funcName = '__main__'

        pkgName = package + '.' + funcName if funcName else package

        # - tracciamo la singola funzione oppure modulo oppure libreria od altro
        LOG_LEVEL = None
        if _logMODULE:
            fullPkg = (package + funcName).lower()
            for stringa in _logMODULE.split(','):
                if stringa.lower() in fullPkg:
                    LOG_LEVEL = logging.DEBUG

        elif _logACTIVE:
            LOG_LEVEL = logging.DEBUG

    else:
        return setNullLogger()



        # ------------------------------------------------
        # - del package prendiamo
        # - solo gli ultimi n.. gPackageQualifiers.
        # ------------------------------------------------
    if _logCONSOLE:
        pkgName = 'LnC.{0}'.format(package.split('.')[-1])
    else:
        packageHier = pkgName.split('.')

        pkgName     = (packageHier[0] +'.'+packageHier[-1])  # se ho nomi servizi uguali in diversi moduli crea confusione
        pkgName     = ('.'.join(packageHier[-gPackageQualifiers:]))

        pkgName     = ('.'.join(packageHier[-2:])) # prende il modulo+Function


    logger = logging.getLogger(pkgName)

    # -----------------------------------------------------------------------------------------
    # - Per quanto riguarda il setLogger, devo intervenire sul numero di riga della funzione
    # - altrimenti scriverebbe quello della presente funzione.
    # - Per fare questo utilizzo l'aggiunta di un filtro passandogli il lineNO corretto
    # - per poi ripristinarlo al default
    # -----------------------------------------------------------------------------------------

    if LOG_LEVEL:
        logger.setLevel(LOG_LEVEL)
    else:
         # logger.setLevel(logging.NOTSET)  # oppure FATAL
         logger.disabled

        # - creiamo il contextFilter
    LnFilter    = ContextFilter()

        # - aggiungiamolo al logger attuale
    logger.addFilter(LnFilter)

        # - modifichiamo la riga della funzione chiamante
    LnFilter.setLineNO(funcLineNO)

        # ----------------------------------------------------------------------------------
        # - inseriamo la riga con riferimento al chiamante di questa fuznione
        # - nel "...called by" inseriamo il caller-1
        # ----------------------------------------------------------------------------------
    # logger.debug('')
    logger.debug('......called by:{CALLER}'.format(CALLER=getCaller(stackLevel+2)))

        # --------------------------------------------------------------------------
        # - azzeriamo il lineNO in modo che le prossime chiamate al logger, che
        # - non passano da questa funzione, prendano il lineNO corretto.
        # --------------------------------------------------------------------------
    LnFilter.setLineNO(None)
    LnFilter.setStack(5)            # ho verificato che con 5 sembra andare bene

    return logger




if __name__ == '__main__':
        # ---------------------------------------------------------
        # - SetUp del log
        # ---------------------------------------------------------
    userName=getpass.getuser()
    logFileName          = '/tmp/IFC_{USER}.log'.format(USER=userName)
    logConfigFileName   = os.path.join(os.path.dirname(__file__), 'LoggerConfig.ini')

    gv.Ln.initLogger(iniLogFile=logConfigFileName, logFileName=logFileName, package='IFC', packageQualifiers=2)
    logger = gv.Ln.setLogger(gv, package="Main")
