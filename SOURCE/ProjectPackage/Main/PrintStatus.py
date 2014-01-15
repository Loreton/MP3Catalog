#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################




def printStatus(gv):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    cfgModule  = gv.CONFIG.FILE_MODULE

    LN.sys.getKeyboardInput(gv, LN.cYELLOW + "* Presse ENTER ver visualizzare il report", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
    cfgModule.verifica()
    LN.dict.printDictionaryTree(gv, gv.COPY, header="COPY dict data [%s]" % calledBy(0), retCols='TVL', lTAB=' '*4, console=True)
