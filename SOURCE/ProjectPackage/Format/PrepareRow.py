#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# ################################################################
# - Verifichiamo che non ci siano colonne vuote
# ################################################################
def prepareRow(gv, rowValue=None):
    # Prj         = gv.Prj
    # LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))
    fld = gv.EXCEL.columnName

    if rowValue == None:
        rowValue = []
        for i in range(gv.EXCEL.maxCols):
            rowValue.append(u'.')

        rowValue[fld.AUTHOR_NAME] = 'EMPTY'
        rowValue[fld.ALBUM_NAME]  = 'EMPTY'
        rowValue[fld.TYPE]        = 'EMPTY'
        rowValue[fld.PUNTEGGIO]   = 0
        rowValue[fld.SONG_SIZE]   = 0

    for i in range(gv.EXCEL.startAttrIndex, gv.EXCEL.maxCols):
        if rowValue[i] == '':
            rowValue[i] = u'.'

    if rowValue[fld.AUTHOR_NAME] == '': rowValue[fld.AUTHOR_NAME] = 'UNKNOWN'
    if rowValue[fld.ALBUM_NAME]  == '': rowValue[fld.ALBUM_NAME]  = 'UNKNOWN'
    if rowValue[fld.TYPE]        == '': rowValue[fld.TYPE]        = 'UNKNOWN'
    rowValue[fld.PUNTEGGIO]   = int(rowValue[fld.PUNTEGGIO])
    rowValue[fld.SONG_SIZE]   = int(rowValue[fld.SONG_SIZE])


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))

    return rowValue

