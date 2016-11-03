#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4
import getpass
import os, sys

# #########################################################
# - SetUp del log
# #########################################################
def setupLog(gv):
    if gv.INPUT_PARAM.LogACTIVE:
        C       = gv.Ln.Colors()

        logFileName         = '/tmp/{PREFIX}_{USER}.log'.format(PREFIX=gv.Prj.prefix, USER=getpass.getuser())
        logConfigFileName   = os.path.normpath('{CONFDIR}/LoggerConfig.ini'.format(CONFDIR=gv.Prj.configDIR))

        if gv.fDEBUG:
            C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
            C.printCyan('logFileName       {0}'.format(logFileName), tab=8)
            C.printCyan('logConfigFileName {0}'.format(logConfigFileName), tab=8)
            C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
            print ()



        if os.path.isfile(logConfigFileName):
            # gv.Ln.initLogger(iniLogFile=logConfigFileName, logFileName=logFileName, package=gv.Prj.name, packageQualifiers=8)
            gv.Ln.InitLogger(   iniLogFile=logConfigFileName,
                                logFileName=logFileName,
                                package=gv.Prj.name,
                                logCONSOLE=gv.INPUT_PARAM.LogCONSOLE,
                                logMODULE=gv.INPUT_PARAM.LogMODULE,
                                logACTIVE=gv.INPUT_PARAM.LogACTIVE,
                                packageQualifiers=8
                            )

            logger = gv.Ln.SetLogger(package="Main")
        else:
            errMsg = 'il file {0} non esiste..'.format(logConfigFileName)
            gv.Ln.Exit(1, errMsg)
    else:
        logger = gv.Ln.SetLogger(package="Main")
        # logger = gv.Ln.setNullLogger()

    return logger



