#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys

class BreakIt(Exception): pass

def songFilter(gv, RECs, fldNames):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()
    FLD     = gv.Ln.LnEnum(fldNames, myDict=gv.Ln.LnDict)
    WEIGHT   = gv.Ln.LnEnum(fldNames, myDict=gv.Ln.LnDict, weighted=True)


    includeAttr     = [token.strip() for token in gv.ini.MAIN.includeAttr.split(',')]
    excludeAttr     = [token.strip() for token in gv.ini.MAIN.excludeAttr.split(',')]
    excludeAuthor   = [token.strip() for token in gv.ini.MAIN.excludeAuthor.split(',')]
    excludeAlbums   = [token.strip() for token in gv.ini.MAIN.excludeAlbums.split(',')]
    excludeType     = [token.strip() for token in gv.ini.MAIN.excludeType.split(',')]

    maxSongs        = int(gv.ini.MAIN.maxSongs)
    numOutDirs      = int(gv.ini.MAIN.numOutDirs)
    maxBytesPerDir  = gv.ini.MAIN.maxBytesPerDir
    emptyField      = ['.', '_']


    gv.songList = gv.Ln.LnDict()
    gv.songList.analizzate = []
    gv.songList.scartate   = []
    gv.songList.validSongs = []


        # Visualizzazione pesi binari.
    reqScore = 0
    C.printCyan ('---  Attribute weight ----', tab=4)
    for item in WEIGHT:
        if item.startswith('_'): continue
        # print (item)
        # continue
        C.printCyan ("{ITEM:<14} -->  {WEIGHT:>8}".format(
                ITEM=item,
                WEIGHT=WEIGHT[item]),
                tab=4
            )

        reqScore  +=  WEIGHT[item]
    print ()
    C.printCyan ('requested Score: {0}'.format(reqScore), tab=4)


    print ()
    print ()
    C.printCyan ('---  Summary   ----', tab=4)
    C.printCyan ("num of output directory : {0}".format(numOutDirs), tab=4)

    comment = ' - no limit' if maxBytesPerDir == 0 else ''
    C.printCyan ("Max Byte per directory  : {0}{1}".format(maxBytesPerDir, comment), tab=4)

    comment = ' - no limit' if maxSongs == 0 else ''
    C.printCyan ("Max Songs to extract    : {0}{1}".format(maxSongs, comment), tab=4)

    print ()
    print ()


    validTotalSize      = 0
    scartateTotSize     = 0
    scartate            = 0
    analizzateTotSize   = 0
    toBeAanalysed       = 0
    toBeAanalysedSize   = 0
    nCols               = len(FLD)


    for index, song in enumerate(RECs):

        if maxSongs and index > maxSongs:
            C.printRedH('numero massimo di canzoni raggiunto', tab=4)
            break

             #  Se Analizzata non contiene flag skip
        if song[FLD.Analizzata] in emptyField: # deve avere un carattere diverso da '.' o '_'
            toBeAanalysed += 1
            toBeAanalysedSize += song[FLD.SongSize]
            continue
        else:
            gv.songList.analizzate.append(song)
            analizzateTotSize += song[FLD.SongSize]

            #  Se è da escludere skip
        if      song[FLD.Type]       in excludeType \
             or song[FLD.AuthorName] in excludeAuthor \
             or song[FLD.AlbumName]  in excludeAlbums:
            gv.songList.scartate.append(song)
            scartateTotSize += song[FLD.SongSize]
            scartate        += 1
            continue

        candidateSong = True

            # -------------------------------------------
            # - verifichiamo le colonne da escludere
            # --------------------------------------------
        for colName in excludeAttr:
            FIELD = FLD[colName]
            if not song[FIELD] in emptyField:
                candidateSong = False
                break

            # ---------------------------------------
            # - verifichiamo le colonne da includere
            # ---------------------------------------
        for colName in includeAttr:
            FIELD = FLD[colName]
            if song[FIELD] in emptyField:
                candidateSong = False
                break


        logger.debug('INCLUDE: {0} candidateSongs:{1}'.format(song[FIELD], candidateSong))

        # logger.debug('EXCLUDE: {0} isValidSong:{1}'.format(song[FIELD], isValidSong))


        if candidateSong:
            gv.songList.validSongs.append(song)
            validTotalSize   += song[FLD.SongSize]
        else:
            gv.songList.scartate.append(song)
            scartateTotSize += song[FLD.SongSize]
            scartate        += 1




    C.printYellow('Record TOTALI                    : {0:>6}'.format(len(RECs)), tab=4)

    C.printYellow('Canzoni con flag   ANALIZZATA    : {0:>6} - bytes: {1:,}'.format(len(gv.songList.analizzate), analizzateTotSize), tab=4)
    C.printYellow('Canzoni senza flag ANALIZZATA    : {0:>6} - bytes: {1:,}'.format(toBeAanalysed, toBeAanalysedSize), tab=4)
    C.printYellow('Canzoni TOTALI  (for checking)   : {0:>6} - (must be == Record Totali)'.format(len(gv.songList.analizzate) + toBeAanalysed), tab=4)

    print ()
    C.printCyan('Risultati dalla ricerca...', tab=4)
    C.printCyan('include cols: {0}'.format(includeAttr), tab=8)
    C.printCyan('exclude cols: {0}'.format(excludeAttr), tab=8)
    print ()
    C.printYellow('VALIDE dalla ricerca             : {0:>6} - bytes: {1:,}'.format(len(gv.songList.validSongs), validTotalSize), tab=4)
    C.printYellow('SCARTATE dalla ricerca           : {0:>6} - bytes: {1:,}'.format(scartate, scartateTotSize), tab=4)
    C.printYellow('Canzoni TOTALI  (for checking)   : {0:>6} - == flag ANALIZZATA'.format(scartate + len(gv.songList.validSongs)), tab=4)

    print()

        # msg = 'writing file: {0}'.format(fileScartate)
            # C.printYellow(msg, tab=4); logger.info(msg)
            # gv.Ln.writeTextFile(fileScartate,   data=gv.songList.scartate)

            # C.printYellow('writing file: {0}'.format(fileValidSongs), tab=4)
            # gv.Ln.writeTextFile(fileValidSongs,   data=gv.songList.validSongs)

            # C.printYellow('writing file: {0}'.format(fileAnalizzate), tab=4)
            # gv.Ln.writeTextFile(fileAnalizzate, data=gv.songList.analizzate)


        # - for DEBUG
    # for song in gv.songList.validSongs:
    #     fieldsToPrint = ['Loreto', 'Type', 'AuthorName', 'AlbumName', 'SongName']
    #     for colName in fieldsToPrint:
    #         FIELD = FLD[colName]
    #         print ('"{}" '.format(song[FIELD]), end='')
    #     print ()
    # sys.exit()

    return gv.songList.validSongs

