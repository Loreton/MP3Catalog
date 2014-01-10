#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os
import types

# class myClass():    pass

# =======================================================================
# ReadExcelCatalog()
# =======================================================================
def readCatalog(gv, MP3Dict):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered   - [called by:%s]' % (calledBy(1)))

    fDEBUG = False
    excelFileName = gv.CONFIG.EXCEL_INPUT_FILE


    if not os.path.isfile(excelFileName):
        Prj.exit(gv, 10, "File doesn't exists: [%s]" % (excelFileName))

    logger.info("Reading excelFileName: [%s]."  % (excelFileName))
    prevAuth = '...'

        # Ritorna il WorkBook
    wb = LN.excel.open(gv, excelFileName)

        # Esaminiamo tutti gli sheet (in teroia è solo il primo)
    for sheet in wb.sheets():
        gv.EXCEL.sheetName = sheet.name
        logger.info('Analizzo sheetName: %s' % (sheet.name))
        startExcelCol = gv.CONFIG.START_EXCEL_COLUMN.upper()   # Colonna di partenza dati

        for row in range(sheet.nrows):
            rowValue = LN.excel.getRow(gv, sheet, row, wb, wantTupleDate=False)

            dummyCols = ord(startExcelCol) - ord('A')                # Eliminiamo le colonne vuote da A fino allo startExcelCol
            while dummyCols:
                del rowValue[0]
                dummyCols -= 1
                # print '^^^^ removing item', rowValue[0]
            logger.debug("rowValue: [%s]" % (rowValue))

                # ------------------------------------------
                # - calcoliamo i nomi delle colonne
                # ------------------------------------------
                    # - Verifica che i campi siano corretti ed enumera gli stessi
            if row == gv.CONFIG.COLUMNS_NAME_ROW:
                fld = Prj.excel.prepareHeader(gv, rowValue)
                # LN.dict.printDictionaryTree(gv, gv.EXCEL, header="Column Names [%s]" % calledBy(0), retCols='LTV', lTAB=' '*4, console=True)
                continue

            elif row<gv.CONFIG.FIRST_SONG_ROW:
                continue

            elif row>gv.CONFIG.LAST_SONG_ROW:
                logger.warning("."*60)
                logger.warning("MAX_ROWs has been reached.......")
                logger.warning("."*60)
                break

            if row%100 == 0: print "%6d/%6d rows has been processed" % (row, sheet.nrows)
            nCols     = len(rowValue)

            if nCols > gv.EXCEL.maxCols:               # ultima colonna valida
                rowValue = rowValue[:gv.EXCEL.maxCols]
            elif nCols < gv.EXCEL.maxCols:               # NON PREVISTO
                print "riga numero:", row
                print rowValue
                Prj.exit(gv, 11, "Il numero di colonne del file non puo' essere inferiore alle colonne previste. [nCols:%d]<[fld.SONG_SIZE:%d]" % (nCols, fld.SONG_SIZE) )


            songName    = rowValue[fld.SONG_NAME]

                 # riga vuota
            if rowValue[fld.TYPE] == '' or rowValue[fld.TYPE] == '#':
                logger.debug("SKIPPING - empty or commented(#) row: [%s]" % (rowValue))
                continue

            if fDEBUG: print "^^^^^ %s/%s/%s/%s" % (rowValue[fld.TYPE], rowValue[fld.AUTHOR_NAME], rowValue[fld.ALBUM_NAME], songName), type(songName)

            if type(songName) == types.IntType or len(songName) < 2:
                logger.warning("SKIPPING - invalid songName: [%s]" % (songName))
                continue

            if songName.find('_NO_MATCH_ON_DISK_') > 0:
                logger.warning("SKIPPING - _NO_MATCH_ON_DISK_ song: [%s]" % (songName))
                continue

            if prevAuth != rowValue[fld.AUTHOR_NAME]:
                prevAuth = rowValue[fld.AUTHOR_NAME]
                logger.info("reading author: [%s]" % (rowValue[fld.AUTHOR_NAME]) )

            rowValue = Prj.fmt.prepareRow(gv, rowValue)

            if len(songName) >= 2 and rowValue[fld.TYPE] != 'Titles':
                Prj.mp3.insertSong(gv, MP3Dict, rowValue)
                if rowValue[fld.TYPE] == 'UNKNOWN':
                    choice=LN.sys.getKeyboardInput(gv, "Vuoi continuare???", validKeys="Y", exitKey='XQ')



    # ###################################
    # choice=LN.sys.getKeyboardInput(gv, "******* STOP Temporaneo *******", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
    # ###################################


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))


