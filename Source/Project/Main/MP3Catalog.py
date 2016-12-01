#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import ast


##############################################################
# - 1. Leggiamo la rootSourceDir
# - 2. Inseriamo ogni file nel dictionary
##############################################################
def merge(gv, csvFile, csvFormat):
    logger  = gv.Ln.SetLogger(package=__name__)

    # gv.song.printDict(gv)
    # gv.song.field.PrintTree()
    # gv.song.PrintValue(['field'])
    # gv.song.field.PrintValue()
    # sys.exit()


        # ---------------------------------------
        # - lettura directory sorgente di MP3
        # ---------------------------------------
    listaFile = gv.Ln.DirList(gv.ini.MAIN.MP3SourceDir, patternLIST=['*.mp3'], onlyDir=False, maxDeep=99)
    if listaFile == []:
        gv.Ln.Exit(43, 'non sono stati trovati file nella directory indicata: {0}'.format(gv.ini.MAIN.MP3SourceDir))



        # ---------------------------------------
        # - inserimento...nuove canzoni
        # ---------------------------------------
        # numero del qualificatore subito doto la sourceDir
    firstRelField = len(gv.ini.MAIN.MP3SourceDir.split(os.path.sep))
    for absName in listaFile:
        line            = absName.rsplit('.', 1)[0]                       # elimina extension
        relativeName    = line.split(os.path.sep)[firstRelField:]    # elimina rootDir
        if relativeName[0].startswith('@'): continue
        if not relativeName[0] in gv.ini.MAIN.songType: continue

            # ------------------------
            # - inserimento canzone
            # ------------------------
        ptr = gv.song.dict.Ptr(relativeName, create=True)
        if not 'SongSize' in ptr:
            print ('....new entry', relativeName)
                # su ogni canzone mettiamo i vari attributi di default
            for attributeName in gv.song.attributeCols:
                ptr[attributeName] = '.'
            ptr.SongSize = 0

        # - print di tutto il dict
    gv.song.dict.PrintTree(fEXIT=True)

        # -----------------------------------------------------------------------
        # - otteniamo una lista della struttura del dict dove ogni entry
        # - è una lista che contiene i token del tree della canzone
        #   ['Bambini', 'Cartoni', 'The best of', 'Anna Dai Capelli Rossi']
        #   ['Bambini', 'Cartoni', 'The best of', 'Arale Avventura']
        #   ['Bambini', 'Cartoni', 'The best of', 'Arrivano I Superboys' ]
        #   ['Bambini', 'Cartoni', 'The best of', 'Astro Robot' ]
        # -----------------------------------------------------------------------
    keyList = gv.song.dict.KeyList()

        # -----------------------------------------------------------------------
        # - Per ogni canzone verifichiamo se esiste il file.
        # - Se non esiste mettiamo songSize=0 nel caso dovesse
        # -   essere necessario copiare gli attributi per poi cancellarle.
        # - Allo stesso tempo leggiamo gli attributi e creiamo una nuova lista
        # - da scrivere in un file CSV.
        # -----------------------------------------------------------------------
    mergedLIST = []
    for songQualifiers in keyList:
        if songQualifiers == []: continue

        fileName = os.path.sep.join(songQualifiers)
        fileName = '{0}{1}{2}.mp3'.format(gv.ini.MAIN.MP3SourceDir, os.path.sep, fileName)

        if os.path.isfile(fileName):
            size = os.stat(fileName).st_size

        else:
            size = 0 # in modo che posso copiare gli attrivuti e poi cancellarle.
            print('     no more exists...', fileName)

        # - pointer alla canzone
        ptrSong = gv.song.dict.Ptr(songQualifiers)
        # - set size
        ptrSong.SongSize = size
        # - get song attributes values
        songAttr = ptrSong.GetValue()

        # -------------------------------------
        # - Inseriamo la canzone nella lista
        # - che salveremo come merged CSV
        # -------------------------------------
        newSong = songQualifiers[:]
        for attributeName, val in songAttr.items():
            # print ('    ', attributeName, val)
            newSong.append(val)

        mergedLIST.append(newSong)

    # -----------------------------------------------------------------------
    # - Salviamo il tutto in formato csv
    # -----------------------------------------------------------------------
    # for line in mergedLIST: print (line)
    gv.Prj.WriteCSVFile(gv, csvFile, mergedLIST, csvFormat)





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


        # ritorna una lista di canzoni (lista a sua volta)
        # SONGS[
        #       song1[...]
        #       song2[...]
        #      ]

        # -------------------------------------------
        # - Export del file excel se richiesto
        # -------------------------------------------

        # - tipo di csv da usare
    csvFormat = gv.ini.MAIN.csvFormat
    logger.debug('CSV format type: {0}'.format(csvFormat))

        # ========================================
        # - Build Excel FileName
        # ========================================
    xlsFile = os.path.abspath(os.path.join(gv.Prj.dataDIR, gv.INPUT_PARAM.excelFile))
    csvFileInput  = xlsFile.rsplit('.', -1)[0] + '.csv'
    csvFileMerged = xlsFile.rsplit('.', -1)[0] + '.merged.csv'

    logger.debug('XLS file name:    {0}'.format(xlsFile))
    logger.debug('CSV file name:    {0}'.format(csvFileInput))


        # - Se il csv è più vecchio dell'xls facciamo l'export
    if gv.Ln.Fmtime(xlsFile) > gv.Ln.Fmtime(csvFileInput):
        logger.debug('range To process: {}'.format(gv.ini.EXCEL.RangeToProcess))
        mydata  = gv.Ln.Excel(xlsFile)
        mydata.exportCSV('Catalog', csvType=csvFormat, outFname=csvFileInput, rangeString=gv.ini.EXCEL.RangeToProcess, colNames=4)
    else:
        logger.debug('excel file is older than CSV file. No export will take place.')

    RECs = gv.Prj.ReadCSVFile(gv, csvFileInput, csvFormat)

    if action == 'merge':
        gv.song.dict.PrintTree(fEXIT=True)
        merge(gv, csvFileMerged, csvFormat)
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
