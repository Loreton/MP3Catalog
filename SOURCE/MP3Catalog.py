#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


# RSync log interpretation: http://stackoverflow.com/questions/4493525/rsync-what-means-the-f-on-rsync-logs

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
        #      la LIST gv.EXCEL.ROWS[]
        # -------------------------------------------------------------------------------
    Prj.excel.readCatalog(gv, gv.MP3.Dict)
    excelInitialLines = len(gv.EXCEL.ROWS)


        # -----------------------------------------------------------------------------------------
        # - Legge il fileSystem ed integra gv.MP3.Dict con eventuali modifiche/aggiunte trovate.
        # - Crea infine il file di Output in formato excel.
        # -----------------------------------------------------------------------------------------
    if gv.CONFIG.ACTION == 'MERGE':
        Prj.mp3.addFiles(gv)
        Prj.excel.writeCatalog(gv, gv.CONFIG.EXCEL_OUTPUT_FILE, outLines)

        print "Numero canzoni su foglio Excel...........: %6d" % (excelInitialLines)
        print "Numero canzoni dopo Merge dal fileSystem.: %6d" % (totalSongs)


        # -----------------------------------------------------------------------------------------
        # - Estrae da gv.MP3.Dict i file con i criteri impostati nella ExtractSEction del file.cfg
        # - I file estratti verranno copiati nella directory specificata.
        # linee = LN.time.funcElapsed(partial(Prj.mp3.extractSong, gv, linee), fPRINT=True )
        # -----------------------------------------------------------------------------------------
    elif gv.CONFIG.ACTION == 'EXTRACT':
        songLIST = None
        songLIST = gv.EXCEL.ROWS
        (gv.MP3.mandatorySONGS, gv.MP3.randomSONGS) = Prj.mp3.extractSongs(gv, inpList=songLIST)

        print "Numero canzoni su foglio Excel...........: %6d" % (excelInitialLines)
        print "Numero canzoni random    extracted.......: %6d" % (len(gv.MP3.randomSONGS))
        print "Numero canzoni mandatory extracted.......: %6d" % (len(gv.MP3.mandatorySONGS))


        # sMP3DestDir         =  gv.CONFIG.EXTRACT_SECTION['MP3 Destination Directory']
        # sExtractOrder       =  gv.CONFIG.EXTRACT_SECTION['Extraction Order']
        # lPunteggioRange     =  gv.CONFIG.EXTRACT_SECTION['Punteggi']
        # bPrefixSong         =  gv.CONFIG.EXTRACT_SECTION['PrefixSong']     # Mette <N.Cognome-> dell'autore prima del titolo della canzone All'interno del folder Type
        bRecomended         =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
        if bRecomended:
            Prj.mp3.copySongs(gv, gv.MP3.mandatorySONGS)


        Prj.mp3.copySongs(gv, gv.MP3.randomSONGS)





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
    Prj.exit(gv, 9999, "Uscita Temporanea - [called by: %s] " % (calledBy(1)))



    # ###################################
    # choice=LN.sys.getKeyboardInput(gv, "******* STOP Temporaneo *******", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
    # LN.dict.printDictionaryTree(gv, gv.MP3.Dict, header="Excel File data [%s]" % calledBy(0), retCols='T', lTAB=' '*4, console=True)
    # ###################################
