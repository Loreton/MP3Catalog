#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4
import getpass
import os, sys

# #########################################################
# - SetUp del log
# #########################################################
def setupLog(gv):
    C       = gv.Ln.Colors()

    logFileName         = '/tmp/{PREFIX}_{USER}.log'.format(PREFIX=gv.Prj.prefix, USER=getpass.getuser())
    logConfigFileName   = '{CONFDIR}/{PREFIX}_LoggerConfig.ini'.format(CONFDIR=gv.Prj.configDIR, PREFIX=gv.Prj.prefix)

    if gv.fDEBUG:
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        C.printCyan('logFileName       {0}'.format(logFileName), tab=8)
        C.printCyan('logConfigFileName {0}'.format(logConfigFileName), tab=8)
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()



    gv.Ln.initLogger(iniLogFile=logConfigFileName, logFileName=logFileName, package='MP3', packageQualifiers=2)
    logger = gv.Ln.setLogger(package="Main", CONSOLE=gv.INPUT_PARAM.LogCONSOLE)

    return logger