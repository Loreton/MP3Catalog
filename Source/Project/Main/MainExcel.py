#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import ast




################################################################################
# - M A I N - Excel
# - Prevede:
# -  leggere il file excel, esportarlo in CSV
# -  se action==merge allora fa il merge con la directory degli MP3
# -  e crea un file CSV di output.
################################################################################
def Main(gv, action):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()
    # gv.data = gv.Ln.LnDict()


        # ---------- E X C E L
    if gv.INPUT_PARAM.actionCommand == 'excel.export':
        xlsFile       = os.path.abspath(os.path.join(gv.Prj.dataDIR, gv.INPUT_PARAM.excelFile))
        csvFileInput  = gv.Prj.ReadExcelDB(gv, xlsFile, gv.ini.EXCEL.RangeToProcess)
        csvFileMerged = xlsFile.rsplit('.', -1)[0] + '.merged.csv'

        # requiredColNames = ';'.join(gv.song.colsName)
        # RECs = gv.Prj.ReadCSVFile(gv, csvFileInput, requiredColNames)

    # gv.song.dict.PrintTree(fEXIT=True, MaxLevel=3)
    if gv.INPUT_PARAM.actionCommand == 'excel.merge':
    # if action == 'merge':
            # -----------------------------------------------------------------------
            # - Merging del dictionary con la directory sorgente
            # -----------------------------------------------------------------------
        mergedLIST = gv.Prj.Merge(gv, gv.ini.MAIN.MP3SourceDir, gv.song.dict)
            # -----------------------------------------------------------------------
            # - Salviamo il tutto in formato csv
            # -----------------------------------------------------------------------
        gv.Prj.WriteCSVFile(gv, csvFileMerged, mergedLIST)
        print ()
        C.printYellowH('file: {0} has been saved.'.format(csvFileMerged), tab=4)

        # gv.Prj.SQL(gv, csvFileMerged, mergedLIST)
        # gv.song.PrinclstTree(MaxLevel=2)


