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
def mainLite(gv, action):
    logger  = gv.Ln.setLogger(package=__name__, CONSOLE=gv.INPUT_PARAM.LogCONSOLE)
    color   = gv.Ln.Colors()
    gv.data = gv.Ln.LnDict()

    # csvFile                 = gv.Prj.dataDIR + '/MP3_Master_2015-08-10.csv'
    csvFile                 = gv.Prj.dataDIR + '/MP3_Master_2016-07-25.csv'
    gv.data.fileScartate    = gv.Prj.dataDIR + '/_Scartate.csv'
    gv.data.fileAnalizzate  = gv.Prj.dataDIR + '/_Analizzate.csv'
    gv.data.fileEstratte    = gv.Prj.dataDIR + '/_Estratte.csv'

    if action == 'extract':
        rowList = gv.Prj.readFile(gv, csvFile)
        RECs = []       # RECs una lista di liste/canzoni
        for row in rowList:
            tokens = [token.strip() for token in row.split(';') if token]
            RECs.append(tokens)
        gv.Prj.songFilter(gv, RECs)


    elif action == 'copySongs':
        rowList = gv.Prj.readFile(gv, gv.data.fileEstratte)
        # print (len(rowList))
        RECs = []
        for row in rowList:
            tokens = [token.strip() for token in row.split(';') if token]
            RECs.append(tokens)

        logger.info('trovate {0} canzoni da copiare'.format(len(RECs)))
        if gv.INPUT_PARAM.fCHECK_SOURCE:
            gv.Prj.checkSourceSongs(gv, RECs)
        else:
            gv.Prj.copySongs(gv, RECs)

    else:
        print (color.RED08 + 'Action {0} not yet implemente...!'.format(action))
        sys.exit()