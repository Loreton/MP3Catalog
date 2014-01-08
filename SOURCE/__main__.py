#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os
import platform

sys.dont_write_bytecode = True

class myClass():    pass






# #############################################################################
# # preparePATHs()
# # Impostazione delle PATHs
# # La scriptDir è la current dir a meno che:
# # non finisce con .zip - nel qual caso saliamo di un livello.
# # non finisce con /bin - nel qual caso saliamo di una subDir.
# #############################################################################
def preparePATHs(gv, fDEBUG=False):

    thisModuleDIR   = os.path.dirname(os.path.realpath(__file__))
    scriptBase      = thisModuleDIR
    subDirs         = thisModuleDIR.split(os.sep)

    if thisModuleDIR.endswith('.zip'):
        ZIP = True
        (MAINDIR, PRJBASEDIR, PRJBINDIR ) = ( -2, -2, -1)
        packageName = gv.packageName
    else:
        ZIP = False
        packageName = gv.packageName + '_Source'
        (MAINDIR, PRJBASEDIR) = ( -2, -1)

    PrjBaseDir      = os.sep.join(subDirs[:PRJBASEDIR])
    PrjBinDir      = os.path.join(PrjBaseDir, 'bin')    # dovrebbe essere la BIN
    PrjPackageDir   = thisModuleDIR
    LnPackageDir    = os.sep.join(subDirs[:MAINDIR])
    mainConfigDIR   = os.path.join(PrjBaseDir, 'conf' )



    myPaths = [
            # os.path.normpath('%s/conf'                   % (PrjBinDir) ),
        ]

    if ZIP:
        myPaths.extend([
            os.path.normpath('%s'                   % (PrjBinDir) ),
            os.path.normpath('%s'                   % (PrjBaseDir) ),
            os.path.normpath('%s'                   % (PrjPackageDir)),
        ])
    else:
        myPaths.extend([
            os.path.normpath('%s'                   % (PrjBinDir) ),
            os.path.normpath('%s/LnFunctions'       % (LnPackageDir)), # In caso di ZIP non serve
            os.path.normpath('%s'                   % (LnPackageDir)),
            os.path.normpath('%s'                   % (PrjPackageDir)),
        ])

    myPaths.reverse()
    for path in myPaths:  sys.path.insert(0, path)

    os.environ['PYTHONPATH']    = os.pathsep.join(myPaths)

    gv.scriptDir        = scriptBase
    gv.pythonPATH       = myPaths
    gv.mainConfigDIR    = mainConfigDIR
    gv.LnPackageDir     = LnPackageDir
    gv.PrjPackageDir     = PrjPackageDir
    gv.PrjBinDir     = PrjBinDir
    gv.PrjBaseDir     = PrjBaseDir
    gv.TAB          = ' '*5 # Spazio inizio riga per il print


    # fDEBUG = True
    if fDEBUG:
        print
        print 'scriptDir        = %s' % (gv.scriptDir)
        print
        print 'LnPackageDir     = %s' % (gv.LnPackageDir)
        print 'PrjBaseDir       = %s' % (PrjBaseDir)
        print 'PrjBinDir        = %s' % (PrjBinDir)
        print 'PrjPackageDir    = %s' % (PrjPackageDir)
        print 'mainConfigDIR    = %s' % (gv.mainConfigDIR)
        print
        print 'scriptName.....', gv.scriptName
        print 'projectID......', gv.projectID
        print 'PYTHONPATH......'
        print
        for path in os.getenv('PYTHONPATH').split(os.pathsep):
            print "     ", path
        print



################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    gv              = myClass()                   # Global variable di progetto
    gv.OpSys        = platform.system()
    gv.packageName  = 'MP3Catalog'               # directory del sorgente
    gv.projectID    = 'MP3Catalog'
    gv.scriptName    = gv.projectID

    preparePATHs(gv, fDEBUG=False)


        # --------------------------------------------------------------------------------------
        # - inseriamo il path del LNPackage (se serve) nel percorso ed importiamo il package
        # --------------------------------------------------------------------------------------
    import      ProjectPackage as Prj
    import      LnFunctions as LN
    gv.LN       = LN
    gv.Prj      = Prj
    calledBy    = LN.sys.calledBy

    logger      = gv.LN.logger          #  Ancora non lo abbiamo impostato
    logger.setConsoleAnyway(False)

    # LN.dict.printDictionaryTree(gv, gv, header="Main variables [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)
    # sys.exit()


        # ------------------------------------------------------------------------------------
        # - Inizializzazione di variabili globali
        # ------------------------------------------------------------------------------------
    Prj.setup.initVariables(gv)                                               # Imposta i valori JBStatus

        # ------------------------------------------------------------------------------------
        # - Leggiamo il file di configurazione di base per inizializzare il file di LOG
        # ------------------------------------------------------------------------------------
    iniFileName = gv.scriptName + '.ini' if gv.OpSys.upper() != 'WINDOWS' else gv.scriptName + 'Win.ini'
    logInfo     = Prj.setup.readIniConfig(gv, os.path.join(gv.mainConfigDIR, iniFileName))


        # --------------------------------------------------------
        # - SetUp del log
        # --------------------------------------------------------
    Prj.setup.initLog(gv)



        # --------------------------------------------------------
        # - CALL Project MAIN Program
        # --------------------------------------------------------
    import MP3Catalog as MP3Catalog

    MP3Catalog.Main(gv, sys.argv)

    choice = LN.sys.getKeyboardInput(gv, "Procedura completata con successo - Press ENTER to exit.", validKeys='ENTER', exitKey='X')

    Prj.exit(gv, 9000, "Procedura completata con successo - [called by: %s] " % (calledBy(0)))

