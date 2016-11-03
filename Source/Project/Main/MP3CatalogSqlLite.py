#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys




################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv, action):
    logger  = gv.Ln.SetLogger(package=__name__, CONSOLE=gv.INPUT_PARAM.LogCONSOLE)
    C       = gv.Ln.Colors()
    gv.data = gv.Ln.LnDict()

        # -----------------------------------
        # - Importing Excel File if required
        # -----------------------------------
    if action == 'importExcel':
        csvData = gv.Ln.excel.readExcelData(fileName)