#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import ast



###############################################
# - InsertSong()
# - 1. Verifica se file passato esiste nel dictionary
# - 2. Se non esiste la inserisce.
###############################################
def insertSong(gv, songPath):
    logger  = gv.Ln.SetLogger(package=__name__)

        # prima colonna degli attributi (subito dopo il nome canzone)
    startAttributeCols = gv.song.field.SongName+1

        # -----------------------------------------------------
        # - Ci spostiamo nei campi primari della canzone
        # -      type.author.album.songName
        # - Se il path non esiste lo crea
        # - All'uscita dovremmo avere il ptr-->attributeCols
        # -----------------------------------------------------
    ptr = gv.song.dict
    for field in songPath[:startAttributeCols]:
        if not field in ptr:
            ptr[field] = gv.Ln.LnDict()
        ptr = ptr[field]

        # --------------------------------------------------
        # - facciamo il test di un attributo qualsiasi
        # - per verificare che la canzone abbia già i dati
        # --------------------------------------------------
    if not 'SongSize' in ptr:
        print ('....new entry', songPath)
            # su ogni canzone mettiamo i vari attributi di default
        for attributeName in gv.song.attributeCols:
            ptr[attributeName] = '.'

        ptr.SongSize = 0






















##############################################################
# - 1. Leggiamo la rootSourceDir
# - 2. Inseriamo ogni file nel dictionary (insertSong()
##############################################################
def merge(gv):
    logger  = gv.Ln.SetLogger(package=__name__)

        # --------------------------------------------------
        # - convertiamo il dictionary in una lista[]
        # --------------------------------------------------
    # gv.song.dict.printDict(gv)
    # ret = gv.song.dict.toList(gv)
    myDictTYPES = [dict, gv.Ln.LnDict]
    # gv.song.dict.printDict(gv)


    keyList = gv.song.dict.GetKeyList(fPRINT=True)
    gv.song.dict.PrintTree()

    sys.exit()
    ''' OK '''
    ret = gv.Ln.DictToList(gv.song.dict, myDictTYPES=myDictTYPES)
    # ret = gv.Ln.DictToList(gv, myDictTYPES=myDictTYPES)

    print ()
    print ()
    for index, item in enumerate(ret):
        print ('{0:02} - {1}'.format(index, item))
        gv.Ln.printDictValues(gv, pointer=item, myDictTYPES=myDictTYPES)

    sys.exit()








        # ---------------------------------------
        # - lettura directory sorgente di MP3
        # ---------------------------------------
    listaFile = gv.Ln.DirList(gv.ini.MAIN.MP3SourceDir, patternLIST=['*.mp3'], onlyDir=False, maxDeep=99)

    # numero del qualificatore subito doto la sourceDir
    firstRelField = len(gv.ini.MAIN.MP3SourceDir.split(os.path.sep))

        # ---------------------------------------
        # - inserimento...
        # ---------------------------------------
    for absName in listaFile:
        # fileSize = os.stat(absName).st_size             # get fileSize
        line    = absName.rsplit('.', 1)[0]                       # elimina extension
        relName = line.split(os.path.sep)[firstRelField:]    # elimina rootDir
        if relName[0].startswith('@'): continue
        if not relName[0] in gv.ini.MAIN.songType: continue
        insertSong(gv, relName)




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
    RECs = gv.Prj.ReadCSVFile(gv)

    if action == 'merge':
        merge(gv)
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
