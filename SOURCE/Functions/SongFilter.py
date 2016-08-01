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
    # ricerca della riga con i nomi
    for index, song in enumerate(RECs):
        # print (len(song), song)
        if len(song) > 1 and song[0] == 'Type':
            col = gv.Prj.enumCols(gv, RECs[index])
            nCols = len(col)
            RECs = RECs[index:]
            break


        # ----------------------------------------------
        # - Preleviamo tutte le canzoni analizzate
        # Analizzata;Recomended;Loreto;Buona;Soft;Vivace;Molto Viv;Camera;Car;Lenta;Count
        # ----------------------------------------------
    sf.validSongs  = [RECs[0]]  # init con il nome delle colonne
    sf.analizzate = [RECs[0]]  # init con il nome delle colonne
    sf.scartate   = [RECs[0]]  # init con il nome delle colonne

    validTotSize     = 0
    scartateTotSize     = 0
    analizzateTotSize     = 0

    sf.excludeType     = ['Bambini', 'Natale', 'Popolari', 'Themes']
    sf.excludeAuthor   = ['Bambini', 'Chitarra', 'Classica']

        # Assegnamo un valore binario ad ogni colonna che ci interessa filtrare.
    colVal = gv.Prj.enumColsKeyVal(gv, ['Analizzata   = 1',
                                        'Recomended = 2',
                                        'Loreto     = 4',
                                        'Buona      = 8',
                                        'Soft       = 16',
                                        'Vivace     = 32',
                                        'MoltoViv    = 64',
                                        'Camera     = 128',
                                        'Car        = 256',
                                        ]
                                    )



    C.printCyan ("Analizzata   {1:>6} - {0}".format(gv.INPUT_PARAM.Analizzata,colVal.Analizzata), tab=4)
    C.printCyan ("Recomended   {1:>6} - {0}".format(gv.INPUT_PARAM.Recomended,  colVal.Recomended), tab=4)
    C.printCyan ("Loreto       {1:>6} - {0}".format(gv.INPUT_PARAM.Loreto,      colVal.Loreto), tab=4)
    C.printCyan ("Buona        {1:>6} - {0}".format(gv.INPUT_PARAM.Buona,       colVal.Buona), tab=4)
    C.printCyan ("Soft         {1:>6} - {0}".format(gv.INPUT_PARAM.Soft,        colVal.Soft), tab=4)
    C.printCyan ("Vivace       {1:>6} - {0}".format(gv.INPUT_PARAM.Vivace,      colVal.Vivace), tab=4)
    C.printCyan ("MoltoViv     {1:>6} - {0}".format(gv.INPUT_PARAM.MoltoViv,     colVal.MoltoViv), tab=4)
    C.printCyan ("Camera       {1:>6} - {0}".format(gv.INPUT_PARAM.Camera,      colVal.Camera), tab=4)
    C.printCyan ("Car          {1:>6} - {0}".format(gv.INPUT_PARAM.Car,         colVal.Car), tab=4)
    print ()
    C.printCyan ("num of output directory: {0}".format(gv.INPUT_PARAM.numDirs), tab=4)
    comment = ' - no limit' if gv.INPUT_PARAM.maxBytes == 0 else ''
    C.printCyan ("Max Byte per directory:  {0}{1}".format(gv.INPUT_PARAM.maxBytes, comment), tab=4)
    C.printCyan ("Max Songs to extract:    {0}".format(gv.INPUT_PARAM.maxSongs), tab=4)

    reqScore =      gv.INPUT_PARAM.Analizzata   * colVal.Analizzata +\
                    gv.INPUT_PARAM.Recomended   * colVal.Recomended +\
                    gv.INPUT_PARAM.Loreto       * colVal.Loreto +\
                    gv.INPUT_PARAM.Buona        * colVal.Buona +\
                    gv.INPUT_PARAM.Soft         * colVal.Soft +\
                    gv.INPUT_PARAM.Vivace       * colVal.Vivace +\
                    gv.INPUT_PARAM.MoltoViv     * colVal.MoltoViv +\
                    gv.INPUT_PARAM.Camera       * colVal.Camera +\
                    gv.INPUT_PARAM.Car          * colVal.Car

    print ()
    C.printCyan ('requested Score: {0}'.format(reqScore), tab=4)
    print ()

    sf.col         = col
    sf.colVal      = colVal
    sf.reqScore    = reqScore

    for index, song in enumerate(RECs[1:]):
        if len(song) != nCols:
            sf.scartate.append(song)
            continue

        if gv.INPUT_PARAM.maxSongs and index > gv.INPUT_PARAM.maxSongs:
            print ('numero massimo di canzoni raggiunto')
            break

        size = int(song[col.SongSize].replace('bytes', '').replace('.', ''))

        if not song[col.Analizzata] == '.':
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