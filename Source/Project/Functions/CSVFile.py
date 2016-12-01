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
def ReadCSVFile(gv, csvFile, csvFormat):
    logger = gv.Ln.SetLogger(package=__name__)
    C      = gv.Ln.LnColor()


        # ------------------------------------------------------------
        # - Lettura del file.csv
        # - La prima riga contiene il nome delle colonne
        # - Eliminiamo i blank nei nomi colonne
        # ------------------------------------------------------------
    csvRowList      = gv.Ln.readTextFile(csvFile)
    csvRowList[0]   = csvRowList[0].replace(' ', '')   # eliminiamo i BLANK nei nomi colonne

    if csvFormat == 'listtype':
        try:
            colNames = ast.literal_eval(csvRowList[0])    # converte una stringa formato LIST in una LIST
        except Exception as why:
            msg = [str(why), csvRowList[0]]
            gv.Ln.Exit(2, msg, printStack=True)
    else:
        # colNames = [token.strip() for token in csvRowList[0].split(';') if token]
        colNames = [token.strip() for token in csvRowList[0].split(';')]

    excelColsName    = ';'.join(colNames)
    requiredColsName = ';'.join(gv.song.colsName)
    logger.debug('excel  columns name: {0}'.format(excelColsName))
    logger.debug('config columns name: {0}'.format(requiredColsName))

    if not excelColsName == requiredColsName:
        C.printYellowH('i nomi delle colonne non coincidono', tab=4)
        C.printYellowH('file     : {0}'.format(csvRowList[0]), tab=4)
        C.printYellowH('expected : {0}'.format(requiredColsName), tab=4)
        C.printYellowH('found    : {0}'.format(excelColsName), tab=4)
        gv.Ln.Exit(1, 'I nomi delle colonne non coincidono')


        # ===========================================
        # - RECs creazione di una lista di liste/canzoni [[],[],..]
        # ===========================================
    RECs = []
    if csvFormat == 'listtype':
        for row in csvRowList:
            try:
                column0 = ast.literal_eval(row)    # converte una stringa formato LIST in una LIST
                column = []
                for token in column0:
                    if isinstance(token, str):
                        column.append(token.strip())
                    else:
                        column.append(token)

                if len(column[gv.song.field.Type].strip()) > 3:
                    RECs.append(column)
            except Exception as why:
                gv.Ln.Exit(2, str(why), fullStack=True)
    else:
        for row in csvRowList:
            column = [token.strip() for token in row.split(';') if isinstance(token, str)]
            if len(column[gv.song.field.Type].strip()) > 3:
                RECs.append(column)


    gv.song.list = RECs

        # ===========================================
        #  - Creazione del dictionary del CSV
        # ===========================================
    gv.song.dict = gv.Ln.LnDict()
    for song in RECs[1:]:   # skip line 0 with fields name
        ptr = gv.song.dict
        startAttributeCols = gv.song.field.SongName+1

            # -creazione dictionary per type.author.album.songName
        for field in song[:startAttributeCols]:
            if not field in ptr:
                ptr[field] = gv.Ln.LnDict()
            ptr = ptr[field]

            # su ogni canzone mettiamo i vari attributi
        for index, value in enumerate(song[startAttributeCols:]):
            attrName  = gv.song.attributeCols[index]
            ptr[attrName] = value


    logger.debug('FOUND {0} records... in the required range {1}'.format(len(RECs), gv.ini.EXCEL.RangeToProcess))

    if gv.fDEBUG: gv.song.dict.PrintTree()
    return RECs
    gv.Ln.Exit(0, "--------------- debugging exit ----------------", printStack=True, stackLevel=9, console=True)




#######################################################
# #
#######################################################
def WriteCSVFile(gv, csvFile, data=[], csvFormat=''):
    logger = gv.Ln.SetLogger(package=__name__)
    logger.debug('writing file:             {0}'.format(csvFile))
    logger.debug('number of lines to write: {0}'.format(len(data)))

        # -----------------------------------------------------------------------
        # - Per ogni canzone prendiamo gli attributi e salviamola.
        # -----------------------------------------------------------------------
    f = open(csvFile, "w", encoding='utf-8')
    for line in data:
        if isinstance(line, list):
            # converte all items to string perché...
            # ...potrebbe dare errore se qualche item non è stringa
            lineStr = [str(item) for item in line]
            f.write(';'.join(lineStr))
        else:
            f.write(line)
        f.write('\n')
    f.close()

