#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os
import types

# =======================================================================
# ReadExcelCatalog()
# =======================================================================
def readCatalog(gv, MP3Dict):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered   - [called by:{0}]'.format(calledBy(1)))


    fDEBUG = False
    # excelFileName   = gv.MainVars.excelInputFile

        # -------------------------
        # - Lettura del WorkBook
        # -------------------------
    wb = gv.LN.excel.read(gv, gv.MainVars.excelInputFile, keep_vba=True)
    logger.info('Analisi del foglio: {0}'.format(gv.MainVars.sheetName))

    # range.rowLow
    # range.rowHigh
    # range.colLow
    # range.colHigh

        # -------------------------------------------------------
        # - Acquisizione del folgio richiesto in formato CSV
        # -------------------------------------------------------
    if not gv.MainVars.sheetName in wb.get_sheet_names():
        gv.LN.exit(gv, 1001, "Il nome del foglio richiesto {0} non e' presente nel file {1}".format(gv.MainVars.sheetName, gv.MainVars.excelInputFile))
    outFname = 'd:/tmp/excelToCSV_{0}.csv'.format(gv.MainVars.sheetName)
    gv.ExcelCSV = gv.LN.excel.exportToCSV(gv, wb, gv.MainVars.sheetName, outFname=outFname, maxrows=gv.MainVars.MaxRowsToRead, fPRINT=False)
    # for line in gv.ExcelCSV: print (line)
    return  gv.ExcelCSV

    choice=gv.LN.sys.getKeyboardInput(gv, "Uscita Temporanea", validKeys="X", exitKey='XQ')



    ws = wb.get_sheet_by_name(gv.MainVars.sheetName)

    prevAuth = '...'

    # gv.LN.dict.printDictionaryTree(gv, gv.MainVars, header="MainVars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2, MaxDeepLevel=99)

    # startExcelCol = gv.MainVars.ExcelStartCol   # Colonna di partenza dati

    # fullRange = openpyxl.cell.get_column_letter(1) + str(1) + ':' + openpyxl.cell.get_column_letter(nCols) + str(nRows)

    fld = gv.Prj.excel.prepareHeader(gv, gv.ExcelCSV)
    choice=gv.LN.sys.getKeyboardInput(gv, "Uscita Temporanea", validKeys="X", exitKey='XQ')



    colNames = ws.rows[gv.MainVars.ExcelColNamesRow-1]

    print ('creating /tmp/sample.xlsm file')
    wb.save("/tmp/sample.xlsm")


    '''
    for row in range(sheet.nrows):
        rowValue = LN.excel.getRow(gv, sheet, row, wb, wantTupleDate=False)

        dummyCols = ord(gv.MainVars.ExcelStartCol) - ord('A')                # Eliminiamo le colonne vuote da A fino allo startExcelCol
        while dummyCols:
            del rowValue[0]
            dummyCols -= 1


            logger.info('working on row - {0}'.format(rowValue[:5]) )
                # ------------------------------------------
                # - calcoliamo i nomi delle colonne
                # ------------------------------------------
                    # - Verifica che i campi siano corretti ed enumera gli stessi
            if row == gv.CONFIG.COLUMNS_NAME_ROW:
                fld = Prj.excel.prepareHeader(gv, rowValue)
                # LN.dict.printDictionaryTree(gv, gv.EXCEL, header="Column Names [{0}]".formatcalledBy(0), retCols='LTV', lTAB=' '*4, console=True)
                continue

            elif row<gv.CONFIG.FIRST_SONG_ROW:
                continue

            elif row>gv.CONFIG.LAST_SONG_ROW:
                logger.warning("."*60)
                logger.warning("MAX_ROWs has been reached.......")
                logger.warning("."*60)
                break

            if row%100 == 0: print "%6d/%6d [LimitedTo:%d] rows has been processed".format(row, sheet.nrows, gv.CONFIG.LAST_SONG_ROW)
            nCols     = len(rowValue)

            if nCols > gv.EXCEL.maxCols:               # ultima colonna valida
                rowValue = rowValue[:gv.EXCEL.maxCols]
            elif nCols < gv.EXCEL.maxCols:               # NON PREVISTO
                print "riga numero:", row
                print rowValue
                Prj.exit(gv, 11, "Il numero di colonne del file non puo' essere inferiore alle colonne previste. [nCols:%d]<[fld.SONG_SIZE:%d]".format(nCols, fld.SONG_SIZE) )

                # Per essere certi di non avere sorprese
            rowValue[fld.TYPE]           = rowValue[fld.TYPE].strip()
            rowValue[fld.AUTHOR_NAME]    = rowValue[fld.AUTHOR_NAME].strip()
            rowValue[fld.ALBUM_NAME]     = rowValue[fld.ALBUM_NAME].strip()
            rowValue[fld.SONG_NAME]      = rowValue[fld.SONG_NAME].strip()

            songName    = rowValue[fld.SONG_NAME]

                 # riga vuota
            if rowValue[fld.TYPE] == '' or rowValue[fld.TYPE] == '#':
                logger.debug("SKIPPING - empty or commented(#) row: [{0}]".format(rowValue))
                continue

            if fDEBUG: print "^^^^^ {0}/{0}/{0}/{0}".format(rowValue[fld.TYPE], rowValue[fld.AUTHOR_NAME], rowValue[fld.ALBUM_NAME], songName), type(songName)

            if type(songName) == types.IntType or len(songName) < 2:
                logger.warning("SKIPPING - invalid songName: [{0}]".format(songName))
                continue

            if songName.find('_NO_MATCH_ON_DISK_') > 0:
                logger.warning("SKIPPING - _NO_MATCH_ON_DISK_ song: [{0}]".format(songName))
                continue

            if prevAuth != rowValue[fld.AUTHOR_NAME]:
                prevAuth = rowValue[fld.AUTHOR_NAME]
                logger.console("reading author: [{0}:{0}]".format(rowValue[fld.TYPE], rowValue[fld.AUTHOR_NAME]) )

            rowValue = Prj.fmt.prepareRow(gv, rowValue)

            if len(songName) >= 2 and rowValue[fld.TYPE] != 'Titles':
                Prj.mp3.insertSong(gv, MP3Dict, rowValue)
                if rowValue[fld.TYPE] == 'UNKNOWN':
                    choice=LN.sys.getKeyboardInput(gv, "Vuoi continuare???", validKeys="Y", exitKey='XQ')



    # ###################################
    # choice=LN.sys.getKeyboardInput(gv, "******* STOP Temporaneo *******", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
    # ###################################


    logger.debug('exiting - [called by:{0}]'.format(calledBy(1)))

    '''

