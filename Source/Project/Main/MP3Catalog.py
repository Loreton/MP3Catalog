#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import ast



###############################################
# -
###############################################
def insertSong(gv, song):
    logger  = gv.Ln.SetLogger(package=__name__)

        # ===========================================
        #  - Inserimento di un nuovo record
        # ===========================================
    # mp3Dict = gv.song.dict

    ptr = gv.song.dict
    startAttributeCols = gv.song.field.SongName+1

        # - creazione dictionary per type.author.album.songName
    for field in song[:startAttributeCols]:
        if not field in ptr:
            ptr[field] = gv.Ln.LnDict()
        ptr = ptr[field]

        if gv.song.attributeCols[0] in ptr:
            pass
        else:
            print ('....new entry', song)
                # su ogni canzone mettiamo i vari attributi di default
            for index, value in enumerate(song[startAttributeCols:]):
                attrName  = gv.song.attributeCols[index]
                ptr[attrName] = '.'


###############################################
# -
###############################################
def merge(gv):
    logger  = gv.Ln.SetLogger(package=__name__)
    mp3Dict = gv.song.dict

    # lettura directory
    listaFile = gv.Ln.DirList(gv.ini.MAIN.MP3sourceDir, patternLIST=['*.mp3'], onlyDir=False, maxDeep=99)
    firstField = len(gv.ini.MAIN.MP3sourceDir.split(os.path.sep))
    for line in listaFile:
        line = line.rsplit('.', 1)[0]
        record = line.split(os.path.sep)[firstField:]
        if not record[0] in gv.ini.MAIN.songType: continue
        if record[0].startswith('@'): continue
        insertSong(gv, record)
        # print (record)


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
    # print (type(RECs), RECs)

    if action == 'merge':
        merge(gv)


    fileScartate        = '{ROOT}/tmp/_Scartate.csv'.format(ROOT=gv.Prj.dataDIR)
    fileAnalizzate      = '{ROOT}/tmp/_Analizzate.csv'.format(ROOT=gv.Prj.dataDIR)
    fileValidSongs      = '{ROOT}/tmp/_ValidSongs.csv'.format(ROOT=gv.Prj.dataDIR)
    fileDuplicateSongs  = '{ROOT}/tmp/_DuplicateSongs.csv'.format(ROOT=gv.Prj.dataDIR)

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
        gv.Prj.writeFile(gv, fileScartate,   data=gv.songList.scartate)

        C.printYellow('writing file: {0}'.format(fileValidSongs), tab=4)
        gv.Prj.writeFile(gv, fileValidSongs,   data=gv.songList.validSongs)

        C.printYellow('writing file: {0}'.format(fileAnalizzate), tab=4)
        gv.Prj.writeFile(gv, fileAnalizzate, data=gv.songList.analizzate)


    if action == 'copySongs':
        gv.fEXECUTE      = gv.INPUT_PARAM.fEXECUTE
        RECs = gv.songList.validSongs[:]
        logger.info('trovate {0} canzoni da copiare'.format(len(RECs)))

        if gv.INPUT_PARAM.fCHECK_SOURCE:
            gv.Prj.checkSourceSongs(gv, RECs)

        else:
            choice = gv.Ln.getKeyboardInput("    Continuare per copiare le canzoni sulla destinazione?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
            if choice.lower() in ['x', 'no']:
                sys.exit()

            gv.Prj.copySongs(gv, RECs)
            print()
            C.printYellow('writing file: {0}'.format(fileDuplicateSongs), tab=4)
            print()
            gv.Prj.writeFile(gv, fileDuplicateSongs, data=gv.songList.duplicate)

            gv.copySong.printDict(gv)

    else:
        C.printRed('Action {0} not yet implemented...!'.format(action), tab=8)
        sys.exit()

    gv.Ln.Exit(0, "--------------- debugging exit ----------------", printStack=True, stackLevel=9, console=True)
    gv.Ln.Exit(0, "--------------- debugging exit ----------------", printStack=True, stackLevel=9, console=True)
