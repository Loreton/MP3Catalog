#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys


    # print ('.......readFile.....')
def readFile(csvFile):
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    f = open(csvFile, "r", encoding="latin-1")
    for line in f:
        row.append(line.strip())
    f.close()
    return row


def writeFile(outFile, data=[]):
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    f = open(outFile, "w", encoding="latin-1")
    for line in data:
        f.write(';'.join(line))
        f.write('\n')
    f.close()




def extract(gv, csvFile):
    # RECs una lista di liste/canzoni
    rowList = readFile(csvFile)
    RECs = []
    for row in rowList:
        # print(row.strip('\n').strip())
        tokens = [token.strip() for token in row.split(';') if token]
        RECs.append(tokens) # se il primo è vuoto

    #  -------------------------------------------------
    # RECs[0] = Type
    #            Author Name
    #            Album Name
    #            Song Name
    #            Punteggio
    #            Analizzata
    #            Recomended
    #            Loreto
    #            Buona
    #            Soft
    #            Vivace
    #            Molto Viv
    #            Camera
    #            Car
    #            Lenta
    #            Country
    #            Strumentale
    #            Classica
    #            Lirica
    #            Live
    #            Discreta
    #            Undefined
    #            Avoid it
    #            Confusionaria
    #            Song Size
    #  -------------------------------------------------

        # Creiamo una enum con i nomi delle colonne
    col = gv.Ln.LnDict()
    for index, name in enumerate(RECs[0]):
        colName = name.replace(' ', '')
        col[colName] = index
        print (index, colName)
    nCols = index+1
    print(nCols)

        # ----------------------------------------------
        # - Preleviamo tutte le canzoni analizzate
        # ----------------------------------------------
    extracted  = []
    analizzate = []
    scartate   = []
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
    writeFile(gv.data.fileScartate,   data=scartate)

    print('writing file:', gv.data.fileEstratte)
    writeFile(gv.data.fileEstratte,   data=extracted)

    print('writing file:', gv.data.fileAnalizzate)
    writeFile(gv.data.fileAnalizzate, data=analizzate)




def type02(csvFile):
    row = []
    # with open(csvFile, encoding='ascii', errors="surrogateescape") as f:
    with open(csvFile, 'r', encoding='latin-1') as f:
        row = f.read()
    row = row.split('\n').strip()

    return row

################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def mainLite(gv):
    # gv.data = gv.Ln.LnDict(_dynamic=True)
    gv.data = gv.Ln.LnDict()

    csvFile                 = gv.Prj.dataDIR + '/MP3_Master_2015-08-10.csv'
    gv.data.fileScartate    = gv.Prj.dataDIR + '/_Scartate.csv'
    gv.data.fileAnalizzate  = gv.Prj.dataDIR + '/_Analizzate.csv'
    gv.data.fileEstratte    = gv.Prj.dataDIR + '/_Estratte.csv'

    extract(gv, csvFile)