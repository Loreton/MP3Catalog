#!/usr/bin/env python3
#
#-*- coding: iso-8859-1 -*-
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys; sys.dont_write_bytecode = True
import os


################################################################################
# - M A I N
# - Imposta le variabili per fare l'import delle funzioni
# - Preleva alcuni parametri di input
# - Legge il file.ini
# - Chiama il vero main applicativo
################################################################################
import ProjectPackage   as Prj
if __name__ == "__main__":
    projectName='MP3Catalog'

    gv = Prj.setUpEnv(Prj, __file__, projectName=projectName, fDEBUG=False)
    calledBy = gv.LN.sys.calledBy


    # midName = 'MP3'
    # setattr(gv.Table, midName, gv.LnClass())
    # setattr("{0}.{1}".format(gv.Table, midName), 'name', 'TableName')
    # setattr(gv.Table[midName], 'name', 'TableName')
    # gv.Table()[midName] = gv.LnClass()
    # gv.Table.__dict__[midName] = gv.LnClass()
    # gv.Table.__dict__[midName].name = 'Ciao'
    # gv.Table()[midName], 'name', 'TableName')

    # gv.LN.dict.printDictionaryTree(gv, gv.Table, header="Global Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)




        # ---------------------------------------------------------
        # - SetUp del log
        # ---------------------------------------------------------
    gv.MAIN.DEBUG    = True
    logConfigFileName = os.path.join(gv.MAIN.mainConfigDIR, 'LoggerConfig.ini')
    if gv.MAIN.DEBUG:
        print ("    {0:<32}: {1}".format('Reading LOG configuration file', logConfigFileName))
    gv.MAIN.logFileName = gv.LN.logger.initLogger(loggerFile=logConfigFileName, package='LN-Protocol', packageQualifiers=2)
    logger              = gv.LN.logger.setLogger(gv, package="Main")
    if gv.MAIN.DEBUG:
        print ("    {0:<32}: {1}".format('using LOG file', gv.MAIN.logFileName))
    gv.MAIN.DEBUG    = False


    iniFileName = os.path.abspath(os.path.join(gv.MAIN.mainConfigDIR, projectName + '.ini'))
    gv.INI.configParser, gv.INI.dict = gv.LN.dict.readIniFile(gv, iniFileName, RAW=False, exitOnError=True)

    Prj.Main(gv)
    # gv.LN.dict.printDictionaryTree(gv, gv, header="Global Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)
