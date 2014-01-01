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
def verifyColContent(gv, attribCols):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))


    # baseAttribValue = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0']
    for i in range(len(attribCols)-1):
        if attribCols[i] == '':
            attribCols[i] = u'.'


    logger.info('exiting - [called by:%s]' % (calledBy(1)))

    return attribCols
