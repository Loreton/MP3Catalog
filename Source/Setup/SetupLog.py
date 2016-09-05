#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4
import getpass
import os, sys

# #########################################################
# - SetUp del log
# #########################################################
def setupLog(gv):

        ##############################################################################
        # - classe che mi permette di lavorare nel caso il logger non sia richiesto
        ##############################################################################
    class nullLogger():
        def __init__(self, package=None, stackNum=1):
            pass
        def info(self, data):   pass
        def debug(self, data):  pass


    if gv.INPUT_PARAM.LogACTIVE:
        C       = gv.Ln.Colors()

        logFileName         = '/tmp/{PREFIX}_{USER}.log'.format(PREFIX=gv.Prj.prefix, USER=getpass.getuser())
        logConfigFileName   = '{CONFDIR}/{PREFIX}_LoggerConfig.ini'.format(CONFDIR=gv.Prj.configDIR, PREFIX=gv.Prj.prefix)

        if gv.fDEBUG:
            C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
            C.printCyan('logFileName       {0}'.format(logFileName), tab=8)
            C.printCyan('logConfigFileName {0}'.format(logConfigFileName), tab=8)
            C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
            print ()



        gv.Ln.initLogger(iniLogFile=logConfigFileName, logFileName=logFileName, package='MP3', packageQualifiers=8)
        logger = gv.Ln.setLogger(gv, package="Main")
    else:
        logger = nullLogger()

    return logger



