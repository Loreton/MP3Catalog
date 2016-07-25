#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys

class BreakIt(Exception): pass

def songFilter(gv, RECs):
    # ricerca della riga con i nomi
    for index, song in enumerate(RECs):
        print (len(song), song)
        if len(song) > 1 and song[0] == 'Type':
            col = gv.Prj.enumCols(gv, RECs[index])
            nCols = len(col)
            RECs = RECs[index:]
            break


        # ----------------------------------------------
        # - Preleviamo tutte le canzoni analizzate
        # ----------------------------------------------
    extracted  = [RECs[0]]  # init con il nome delle colonne
    analizzate = [RECs[0]]  # init con il nome delle colonne
    scartate   = [RECs[0]]  # init con il nome delle colonne
    TotSize     = 0
    excludeType     = ['Bambini', 'Natale', 'Popolari', 'Themes']
    excludeAuthor   = ['Bambini', 'Chitarra', 'Classica']

    for index, song in enumerate(RECs[1:]):
        if len(song) != nCols: continue
        # if index > 10: break
        if not song[col.Analizzata] == '.':
            if song[col.Type]       in excludeType:     continue
            if song[col.AuthorName] in excludeAuthor:   continue
            analizzate.append(song)
            if song[col.Recomended] + song[col.Loreto] + song[col.Soft] != '...':
                extracted.append(song)
                size = int(song[col.SongSize].replace('bytes', '').replace('.', ''))
                TotSize += int(size)

        else:
            scartate.append(song)

    print('TATALI    :', len(RECs))
    print()
    print('ANALIZZATE:', len(scartate))
    print('VALIDE    :', len(analizzate))
    print('SCARTATE  :', len(scartate))
    print('ESTRATTE  :', len(extracted))
    print('Bytes     : {0:,}'.format(TotSize))
    print()

    print('writing file:', gv.data.fileScartate)
    gv.Prj.writeFile(gv.data.fileScartate,   data=scartate)

    print('writing file:', gv.data.fileEstratte)
    gv.Prj.writeFile(gv.data.fileEstratte,   data=extracted)

    print('writing file:', gv.data.fileAnalizzate)
    gv.Prj.writeFile(gv.data.fileAnalizzate, data=analizzate)




