#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


# RSync log interpretation: http://stackoverflow.com/questions/4493525/rsync-what-means-the-f-on-rsync-logs

import os, sys

################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv, args):
    LN          = gv.LN
    Prj         = gv.Prj
    calledBy    = gv.LN.sys.calledBy

        # --------------------------------------------------------------------------
        # - lettura degli Input parameters
        # --------------------------------------------------------------------------
    options = Prj.setup.parseInput(gv)
    fDEBUG = gv.INP_PARAM.fDEBUG
    # if fDEBUG: LN.dict.printDictionaryTree(gv, gv, header="INPUT Parameters [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)




        # =======================================
        # - Lettura del file di configurazione
        # =======================================
    cfgDICT    = Prj.setup.readProjectConfig(gv, cfgFileName=gv.INP_PARAM.mainCfgFile)
    if fDEBUG: LN.dict.printDictionaryTree(gv, cfgDICT, header="Main Configuration File data [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)


        # -------------------------------------------------------------------------------
        # - Leggiamo il file Excel di Input  e creiamo il DB gv.MP3Dict
        # -------------------------------------------------------------------------------
    Prj.excel.readCatalog(gv)
    linee = LN.dict.dictionaryToList(gv, gv.MP3Dict, MaxDeepLevel=99)
    SongNumberExcel = len(linee)
    # LN.dict.printDictionaryTree(gv, gv.MP3Dict, header="Excel File data [%s]" % calledBy(0), retCols='T', lTAB=' '*4, console=True)


    if gv.CONFIG.ACTION == 'MERGE':
        Prj.mp3.addFiles(gv)
        linee = LN.dict.dictionaryToList(gv, gv.MP3Dict, MaxDeepLevel=99)
        SongNumberAfterAdd = len(linee)
        # LN.dict.printDictionaryTree(gv, gv.MP3Dict, header="After FileSystem data [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)
        Prj.excel.writeCatalog(gv, gv.CONFIG.EXCEL_OUTPUT_FILE)

    elif gv.CONFIG.ACTION == 'EXTRACT':
        pass
        # extractedFile = Mp3Extract()

    elif gv.CONFIG.ACTION == 'RANDOM':
        pass
        # extractedDict = Mp3Extract()
        # RandomExtract(extractedDict)

    # ---------------
        # choice = LN.sys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
    # ---------------

    elif gv.CONFIG.ACTION == 'DISPLAY':
        pass
        # MP3Catalog.Mp3Display(iniDB, dir2Scan=globalARGs[INPUT_ARG_INPDIR ], excelInputFile=globalARGs[EXCEL_OUTPUT_FILE])

    else:
        print gv.CONFIG.ACTION
        Msg1 = "Should NOT Occur.\n"
        print Msg1
        Prj.exit(gv, 10, Msg1, stackLevel=2)

    print "Process completed."
    print "Numero canzoni su foglio Excel...........: %6d" % (SongNumberExcel)
    print "Numero canzoni dopo ADD dal fileSystem...: %6d" % (SongNumberAfterAdd)


    return
    Prj.exit(gv, 9999, "Uscita Temporanea - [called by: %s] " % (calledBy(1)))



