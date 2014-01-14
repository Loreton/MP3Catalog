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


        processMandatorySongs(gv, mandatorySongsLIST)
        processRandomSongs(gv, randomSongsLIST)

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



# ############################################
# # Write MANDATORY Songs
# ############################################
def processMandatorySongs(gv, mandatorySongsLIST):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger

    print
    print
    print "%s # ############################################" % (' '*15)
    print "%s # # Write MANDATORY Songs" % (' '*15)
    print "%s # ############################################" % (' '*15)
    print

    bRecomended  =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
    if not bRecomended or gv.COPY.mandatorySONGS <= 0:
        return

    LOOP = True
    while LOOP:
        (gv.COPY.mandatorySONGS_written, gv.COPY.mandatorySONGS_remaining) = Prj.mp3.processSongs(gv, mandatorySongsLIST)
        print '\n'*2
        logger.console(LN.cGREEN + "mandatory songs have been written.....:%5d" % (gv.COPY.mandatorySONGS_written))
        logger.console(LN.cGREEN + "mandatory songs remainings............:%5d" % (gv.COPY.mandatorySONGS_remaining))

            # prepariamoci ad uscire
        gv.COPY.IGNORE_CRITERIA = False
        LOOP                    = False

        if gv.COPY.mandatorySONGS_remaining:
            logger.console(LN.cYELLOW + "Ci sono ancora canzoni Mandatory da scrivere.")
            choice = LN.sys.getKeyboardInput(gv, LN.cYELLOW + "      - Vuoi copiarle comunque ignorando i criteri richiesti?", validKeys=['yes', 'no'], exitKey='XQ', deepLevel=3, fDEBUG=False)
            if choice.upper() == 'YES':
                gv.COPY.IGNORE_CRITERIA = True
                LOOP                    = True



# ############################################
# # Write RANDOM Songs
# ############################################
def processRandomSongs(gv, randomSongsLIST):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger

    print
    print
    print "%s # ############################################" % (' '*15)
    print "%s # # Write RANDOM Songs" % (' '*15)
    print "%s # ############################################" % (' '*15)
    print



    if gv.COPY.randomSONGS <= 0:
        logger.console(LN.cRED + "Non ci sono canzoni risultanti dalla selezione richiesta.")
        return

    LOOP = True
    while LOOP:
        gv.COPY.randomSONGS_written, gv.COPY.randomSONGS_remaining = Prj.mp3.processSongs(gv, randomSongsLIST)
        print '\n'*2
        logger.console(LN.cGREEN + "Mandatory songs have been written..: %5d"   % (gv.COPY.randomSONGS_written))
        logger.console(LN.cGREEN + "Random    songs remaining..........: %5d"   % (gv.COPY.randomSONGS_remaining))

            # prepariamoci ad uscire
        gv.COPY.IGNORE_CRITERIA = False
        LOOP                    = False

        if gv.COPY.randomSONGS_remaining:
            logger.console(LN.cYELLOW + "Ci sono ancora canzoni valide da copiare.")
            choice = LN.sys.getKeyboardInput(gv, LN.cYELLOW + "      - Vuoi copiarle comunque ignorando i criteri richiesti?", validKeys=['yes', 'no'], exitKey='XQ', deepLevel=3, fDEBUG=False)
            if choice.upper() == 'YES':
                gv.COPY.IGNORE_CRITERIA = True
                LOOP                    = True

