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

        # -------------------------------------------------------------------------------
        # - Leggiamo il file Excel di Input  e creiamo:
        #      il DB gv.MP3.Dict
        # -------------------------------------------------------------------------------
    Prj.excel.readCatalog(gv, gv.MP3.Dict)
    # sec0 = LN.time.now()
    songROWS = LN.dict.dictionaryToList(gv, gv.MP3.Dict, MaxDeepLevel=99)
    excelInitialLines = len(songROWS)
    # sec1 = LN.time.now()
    # print "impiegato: %d secondi" % (sec1-sec0)



        # -----------------------------------------------------------------------------------------
        # - Legge il fileSystem ed integra gv.MP3.Dict con eventuali modifiche/aggiunte trovate.
        # - Crea infine il file di Output in formato excel.
        # -----------------------------------------------------------------------------------------
    if gv.CONFIG.ACTION == 'MERGE':
        Prj.mp3.addFiles(gv)
        print "Converting dictionary to LIST..."
        songROWS = LN.dict.dictionaryToList(gv, gv.MP3.Dict, MaxDeepLevel=99)
        print "Adding filesystem song to Dictionary"
        songsAfterAdd = len(songROWS)
        print "Writing Dictionary to excel file: %s" % (gv.CONFIG.EXCEL_OUTPUT_FILE)
        Prj.excel.writeCatalog(gv, gv.CONFIG.EXCEL_OUTPUT_FILE, songROWS)

        print "Numero canzoni su foglio Excel...........: %6d" % (excelInitialLines)
        print "Numero canzoni dopo Merge dal fileSystem.: %6d" % (songsAfterAdd)


        # -----------------------------------------------------------------------------------------
        # - Estrae da gv.MP3.Dict i file con i criteri impostati nella ExtractSEction del file.cfg
        # - I file estratti verranno copiati nella directory specificata.
        # linee = LN.time.funcElapsed(partial(Prj.mp3.extractSong, gv, linee), fPRINT=True )
        # -----------------------------------------------------------------------------------------
    elif gv.CONFIG.ACTION == 'EXTRACT':
        songROWS = LN.dict.dictionaryToList(gv, gv.MP3.Dict, MaxDeepLevel=99)
        (gv.MP3.mandatorySONGS, gv.MP3.randomSONGS) = Prj.mp3.extractSongs(gv, inpList=songROWS)

        print "Numero canzoni su foglio Excel...........: %6d" % (excelInitialLines)
        print "Numero canzoni mandatory extracted.......: %6d" % (len(gv.MP3.mandatorySONGS))
        print "Numero canzoni random    extracted.......: %6d" % (len(gv.MP3.randomSONGS))


        bRecomended  =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
        if bRecomended:
            writtenMandatorySongs = Prj.mp3.processSongs(gv, gv.MP3.mandatorySONGS)
            print "[songs:%d] Mandatory songs have been written" % (writtenMandatorySongs)
            # ###################################
            choice=LN.sys.getKeyboardInput(gv, "* Mandatory songs have been written. Vuoi continuare? *", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
            # ###################################

        writtenRandomSongs = Prj.mp3.processSongs(gv, gv.MP3.randomSONGS)
        print "[songs:%d] Mandatory songs have been written" % (writtenMandatorySongs)
        print "[songs:%d] Random songs have been written" % (writtenRandomSongs)


        # --- DEBUG
        # if fPERCENT_DEBUG:
            # percentDict = gv.CONFIG.EXTRACT_SECTION['PERCENT']
            # LN.dict.printDictionaryTree(gv, percentDict, header="PERCENT dict data [%s]" % calledBy(0), retCols='TVL', lTAB=' '*4, console=True)

        xx = gv.CONFIG.FILE_MODULE
        xx.verifica()





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
