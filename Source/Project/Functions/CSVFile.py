#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os
import ast

########################################################
# -
########################################################
def ReadCSVFile(gv, csvFile, requiredColNames):
    logger = gv.Ln.SetLogger(package=__name__)
    C      = gv.Ln.LnColor()

    FLD     = gv.Ln.LnEnum(requiredColNames, myDict=gv.Ln.LnDict)
        # ------------------------------------------------------------
        # - Lettura del file.csv
        # - La prima riga contiene il nome delle colonne
        # - Eliminiamo i blank nei nomi colonne
        # ------------------------------------------------------------
    csvRowList    = gv.Ln.readTextFile(csvFile)
    print ()
    print (csvRowList[0])
    print (csvRowList[1])
    print (FLD)
    print (FLD.Type)
    print ()

    colNames = [token.replace(' ', '').strip() for token in csvRowList[0].split(';')]


    if not colNames == requiredColNames:
        C.printYellowH('i nomi delle colonne non coincidono', tab=4)
        C.printYellowH('file     : {0}'.format(colNames), tab=4)
        C.printYellowH('expected : {0}'.format(requiredColNames), tab=4)
        gv.Ln.Exit(1, 'I nomi delle colonne non coincidono')


        # ===========================================
        # - RECs creazione di una lista di liste/canzoni [[],[],..]
        # ===========================================
    RECs = []
    for row in csvRowList:
        column = [token.strip() for token in row.split(';') if isinstance(token, str)]
        if len(column[FLD.Type].strip()) > 3:
            RECs.append(column)


        # ===========================================
        #  - Creazione del dictionary del CSV
        # ===========================================
    gv.song.dict = gv.Ln.LnDict()

    # gv.song.PrintTree(fEXIT=True)
    for song in RECs[1:]:   # skip line 0 with fields name
        ptr = gv.song.dict
        startAttributeCols = FLD.SongName+1

            # -creazione dictionary per type.author.album.songName
        for field in song[:startAttributeCols]:
            if not field in ptr:
                ptr[field] = gv.Ln.LnDict()
            ptr = ptr[field]

            # su ogni canzone mettiamo i vari attributi
        for index, value in enumerate(song[startAttributeCols:]):
            attrName  = requiredColNames[index]
            ptr[attrName] = value


    logger.debug('FOUND {0} records... in the required range {1}'.format(len(RECs), gv.ini.EXCEL.RangeToProcess))

    if gv.fDEBUG: gv.song.dict.PrintTree()
    return RECs

    gv.Ln.Exit(0, "--------------- debugging exit ----------------", printStack=True, stackLevel=9, console=True)




#######################################################
# #
#######################################################
def WriteCSVFile(gv, csvFile, data=[]):
    logger = gv.Ln.SetLogger(package=__name__)
    logger.debug('writing file:             {0}'.format(csvFile))
    logger.debug('number of lines to write: {0}'.format(len(data)))

        # -----------------------------------------------------------------------
        # - Per ogni canzone prendiamo gli attributi e salviamola.
        # -----------------------------------------------------------------------
    f = open(csvFile, "w", encoding='utf-8', newline='\n')
    NL = '\n'
    for line in data:
        if isinstance(line, list):
            # converte all items to string perché...
            # ...potrebbe dare errore se qualche item non è stringa
            lineStr = [str(item) for item in line]
            f.write(';'.join(lineStr))
        else:
            f.write(line)
        f.write(NL)
    f.close()

