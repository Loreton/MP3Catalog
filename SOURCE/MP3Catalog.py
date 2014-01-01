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


        # --------------------------------------------------------------------
        # - Leggiamo il file Excel di Input (se richiesto) e creimao il DB
        # - Altrimenti lo creiamo nuovo
        # --------------------------------------------------------------------
    if gv.CONFIG.ACTION == 'MERGE':
        MP3Dict = Prj.excel.readCatalog(gv)
        # if fDEBUG:
        # LN.dict.printDictionaryTree(gv, gv.MP3Dict, header="Main Configuration File data [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)
        pass
        # Mp3Merge()

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


    return
    Prj.exit(gv, 9999, "Uscita Temporanea - [called by: %s] " % (calledBy(1)))
























    # cfgFile     = gv.INP_PARAM.mainCfgFile
    cfgDICT = Prj.readConfig(gv, gv.INP_PARAM.mainCfgFile, gv.INP_PARAM.SECTION_NAME)

    # (cfgMODULE, cfgDICT, cfgPATH, cfgFULLPATH) =  LN.dict.loadDictFile(gv, cfgFile, moduleName=None, fDEBUG=False)
    if not cfgDICT:
        Prj.exit(gv, 11, "[%-12s] - file %s NOT Found. It's mandatory." % (gv.projectID, cfgFile) )


    if gv.INP_PARAM.SECTION_NAME == None:
        Prj.exit(gv, 12, "[%-12s] - Immettere il nome della sezione. It's mandatory." )
    else:
        sectionID = cfgDICT.get(gv.INP_PARAM.SECTION_NAME, {})

    # for section in cfgDICT.sections():        print section

    if gv.INP_PARAM.fDEBUG:
        print "ciao"
        LN.dict.printDictionaryTree(gv, vars(sectionID), retCols='TV', lTAB=' '*4, console=True)

    print sectionID
    if not hasattr(cfgDICT, "Main"):
        Prj.exit(gv, 11, "Main{} section NOT present in file"  )


if __name__ == "__main__":
    Main(sys.argv)