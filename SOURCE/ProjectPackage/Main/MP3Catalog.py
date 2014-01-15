#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
from functools import partial


################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv, args):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy

        # --------------------------------------------------------------------------
        # - lettura degli Input parameters
        # --------------------------------------------------------------------------
    options = Prj.setup.parseInput(gv)
    fDEBUG = gv.INP_PARAM.fDEBUG

        # =======================================
        # - Lettura del file di configurazione
        # =======================================
    cfgDICT    = Prj.setup.readProjectConfig(gv, cfgFileName=gv.INP_PARAM.mainCfgFile)
    cfgModule  = gv.CONFIG.FILE_MODULE

        # -------------------------------------------------------------------------------
        # - Leggiamo il file Excel di Input  e creiamo:
        #      il DB gv.MP3.Dict
        # -------------------------------------------------------------------------------
    Prj.excel.readCatalog(gv, gv.MP3.Dict)
    # sec0 = LN.time.now()
    songLIST = LN.dict.dictionaryToList(gv, gv.MP3.Dict, MaxDeepLevel=99)
    excelInitialLines = len(songLIST)
    # sec1 = LN.time.now()
    # print "impiegato: %d secondi" % (sec1-sec0)



        # -----------------------------------------------------------------------------------------
        # - Legge il fileSystem ed integra gv.MP3.Dict con eventuali modifiche/aggiunte trovate.
        # - Crea infine il file di Output in formato excel.
        # -----------------------------------------------------------------------------------------
    if gv.CONFIG.ACTION == 'MERGE':
        logger.console("Adding filesystem song to Dictionary")
        Prj.mp3.addFiles(gv)

        logger.console("Converting dictionary to LIST...")
        songLIST = LN.dict.dictionaryToList(gv, gv.MP3.Dict, MaxDeepLevel=99)

        logger.console("Writing Dictionary to excel file: %s" % (gv.CONFIG.EXCEL_OUTPUT_FILE))
        nLines = Prj.excel.writeCatalog(gv, gv.CONFIG.EXCEL_OUTPUT_FILE, songLIST)

        logger.console("Numero canzoni su foglio Excel...........: %6d" % (excelInitialLines))
        logger.console("Numero canzoni dopo Merge dal fileSystem.: %6d" % (nLines))


        # -----------------------------------------------------------------------------------------
        # - Estrae da gv.MP3.Dict i file con i criteri impostati nella ExtractSEction del file.cfg
        # - I file estratti verranno copiati nella directory specificata.
        # linee = LN.time.funcElapsed(partial(Prj.mp3.extractSong, gv, linee), fPRINT=True )
        # -----------------------------------------------------------------------------------------
    elif gv.CONFIG.ACTION == 'EXTRACT':

            # -------------------------------
            # - Estrazione Canzoni
            # -------------------------------
        songLIST = LN.dict.dictionaryToList(gv, gv.MP3.Dict, MaxDeepLevel=99)
        (mandatorySongsLIST, randomSongsLIST) = Prj.mp3.extractSongs(gv, inpList=songLIST)
        gv.COPY.mandatorySONGS  = len(mandatorySongsLIST)
        gv.COPY.randomSONGS     = len(randomSongsLIST)

        print '\n'*2
        logger.console(LN.cGREEN + "Numero canzoni su foglio Excel...........: %6d" % (excelInitialLines))
        logger.console(LN.cGREEN + "Numero canzoni mandatory extracted.......: %6d" % (gv.COPY.mandatorySONGS))
        logger.console(LN.cGREEN + "Numero canzoni random    extracted.......: %6d" % (gv.COPY.randomSONGS))


        Prj.main.processMandatorySongs(gv, mandatorySongsLIST)
        Prj.main.processRandomSongs(gv, randomSongsLIST)

        LN.sys.getKeyboardInput(gv, LN.cYELLOW + "* Presse ENTER ver visualizzare il report", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
        cfgModule.verifica()
        LN.dict.printDictionaryTree(gv, gv.COPY, header="COPY dict data [%s]" % calledBy(0), retCols='TVL', lTAB=' '*4, console=True)

    else:
        print gv.CONFIG.ACTION
        Msg1 = "Should NOT Occur.\n"
        print Msg1
        Prj.exit(gv, 10, Msg1, stackLevel=2)

    print "Process completed."


    return
    Prj.exit(gv, 0, "Uscita Temporanea - [called by: %s] " % (calledBy(1)))



    # ###################################
    # choice=LN.sys.getKeyboardInput(gv, "******* STOP Temporaneo *******", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
    # LN.dict.printDictionaryTree(gv, gv.MP3.Dict, header="Excel File data [%s]" % calledBy(0), retCols='T', lTAB=' '*4, console=True)
    # ###################################

