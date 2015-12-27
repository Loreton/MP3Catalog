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
    excelFileName = gv.MainVars.excelInputFile


    '''

    if not os.path.isfile(excelFileName):
        gv.Ln.exit(gv, 10, "File doesn't exists: [{0}]".format(excelFileName))

    logger.info("Reading excelFileName: [{0}]." .format(excelFileName))
    prevAuth = '...'
    '''
        # Ritorna il WorkBook
    wb = gv.LN.excel.open(gv, excelFileName)
    gv.LN.dict.printDictionaryTree(gv, gv.MainVars, header="MainVars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2, MaxDeepLevel=99)

    '''

        # Esaminiamo tutti gli sheet (in teroia è solo il primo)
    for sheet in wb.sheets():
        gv.EXCEL.sheetName = sheet.name
        logger.info('Analizzo sheetName: {0}'.format(sheet.name))
        startExcelCol = gv.CONFIG.START_EXCEL_COLUMN.upper()   # Colonna di partenza dati

        for row in range(sheet.nrows):
            rowValue = LN.excel.getRow(gv, sheet, row, wb, wantTupleDate=False)

            dummyCols = ord(startExcelCol) - ord('A')                # Eliminiamo le colonne vuote da A fino allo startExcelCol
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

