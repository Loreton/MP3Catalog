#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import ast




################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def ReadExcelDB(gv, xlsFile, rangeToProcess):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()



    csvFileInput  = xlsFile.rsplit('.', -1)[0] + '.csv'

    logger.debug('XLS file name:    {0}'.format(xlsFile))
    logger.debug('CSV file name:    {0}'.format(csvFileInput))


        # - Se il csv è più vecchio dell'xls facciamo l'export
    if gv.Ln.Fmtime(xlsFile) > gv.Ln.Fmtime(csvFileInput):
        msg= 'range To process: {0}'.format(rangeToProcess)
        logger.debug(); print(msg)
        mydata  = gv.Ln.Excel(xlsFile)
        mydata.exportCSV('Catalog', outFname=csvFileInput, rangeString=rangeToProcess, colNames=4, fPRINT=True)
    else:
        msg = 'excel file is older than CSV file. No export will take place.'
        logger.debug(msg); print(msg)


    return csvFileInput
