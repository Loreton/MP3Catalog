#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys

class BreakIt(Exception): pass

def songFilter(gv, RECs):
    logger = gv.Ln.setLogger(gv, package=__name__)
    C = gv.Ln.Colors()
    col = gv.Prj.enumCols(gv, gv.Prj.songColumsName)





        # Assegnamo un peso binario ad ogni colonna che ci interessa filtrare.
    # colVal = gv.Prj.enumColsBase2(gv, gv.Prj.songAttributes)
    colVal = gv.Prj.enumColsBase2(gv, gv.INPUT_PARAM.include)
    reqScore = 0
    for item in colVal:
        C.printCyan ("{ITEM:<14} -->  {WEIGHT:>6}".format(
                ITEM=item,
                WEIGHT=colVal[item]),
                tab=4
            )

        reqScore  +=  colVal[item]

    print ()
    C.printCyan ("num of output directory: {0}".format(gv.INPUT_PARAM.numDirs), tab=4)
    comment = ' - no limit' if gv.INPUT_PARAM.maxBytes == 0 else ''
    C.printCyan ("Max Byte per directory:  {0}{1}".format(gv.INPUT_PARAM.maxBytes, comment), tab=4)
    comment = ' - no limit' if gv.INPUT_PARAM.maxSongs == 0 else ''
    C.printCyan ("Max Songs to extract:    {0}{1}".format(gv.INPUT_PARAM.maxSongs, comment), tab=4)
    print ()
    C.printCyan ('requested Score: {0}'.format(reqScore), tab=4)
    print ()

    # gv.songList.col         = col
    # gv.songList.colVal      = colVal
    # gv.songList.reqScore    = reqScore

    validTotSize        = 0
    scartateTotSize     = 0
    scartate            = 0
    analizzateTotSize   = 0
    toBeAanalysed       = 0
    toBeAanalysedSize   = 0
    invalidLines   = 0
    nCols = len(gv.Prj.songColumsName)

    excludeType     = ['Bambini', 'Natale', 'Popolari', 'Themes']
    excludeAuthor   = ['xxx', 'cccc', 'xxx']
    includeCol  = ['Analizzata']
    includeCol.extend(gv.INPUT_PARAM.include)
    excludeCol  = gv.INPUT_PARAM.exclude

    for index, song in enumerate(RECs):
        if len(song) != nCols:
            invalidLines += 1
            continue

        if gv.INPUT_PARAM.maxSongs and index > gv.INPUT_PARAM.maxSongs:
            print ('numero massimo di canzoni raggiunto')
            break


        size = int(song[col.SongSize].replace('bytes', '').replace('.', ''))

        # se la canzone NON ha il flag 'Analizzata'... ignorala
        if song[col['Analizzata']] == '.':  # deve avere un carattere diverso da '.'
            toBeAanalysed += 1
            toBeAanalysedSize += size
            continue
        else:
            gv.songList.analizzate.append(song)
            analizzateTotSize += size

        if song[col.Type] in excludeType or song[col.AuthorName] in excludeAuthor:
            gv.songList.scartate.append(song)
            scartateTotSize += size
            scartate        += 1
            continue


        isValidSong = True


        TRACE_SONG = False
        if TRACE_SONG:
            if song[col.SongName] == 'Conforto alla vita':
                print (song)
            else:
                TRACE_SONG = False   #azzera flag se non è la canzone che vogliamo verificare

        for colName in includeCol:
            if TRACE_SONG: print ('INCLUDE:', colName, song[col[colName]])
            if song[col[colName]] == '.':
                isValidSong = False
                break

        if TRACE_SONG: print('INCLUDE: isValidSong', isValidSong)

            # verifichiamo le colonne da escludere.
        for colName in excludeCol:
            if TRACE_SONG: print ('EXCLUDE:', colName, song[col[colName]])
            if song[col[colName]] != '.':
                isValidSong = False

        if TRACE_SONG: print('EXCLUDE: isValidSong', isValidSong)

        if isValidSong:
            gv.songList.validSongs.append(song)
            validTotSize += int(size)
        else:
            gv.songList.scartate.append(song)
            scartateTotSize += size
            scartate        += 1




    C.printYellow('Record TOTALI                    : {0:>6}'.format(len(RECs)), tab=4)
    C.printYellow('Invalid Lines                    : {0:>6}'.format(invalidLines), tab=4)

    C.printYellow('Canzoni con flag   ANALIZZATA    : {0:>6} - bytes: {1:,}'.format(len(gv.songList.analizzate)-1, analizzateTotSize), tab=4)
    C.printYellow('Canzoni senza flag ANALIZZATA    : {0:>6} - bytes: {1:,}'.format(toBeAanalysed, toBeAanalysedSize), tab=4)
    C.printYellow('Canzoni TOTALI                   : {0:>6}'.format(len(RECs) - invalidLines), tab=4)

    print ()
    C.printCyan('Risultati dalla ricerca...', tab=4)
    C.printCyan('include cols: {0}'.format(includeCol), tab=8)
    C.printCyan('exclude cols: {0}'.format(excludeCol), tab=8)
    print ()
    C.printYellow('risultate VALIDE dalla ricerca   : {0:>6} - bytes: {1:,}'.format(len(gv.songList.validSongs)-1, validTotSize), tab=4)
    C.printYellow('tisultate SCARTATE dalla ricerca : {0:>6} - bytes: {1:,}'.format(len(gv.songList.scartate)-1, scartateTotSize), tab=4)

    '''
    '''
    print()

    return


