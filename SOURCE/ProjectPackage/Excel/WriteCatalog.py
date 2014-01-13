#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os

import xlwt

# =========================================================================
# - Si aspetta una lista dove oni riga è a sua volta una lista
# =========================================================================
def writeCatalog(gv, outFileName, outLines):
    # Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))

        # --------------------------------------------
        # - Creazione del file Excel di Output (in memoria)
        # --------------------------------------------
    WkBook  = xlwt.Workbook()
    WkSheet = WkBook.add_sheet('MP3_Catalog', cell_overwrite_ok=True)


    prevAlbumName=''
    prevAuthorName=''
    currRow=0
    startExcelCol = gv.CONFIG.START_EXCEL_COLUMN.upper()   # Colonna di partenza dati
    fld = gv.EXCEL.columnName

    for row in outLines:
        try:
                # Assicurati che il SongSIZE sia INTEGER
            row[fld.SONG_SIZE]   = int(row[fld.SONG_SIZE])      # convert unicode to integer
            row[fld.PUNTEGGIO]   = int(row[fld.PUNTEGGIO])      # convert unicode to integer
            # row[fld.PUNTEGGIO]   = "=MP3_SommaSE(RC[2]:RC[11],RC[12]:RC[20],R4C8:R4C17)"
            # row[fld.PUNTEGGIO]   = "=MP3_SommaSE(H8:Q8;R8:Z8;$H$4:$Q$4)"

        except:
            print "row[fld.SONG_SIZE]", type(row[fld.SONG_SIZE]), row[fld.SONG_SIZE]
            print "row[fld.PUNTEGGIO]", type(row[fld.PUNTEGGIO]), row[fld.PUNTEGGIO]
            print "ERROR on line: (SongSize or Punteggio are  NOT Valid) oppure char strani (es ',' virgola) nella riga"
            print "    %s" % (row)
            # ####################
            choice=LN.sys.getKeyboardInput(gv, "******* SongSize or Punteggio are  NOT Valid *******", validKeys="ENTER", exitKey='X,Q', keySep=',', deepLevel=3, fDEBUG=False)
            # ####################

        currRow += 1
        logger.debug('writing row[%d]: %s' % (currRow, row))
        albumName   = row[fld.ALBUM_NAME]
        authorName  = row[fld.AUTHOR_NAME]
        if authorName != prevAuthorName:
            prevAlbumName  = albumName
            prevAuthorName = authorName
            logger.info("writing [%-40s]-[%s]" % (authorName, albumName) )


        excelRrow = WkSheet.row(currRow)    # pointer alla riga

            # Inseriamo le colonne vuote per allineare il foglio
        dummyCols = ord(startExcelCol) - ord('A')
        while dummyCols:
            row.insert(0, '')               # inseriamo la colonna 0 - Vuota
            dummyCols -= 1

        col = 0
        for value in row:
            WkSheet.write(currRow, col, value)
            col += 1

        logger.console(row[:5])


    WkBook.save(outFileName)
    logger.console("File: %s has been written. Totla Songs = %d" % (outFileName, currRow))

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return currRow



