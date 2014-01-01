#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# =======================================================================
# sample()
# =======================================================================
def sample():
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

# =========================================================================
# - Si aspetta una lista dove oni riga è a sua volta una lista
# =========================================================================
def WriteCatalogToExcel(outFileName, dict):
    # fDEBUG = True
    fDEBUG = False

    if fDEBUG:
        MyLogger.debug('*'*40)
        dict.printDictionary()
        MyLogger.debug('*'*40)

        # --------------------------------------------
        # - Creazione del file di Output
        # --------------------------------------------
    WkBook = xlwt.Workbook()
    WkSheet = WkBook.add_sheet('MP3_Catalog', cell_overwrite_ok=True)

    (nLevels, linee) = dict.dictionaryToList(MaxDeepLevel=99, fPRINT=False, OutList='Full', Attrib=True, sortIt=True) # ritorna una lista di liste
    fDEBUG = False
    # fDEBUG = True
    if fDEBUG:
        MyLogger.debug('*'*40)
        for line in linee:
            MyLogger.debug(line)
        MyLogger.debug('*'*40)
    # LnSys.exit.exit(LnSys.EXIT_STACK, "--------------- TempoTemporaTemporary DEBUG Exit ---------------------")


    prevAlbumName=''
    prevAuthorName=''
    currRow=0
    startExcelCol = globalARGs[START_EXCEL_COLUMN].upper()   # Colonna di partenza dati

    for row in linee:
        try:
                # Assicurati che il SongSIZE sia INTEGER
            songSize        = row[fldName.SONG_SIZE]
            songPunteggio   = row[fldName.PUNTEGGIO]
            row[fldName.SONG_SIZE] = int(songSize)
            row[fldName.PUNTEGGIO] = int(songPunteggio)
        except:
            print "ERROR on line: (SongSize or Punteggio are  NOT Valid) oppure char strani (es ',' virgola) nella riga"
            print "    %s" % (row)

            # ###################################
            choice = LnSys.getKeyboardInput("* ERRORE.... *", keyLIST='ENTER', exitKey='QX')
            # ###################################
        currRow += 1
        MyLogger.debug('writing row[%d]: %s' % (currRow, row))
        albumName   = row[fldALBUM]
        authorName  = row[fldAUTHOR]
        if authorName != prevAuthorName:
            prevAlbumName  = albumName
            prevAuthorName = authorName
            MyLogger.info("writing [%-40s]-[%s]" % (authorName, albumName) )


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
            # WkSheet.write(currRow, col, "Ciao sono Loreto")
            # WkSheet.col(col).width = colsWidth
            # excelRrow.write(col, value, style)


    WkBook.save(outFileName)
    MyLogger.info("File: %s has been written!" % (outFileName))




    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
