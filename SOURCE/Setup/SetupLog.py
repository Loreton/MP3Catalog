#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4
import getpass
import os, sys
# #########################################################
# - SetUp del log
# #########################################################
def setupLog(gv, prefix='PREFIX'):
    userName    = getpass.getuser()

    logFileName         = '/tmp/{PREFIX}_{USER}.log'.format(PREFIX=prefix, USER=userName)
    # logFileName         = os.path.abspath(os.path.relpath(logFileName))
    logConfigFileName   = '{CONFDIR}/{PREFIX}_LoggerConfig.ini'.format(CONFDIR=gv.Prj.configDIR, PREFIX=prefix)
    # logConfigFileName   = os.path.relpath(os.path.relpath(logConfigFileName))

    gv.Ln.initLogger(iniLogFile=logConfigFileName, logFileName=logFileName, package='MP3', packageQualifiers=2)
    logger = gv.Ln.setLogger(package="Main", CONSOLE=gv.INPUT_PARAM.LogCONSOLE)

    return logger