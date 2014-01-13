#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


# RSync log interpretation: http://stackoverflow.com/questions/4493525/rsync-what-means-the-f-on-rsync-logs

import os, sys
from functools import partial
import random


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
        songLIST = LN.dict.dictionaryToList(gv, gv.MP3.Dict, MaxDeepLevel=99)
        (gv.MP3.mandatorySONGS, gv.MP3.randomSONGS) = Prj.mp3.extractSongs(gv, inpList=songLIST)

        logger.console("Numero canzoni su foglio Excel...........: %6d" % (excelInitialLines))
        logger.console("Numero canzoni mandatory extracted.......: %6d" % (len(gv.MP3.mandatorySONGS)))
        logger.console("Numero canzoni random    extracted.......: %6d" % (len(gv.MP3.randomSONGS)))


        bRecomended  =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
        if bRecomended:
            writtenMandatorySongs, restLines = Prj.mp3.processSongs(gv, gv.MP3.mandatorySONGS)
            logger.console("[%d] mandatory songs have been written" % (writtenMandatorySongs))
            choice=LN.sys.getKeyboardInput(gv, "* Mandatory songs have been written. Vuoi continuare? *", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)



        writtenRandomSongs, restLines = Prj.mp3.processSongs(gv, gv.MP3.randomSONGS)
        logger.console("[%5d] Mandatory songs have been written"   % (writtenMandatorySongs))
        logger.console("[%5d] Random    songs have been written"   % (writtenRandomSongs))


        if restLines > 0:
            cfgModule.verifica()
            logger.console("Sono rimaste %d canzoni") % (restLines)
            choice=LN.sys.getKeyboardInput(gv, "* Vuoi continuare? *", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
        else:
            logger.console("NON sono presenti ulteriori canzoni. Processo completato.")


        cfgModule.verifica()


        # --- DEBUG
        # if fPERCENT_DEBUG:
            # percentDict = gv.CONFIG.EXTRACT_SECTION['PERCENT']
            # LN.dict.printDictionaryTree(gv, percentDict, header="PERCENT dict data [%s]" % calledBy(0), retCols='TVL', lTAB=' '*4, console=True)








    # ---------------
        # choice = LN.sys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
    # ---------------

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
