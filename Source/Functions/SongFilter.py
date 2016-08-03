#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys

class BreakIt(Exception): pass

def songFilter(gv, RECs):
    logger = gv.Ln.setLogger(package=__name__, CONSOLE=gv.INPUT_PARAM.LogCONSOLE)
    C = gv.Ln.Colors()
    sf = gv.Ln.LnDict()
    col = gv.Prj.enumCols(gv, gv.Prj.songColumName)
    '''
    # ricerca della riga con i nomi
    for index, song in enumerate(RECs):
        # print (len(song), song)
        if len(song) > 1 and song[0] == 'Type':
            col = gv.Prj.enumCols(gv, RECs[index])
            nCols = len(col)
            RECs = RECs[index:]
            break
    print (col)
    '''
        # ----------------------------------------------
        # - Preleviamo tutte le canzoni analizzate
        # - Analizzata;Recomended;Loreto;Buona;Soft;Vivace;Molto Viv;Camera;Car;Lenta;Count
        # ----------------------------------------------
    sf.validSongs  = [gv.Prj.songColumName]  # init con il nome delle colonne
    sf.analizzate  = [gv.Prj.songColumName]  # init con il nome delle colonne
    sf.scartate    = [gv.Prj.songColumName]  # init con il nome delle colonne


    # sf.excludeType     = ['Bambini', 'Natale', 'Popolari', 'Themes']
    # sf.excludeAuthor   = ['Bambini', 'Chitarra', 'Classica']

        # Assegnamo un peso binario ad ogni colonna che ci interessa filtrare.
    colVal = gv.Prj.enumColsBase2(gv, gv.Prj.songColumName)

    # visualizzazione pesi e calcolo dello score
    reqScore = 0
    for item in gv.Prj.songColumName:
        C.printCyan ("{ITEM:<10}   {WEIGHT:>6} - {BOOL}".format(ITEM=item, BOOL=gv.INPUT_PARAM[item],  WEIGHT=colVal[item]), tab=4)
        reqScore  +=  gv.INPUT_PARAM[item]   * colVal[item]

    print ()
    C.printCyan ("num of output directory: {0}".format(gv.INPUT_PARAM.numDirs), tab=4)
    comment = ' - no limit' if gv.INPUT_PARAM.maxBytes == 0 else ''
    C.printCyan ("Max Byte per directory:  {0}{1}".format(gv.INPUT_PARAM.maxBytes, comment), tab=4)
    C.printCyan ("Max Songs to extract:    {0}".format(gv.INPUT_PARAM.maxSongs), tab=4)
    print ()
    C.printCyan ('requested Score: {0}'.format(reqScore), tab=4)
    print ()

    sf.col         = col
    sf.colVal      = colVal
    sf.reqScore    = reqScore

    validTotSize        = 0
    scartateTotSize     = 0
    analizzateTotSize   = 0

    excludeCol  = gv.INPUT_PARAM.exclude
    includeCol  = gv.INPUT_PARAM.include

    for index, song in enumerate(RECs):
        if len(song) != nCols:
            sf.scartate.append(song)
            continue

        if gv.INPUT_PARAM.maxSongs and index > gv.INPUT_PARAM.maxSongs:
            print ('numero massimo di canzoni raggiunto')
            break

        size = int(song[col.SongSize].replace('bytes', '').replace('.', ''))

        # verifichiamo le colonne da escludere.
        for colName in gv.Prj.songColumName:
            if colName.lower() in (x.lower() for x in excludeCol):

            if song[colName]
            if name.lower() in (x.lower() for x in InputPARAM.flags):

        if not song[col['Analysed']] == '.':
            analizzateTotSize += int(size)
            sf.analizzate.append(song)

        if isValidSong(gv, sf, song):
            sf.validSongs.append(song)
            validTotSize += int(size)
        else:
            sf.scartate.append(song)
            scartateTotSize += int(size)




    C.printYellow('Canzoni TOTALI   : {0}'.format(len(RECs)), tab=4)
    print()
    C.printYellow('ANALIZZATE       : {0} - bytes: {1:,}'.format(len(sf.analizzate)-1, analizzateTotSize), tab=4)
    C.printYellow('VALIDE           : {0} - bytes: {1:,}'.format(len(sf.validSongs)-1, validTotSize), tab=4)
    C.printYellow('SCARTATE         : {0} - bytes: {1:,}'.format(len(sf.scartate)-1, scartateTotSize), tab=4)

    print()

    return sf


def isValidSong(gv, sf, song):
    songScore = 0
    col     = sf.col
    colVal  = sf.colVal

    if song[col.Type]       in sf.excludeType:     return False
    if song[col.AuthorName] in sf.excludeAuthor:   return False

    if gv.INPUT_PARAM.Analizzata and not song[col.Analizzata]  == '.':  songScore += colVal.Analizzata
    if gv.INPUT_PARAM.Recomended and not song[col.Recomended]  == '.':  songScore += colVal.Recomended
    if gv.INPUT_PARAM.Loreto     and not song[col.Loreto]      == '.':  songScore += colVal.Loreto
    if gv.INPUT_PARAM.Buona      and not song[col.Buona]       == '.':  songScore += colVal.Buona
    if gv.INPUT_PARAM.Soft       and not song[col.Soft]        == '.':  songScore += colVal.Soft
    if gv.INPUT_PARAM.Vivace     and not song[col.Vivace]      == '.':  songScore += colVal.Vivace
    if gv.INPUT_PARAM.MoltoViv   and not song[col.MoltoViv]    == '.':  songScore += colVal.MoltoViv
    if gv.INPUT_PARAM.Camera     and not song[col.Camera]      == '.':  songScore += colVal.Camera
    if gv.INPUT_PARAM.Car        and not song[col.Car]         == '.':  songScore += colVal.Car


    if songScore == sf.reqScore:
        return True
    else:
        # print (sf.reqScore, songScore, song[:col.Car])
        return False