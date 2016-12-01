#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os
import ast


##############################################################
# - 1. Leggiamo la rootSourceDir
# - 2. Inseriamo ogni file nel dictionary
##############################################################
def Merge(gv, csvFile, csvFormat):
    logger  = gv.Ln.SetLogger(package=__name__)
    C = gv.Ln.LnColor()

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
    # gv.song.dict.PrintTree(fEXIT=True)

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
    mergedLIST = [gv.song.colsName] # nomi delle colonne come prima riga
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
        songAttr = ptrSong.GetValue(fPRINT=False)

        # -------------------------------------
        # - Inseriamo la canzone nella lista
        # - che salveremo come merged CSV
        # -------------------------------------
        newSong = songQualifiers[:]
        for attributeName, val in songAttr.items():
            newSong.append(val)

        mergedLIST.append(newSong)

    # -----------------------------------------------------------------------
    # - Salviamo il tutto in formato csv
    # -----------------------------------------------------------------------
    # for line in mergedLIST: print (line)
    gv.Prj.WriteCSVFile(gv, csvFile, mergedLIST, csvFormat)
    print ()
    C.printYellowH('file: {0} has been saved.'.format(csvFile), tab=4)
    # gv.song.PrintTree(MaxLevel=2)


