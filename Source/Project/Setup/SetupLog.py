#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4
import getpass
import os, sys

__author__  = 'Loreto Notarantonio'
__version__ = 'LnVer_2017-06-22_16.42.24'

# #########################################################
# - SetUp del log
# #########################################################
def SetupLog(gv):
    # gv.INPUT_PARAM.printDict(fEXIT=True)
    if gv.INPUT_PARAM.LOGGER:
        C       = gv.Ln.LnColor()

        logFileName         = '/tmp/{PREFIX}_{USER}.log'.format(PREFIX=gv.Prj.prefix, USER=getpass.getuser())
        logConfigFileName   = os.path.normpath('{CONFDIR}/LoggerConfig.ini'.format(CONFDIR=gv.Prj.configDIR))

        if gv.fDEBUG:
            C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
            C.printCyan('logFileName       {0}'.format(os.path.abspath(logFileName)), tab=8)
            C.printCyan('logConfigFileName {0}'.format(logConfigFileName), tab=8)
            C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
            print ()



        if os.path.isfile(logConfigFileName):
            gv.Ln.InitLogger(   iniLogFile=logConfigFileName,
                                logFileName=logFileName,
                                package=gv.Prj.name,
                                LOGGER=gv.INPUT_PARAM.LOGGER,
                                logCONSOLE=gv.INPUT_PARAM.logCONSOLE,
                                logMODULE=gv.INPUT_PARAM.logMODULE,
                                packageQualifiers=8
                            )

            logger = gv.Ln.SetLogger(package="Main")
        else:
            errMsg = 'il file {0} non esiste..'.format(logConfigFileName)
            gv.Ln.Exit(1, errMsg)
    else:
        logger = gv.Ln.SetLogger(package="Main")


    return logger



