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
def verifyColContent(gv, rowValue):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))


    # baseAttribValue = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0']
    attribCols = rowValue[gv.EXCEL.startAttrIndex:] # prendiamo solo i campi Attributi
    for i in range(len(attribCols)-1):
        if attribCols[i] == '':
            attribCols[i] = u'.'

    fld = gv.EXCEL.columnName
    if rowValue[fld.AUTHOR_NAME] == '': rowValue[fld.AUTHOR_NAME] = 'UNKNOWN'
    if rowValue[fld.ALBUM_NAME]  == '': rowValue[fld.ALBUM_NAME]  = 'UNKNOWN'
    if rowValue[fld.TYPE]        == '': rowValue[fld.TYPE]        = 'UNKNOWN'


    logger.info('exiting - [called by:%s]' % (calledBy(1)))


