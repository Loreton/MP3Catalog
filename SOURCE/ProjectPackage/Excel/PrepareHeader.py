#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
# import sys
# import types

def prepareHeader(gv, ws):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy

    logger.info('entered - [called by:{0}]'.format(calledBy(1)))

    colNamesTuple = ws.rows[gv.MainVars.ExcelColNamesRow-1]
    for cell in colNamesTuple:
        val = cell.value
        print (val)


    '''
    # ---------------------------------------------------------
    # - Unisci i nomi delle colonne e verifichiamo
    # - che sono uguali a quelle del foglio excel
    # - La verifica viene fatta solo se viene passato rowValue
    # ---------------------------------------------------------
    totalCols = gv.CONFIG.NOMI_COLONNE_PRIMARIE[:]              # create a new copy of LIST
    totalCols.extend(gv.CONFIG.NOMI_COLONNE_ATTRIBUTI)


    # ###################################
    # - Controllo nomi colonne
    # ###################################
    if len(rowValue) != len(totalCols):
        Msg = "Il numero di colonne del foglio Excel non coincide con il numero di colonne del file di configurazione\n"
        Msg += "Si prega di correggere l'uno oppure l'altro valore\n"
        Msg += "Colonne foglio Excel:         [%d]\n" % (len(rowValue))
        Msg += "Colonne file Configurazione:  [%d]\n" % (len(totalCols))
        Prj.exit(gv, 2001, Msg)

    for i in range(len(rowValue)-1):
        valoreExcel = rowValue[i].encode('utf-8')
        logger.debug("[%s] - [%s]" % (valoreExcel, totalCols[i]))
        if rowValue[i].upper() != totalCols[i].upper():
            Msg = "Il nome colonna definito nel file.ini e' diverso da quanto trovato nel file Excel\n"
            Msg += "Si prega di correggere l'uno oppure l'altro valore\n"
            Msg += "Colonne interessate:    [%s] != [%s]" % (valoreExcel, totalCols[i])
            Prj.exit(gv, 2002, Msg)

    logger.info("Columns names check has been completed")


        # -------------------------------------------------------------------------------
        # - Crea una stringa con i nomi delle colonne rimpiazzando i BLANK con '_'
        # - ed ENUMera i nomi delle colonne
        # -------------------------------------------------------------------------------
    sTotalCols = ''
    for name in totalCols:
        sTotalCols += ' ' + name.replace(' ', '_')

    songAttribCols = ''
    for name in gv.CONFIG.NOMI_COLONNE_ATTRIBUTI:
        songAttribCols += ' ' + name.replace(' ', '_')


    logger.debug("%-20s = [%s]" % ('sTotalCols', sTotalCols.upper()))
    logger.debug("%-20s = [%s]" % ('songAttribCols', songAttribCols.upper()))

    gv.EXCEL.columnName     = LN.sys.enumerateClass(sTotalCols.upper())
    gv.EXCEL.songAttrName   = LN.sys.enumerateClass(songAttribCols.upper())
    gv.EXCEL.maxCols        = len(totalCols)                                        # Numero di colonne di una canzone
    gv.EXCEL.startAttrIndex = len(gv.CONFIG.NOMI_COLONNE_PRIMARIE)                  # indice di partenza degli attributi della canzone


    return gv.EXCEL.columnName

    '''
