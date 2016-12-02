#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import ast




################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv, action):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()
    gv.data = gv.Ln.LnDict()


        # ---------- E X C E L
    xlsFile      = os.path.abspath(os.path.join(gv.Prj.dataDIR, gv.INPUT_PARAM.excelFile))
    csvFileInput = gv.Prj.ReadExcelDB(gv, xlsFile, gv.ini.EXCEL.RangeToProcess)
    csvFileMerged = xlsFile.rsplit('.', -1)[0] + '.merged.csv'

    requiredColNames = ';'.join(gv.song.colsName)
    RECs = gv.Prj.ReadCSVFile(gv, csvFileInput, requiredColNames)

    # gv.song.dict.PrintTree(fEXIT=True, MaxLevel=3)

    if action == 'merge':
        mergedLIST = gv.Prj.Merge(gv, gv.ini.MAIN.MP3SourceDir, gv.song.dict)
            # -----------------------------------------------------------------------
            # - Salviamo il tutto in formato csv
            # -----------------------------------------------------------------------
        # for line in mergedLIST: print (line)

        gv.Prj.WriteCSVFile(gv, csvFileMerged, mergedLIST)
        print ()
        C.printYellowH('file: {0} has been saved.'.format(csvFileMerged), tab=4)
        # gv.song.PrintTree(MaxLevel=2)
        sys.exit()


    fileScartate        = '{ROOT}/tmp/_Scartate.csv'.format(ROOT=gv.Prj.dataDIR)
    fileAnalizzate      = '{ROOT}/tmp/_Analizzate.csv'.format(ROOT=gv.Prj.dataDIR)
    fileValidSongs      = '{ROOT}/tmp/_ValidSongs.csv'.format(ROOT=gv.Prj.dataDIR)
    fileDuplicateSongs  = '{ROOT}/tmp/_DuplicateSongs.csv'.format(ROOT=gv.Prj.dataDIR)
    fileNotFoundSongs   = '{ROOT}/tmp/_NotFoundSongs.csv'.format(ROOT=gv.Prj.dataDIR)

        # ----------------------------------------------
        # - Preleviamo tutte le canzoni analizzate
        # - Analizzata;Recomended;Loreto;Buona;Soft;Vivace;Molto Viv;Camera;Car;Lenta;Count
        # ----------------------------------------------
    gv.songList = gv.Ln.LnDict()
    gv.songList.validSongs  = [gv.song.colsName]  # init LIST con il nome delle colonne
    gv.songList.analizzate  = [gv.song.colsName]  # init LIST con il nome delle colonne
    gv.songList.scartate    = [gv.song.colsName]  # init LIST con il nome delle colonne
    gv.songList.duplicate   = [gv.song.colsName]  # init LIST con il nome delle colonne

    gv.Prj.songFilter(gv, RECs)


    # - Salvataggio dei dati solo per DEBUG
    choice = gv.Ln.getKeyboardInput("    Vuoi salvare i dati sui relativi file?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
    if choice.lower() in ['yes']:
        # songList    = gv.songList
        msg = 'writing file: {0}'.format(fileScartate)
        C.printYellow(msg, tab=4); logger.info(msg)
        gv.Ln.writeTextFile(fileScartate,   data=gv.songList.scartate)

        C.printYellow('writing file: {0}'.format(fileValidSongs), tab=4)
        gv.Ln.writeTextFile(fileValidSongs,   data=gv.songList.validSongs)

        C.printYellow('writing file: {0}'.format(fileAnalizzate), tab=4)
        gv.Ln.writeTextFile(fileAnalizzate, data=gv.songList.analizzate)


    if action == 'copySongs':
        copySong    = None
        gv.fEXECUTE = gv.INPUT_PARAM.fEXECUTE
        RECs = gv.songList.validSongs[:]
        logger.info('trovate {0} canzoni da copiare'.format(len(RECs)))

        if gv.INPUT_PARAM.fCHECK_SOURCE:
            gv.Prj.checkSourceSongs(gv, RECs)

        else:
            choice = gv.Ln.getKeyboardInput("    Continuare per copiare le canzoni sulla destinazione?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
            if choice.lower() in ['x', 'no']:
                sys.exit()

            copySong = gv.Prj.copySongs(gv, RECs)
            print()
            C.printYellow('writing file: {0}'.format(fileDuplicateSongs), tab=4)
            print()
            gv.Ln.writeTextFile(fileDuplicateSongs, data=gv.songList.duplicate)
            print()
            C.printYellow('writing file: {0}'.format(fileNotFoundSongs), tab=4)
            print()
            gv.Ln.writeTextFile(fileNotFoundSongs, data=copySong.NOTFOUND)

            # gv.copySong.printDict(gv)

    else:
        C.printRed('Action {0} not yet implemented...!'.format(action), tab=8)
        sys.exit()

    gv.Ln.Exit(0, "--------------- debugging exit ----------------", printStack=True, stackLevel=9, console=True)
