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
def ReadCSVFile(gv):
    C         = gv.Ln.LnColor()

        # - leggiamo tipo di csv da usare
    csvFormat = gv.ini.MAIN.csvFormat

        # ========================================
        # - Build Excel FileName
        # ========================================
    xlsFile = os.path.abspath(os.path.join(gv.Prj.dataDIR, gv.INPUT_PARAM.excelFile))
    csvFile = xlsFile.rsplit('.', -1)[0] + '.csv'


        # - Se il csv è più vecchio dell'xls facciamo l'export
    if gv.Ln.Fmtime(xlsFile) > gv.Ln.Fmtime(csvFile):
        mydata  = gv.Ln.Excel(xlsFile)
        mydata.exportCSV('Catalog', csvType=csvFormat, outFname=csvFile, rangeString="B2:Z17", colNames=4, fPRINT=True)

        # ------------------------------------------------------------
        # - Lettura del file.csv
        # - La prima riga conriene il nome delle colonne
        # - Eliminiamo i blank nei nomi colonne
        # ------------------------------------------------------------
    csvRowList      = gv.Prj.readFile(gv, csvFile)
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

    if not ';'.join(colNames) == ';'.join(gv.song.songCols):
        C.printYellowH('i nomi delle colonne non coincidono', tab=4)
        C.printYellowH('file     : {0}'.format(csvRowList[0]), tab=4)
        C.printYellowH('required : {0}'.format(';'.join(gv.song.songCols)), tab=4)
        gv.Ln.Exit(1, 'I nomi delle colonne non coincidono')


        # ===========================================
        # RECs creazione di una lista di liste/canzoni [[],[],..]
        # ===========================================
    RECs = []
    if csvFormat == 'listtype':
        for row in csvRowList:
            try:
                column = ast.literal_eval(row)    # converte una stringa formato LIST in una LIST
                if len(column[gv.song.field.Type].strip()) > 3:
                    RECs.append(column)
            except Exception as why:
                gv.Ln.Exit(2, str(why), fullStack=True)
    else:
        for row in csvRowList:
            column = [token.strip() for token in row.split(';')]
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
        # startAttributeCols = len(gv.song.primaryCols)

            # -creazione dictionary per type.author.album.songName
        for field in song[:startAttributeCols]:
            if not field in ptr:
                ptr[field] = gv.Ln.LnDict()
            ptr = ptr[field]

            # su ogni canzone mettiamo i vari attributi
        for index, value in enumerate(song[startAttributeCols:]):
            attrName  = gv.song.attributeCols[index]
            ptr[attrName] = value



    if gv.fDEBUG: gv.song.dict.printDict(gv)

