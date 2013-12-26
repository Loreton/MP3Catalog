#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per la cercare di rendere leggibile un libro pdf
#           da cui è stato prelevato tutto il testo con copy/paste
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os
import platform
import ConfigParser

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




# #############################################################################
# # global Vars()
# #############################################################################
gv              = myClass()                   # Global variable di progetto
gv.OpSys        = platform.system()



################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    gv.packageName  = 'MP3Catalog'               # directory del sorgente
    gv.projectID    = 'MP3Catalog'
    gv.scriptName    = gv.projectID


    thisModuleDIR   = os.path.dirname(os.path.realpath(__file__))
    if thisModuleDIR.endswith('.zip'): packageDir = gv.projectID


        # --------------------------------------------------------------------------------------
        # - determina tutte le path necessarie al buon funzionamento
        # --------------------------------------------------------------------------------------
    preparePATHs(gv, fDEBUG=False)

        # --------------------------------------------------------------------------------------
        # - Possiamo fare l'import del LNPackage (se serve) nel percorso ed importiamo il package
        # --------------------------------------------------------------------------------------
    import ProjectPackage as Prj
    import LnFunctions as LN
    gv.LN       = LN
    gv.Prj      = Prj


        # --------------------------------------------------------
        # - Leggiamo il file di configurazione di base
        # - Qui troviamo:
        # - 1. le caratteristiche del file di log
        # - 2. Eventual uteriori variabili utili per il progetto
        #  - ritorna le variabili nelle classi:
        #  -    gv.INI_LOG  = log
        #  -    gv.INI_MAIN = iniMAIN
        # --------------------------------------------------------
    iniFileName = gv.scriptName + '.ini' if gv.OpSys.upper() != 'WINDOWS' else gv.scriptName + 'Win.ini'
    Prj.setup.readIniConfigFile(gv, os.path.join(gv.mainConfigDIR, iniFileName))    # imposta le variabili del fine.ini in gv.INI_LOG e gv.INI_MAIN

        # --------------------------------------------------------
        # SetUp del log
        # --------------------------------------------------------
    Prj.setup.initLog(gv, gv.INI_LOG)


        # --------------------------------------------------------
        # Impostazione di alcune variabili statiche per il progetto
        # --------------------------------------------------------
    Prj.setup.setVariables(gv)                                               # Imposta i valori JBStatus

        # --------------------------------------------------------------------------
        # - Controllo dei parametri passati a riga di comando
        # - da qui ricavo info sul nome del file di configurazione applicativo
        #  - ritorna le variabili nella classe:
        #  -    gv.args
        # --------------------------------------------------------------------------
    Prj.setup.parseInput(gv)        # return to gv.args




    if gv.OpSys.upper() == 'WINDOWS':
        pass
        # gv.PVEXE = LN.file.getFullPath(gv, 'pv.exe', 'PATH', exitOnError=True)


    # LN.dict.printDictionaryTree(gv, gv, retCols='TV', lTAB=' '*4, console=True)
        # --------------------------------------------------------
        # Impoort del Main module e lancio
        # --------------------------------------------------------
    import MP3Catalog as mainPrj
    mainPrj.Main(gv, sys.argv)


