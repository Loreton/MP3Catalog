#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys; sys.dont_write_bytecode = True

import platform
import os
import tempfile
import socket
# import dotmap

# ####################################################################
# # setUpEnv()
# ####################################################################
def setUpEnv(Prj, callerFileName, projectName=None, fDEBUG=False):

    mainModule = os.path.abspath(os.path.realpath(callerFileName))
    (mainModuleDIR, mainModuleName, mainModuleExt) = preparePaths(mainModule,    fDEBUG=fDEBUG)
    import LnFunctions as Ln


    # gv      = dotmap.DotMap()
    gv      = Prj.LnClass()
    gv.Prj  = Prj
    gv.LN   = Ln

        # ================================================================================
        # gv.LN.LnClass() e gv.Prj.LnClass() sono al momento intercambiabili e definite nei file:
        #      LnFunctions/__init__.py
        #      ProjectPackage/__init__.py
        # ================================================================================
    gv.LnClass = gv.LN.LnClass
    gv.MAIN     = gv.LnClass()  # definita nel file ProjectPackage/__init__.py

    gv.projectName          = projectName
    gv.MAIN.mainModuleDIR   = mainModuleDIR
    gv.MAIN.mainModuleName  = mainModuleName
    gv.MAIN.mainModuleExt   = mainModuleExt

    prepareMainEnv(gv, projectName)
    preparePrjEnv(gv)

    calledBy = gv.LN.sys.calledBy
    if fDEBUG:
        gv.LN.dict.printDictionaryTree(gv, gv, header="Global Vars [%s]" % calledBy(0), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)

    return gv





################################################################################
# preparePaths(gv)
# - inseriamo la lista delle dir dove possiamo trovare le LnFunctions
# - vale anche per quando siamo all'interno del .zip
################################################################################
def preparePaths(mainModule, fDEBUG=False):
    # global gv
    # mainModule                      = os.path.abspath(os.path.realpath(__file__))
    mainModuleDIR                   = os.path.dirname(mainModule)
    mainModuleName, mainModuleExt   = os.path.basename(mainModule).split('.')

    pathsLevels = [ '.', '../', '../../', '../../../', '../../../../' ]

    zipFnameList = ['LnFunctions_tag_V1.1.9.01.zip'] # All'interno dello zip deve esserci la dir LnFunction
    deepLevel = 3

    for i in reversed(range(deepLevel)):
        for zipName in zipFnameList:
            path = os.path.abspath(os.path.join(mainModuleDIR, pathsLevels[i], zipName))
            if os.path.isfile(path):
                sys.path.insert(0, path)

        path = os.path.abspath(os.path.join(mainModuleDIR, pathsLevels[i]))
        sys.path.insert(0, path)


    if fDEBUG:
        for path in sys.path:
            print ('......', path)

    return mainModuleDIR, mainModuleName, mainModuleExt


#######################################################
# prepareMainEnv(gv)
#######################################################
def prepareMainEnv(gv, projectName=None):

        # Classi che servono per il printDictionary
    # gv.myDictTYPES          = [LnClass, argparse.Namespace]
    # gv.myDictTYPES          = [gv.Prj.LnClass, gv.LN.LnClass]

        # Calcolo dello scriptDir
    gv.MAIN.scriptDir = os.path.dirname(os.path.abspath(sys.argv[0]))

    if gv.MAIN.scriptDir.split(os.sep)[-1].lower() in ['source', 'bin']:
        gv.MAIN.projectDir = os.path.abspath(gv.MAIN.scriptDir + os.sep + '..')
    else:
        gv.MAIN.projectDir = gv.MAIN.scriptDir

    sys.path.insert(0, gv.MAIN.scriptDir)
    if projectName:
        gv.MAIN.scriptName = projectName
    else:
        gv.MAIN.scriptName = os.path.basename(os.path.abspath(sys.argv[0])).split('.')[0]
        if gv.MAIN.scriptName == '__main__':
            gv.MAIN.scriptName = os.path.basename(gv.MAIN.projectDir)


    gv.MAIN.OpSys                = platform.system()
    gv.MAIN.fullHostName         = socket.gethostname() if socket.gethostname().find('.')>=0 else socket.gethostbyaddr(socket.gethostname())[0]
    gv.MAIN.shortHostName        = gv.MAIN.fullHostName.split('.')[0]

    gv.MAIN.OK                   = 0
    gv.MAIN.WARNING              = 1
    gv.MAIN.ERROR                = 2
    gv.MAIN.CRITICAL             = 3
    gv.MAIN.UNKNOWN              = 4

    gv.MAIN.fCONSOLE             = False
    gv.MAIN.fSYSLOG              = False
    gv.MAIN.fDEBUG               = False
    gv.MAIN.tempDir              = tempfile.gettempdir()
    gv.MAIN.tempDir              = '/tmp'
    gv.MAIN.logFileName          = "verra' valorizzato a run-time catturandolo dal file LoggerConfig.ini"

    gv.MAIN.mainConfigDIR        = os.path.abspath(os.path.join(gv.MAIN.projectDir, 'conf' ))
    gv.MAIN.mainDataDIR          = os.path.abspath(os.path.join(gv.MAIN.projectDir, 'data' ))
    gv.MAIN.iniMainConfigFile    = os.path.join(gv.MAIN.mainConfigDIR, gv.MAIN.scriptName+'.ini')


        # Conterrà i valori dei parametri di input
    gv.InpParam             = gv.LnClass()

        # Conterrà i valori dei parametri del file INI
    gv.INI                  = gv.LnClass()
    gv.INI_RAW              = gv.LnClass()





#######################################################
# preparePrjEnv(gv)
#######################################################
def preparePrjEnv(gv):
    gv.MainVars             = gv.LnClass()
    gv.extract              = gv.LnClass()

    gv.MP3                  = gv.LnClass()                     # Base per il Catalogo
    gv.MP3.Dict             = {}                            # Catalogo delle canzoni
    gv.MP3.TYPE             = gv.LnClass()

    gv.Table                = gv.LnClass()


