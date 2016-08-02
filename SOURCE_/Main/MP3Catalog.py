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
    logger  = gv.Ln.setLogger(package=__name__, CONSOLE=gv.INPUT_PARAM.LogCONSOLE)
    C       = gv.Ln.Colors()
    gv.data = gv.Ln.LnDict()

    # csvFile                 = gv.Prj.dataDIR + '/MP3_Master_2015-08-10.csv'
    csvFile                 = gv.Prj.dataDIR + '/MP3_Master_2016-07-25.csv'
    gv.data.fileScartate    = gv.Prj.dataDIR + '/_Scartate.csv'
    gv.data.fileAnalizzate  = gv.Prj.dataDIR + '/_Analizzate.csv'
    gv.data.fileValidSongs  = gv.Prj.dataDIR + '/_ValidSongs.csv'

    # if action == 'extract' or action == 'copySongs':
    rowList = gv.Prj.readFile(gv, csvFile)
    RECs = []       # RECs una lista di liste/canzoni
    for row in rowList:
        tokens = [token.strip() for token in row.split(';') if token]
        RECs.append(tokens)
    sf = gv.Prj.songFilter(gv, RECs)

    choice = gv.Ln.getKeyboardInput(gv, "    Vuoi salvare i dati su file?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
    if choice.lower() in ['x']:
        sys.exit()

    elif choice.lower() in ['yes']:
        C.printYellow('writing file: {0}'.format(gv.data.fileScartate), tab=4)
        gv.Prj.writeFile(gv, gv.data.fileScartate,   data=sf.scartate)

        C.printYellow('writing file: {0}'.format(gv.data.fileValidSongs), tab=4)
        gv.Prj.writeFile(gv, gv.data.fileValidSongs,   data=sf.validSongs)

        C.printYellow('writing file: {0}'.format(gv.data.fileAnalizzate), tab=4)
        gv.Prj.writeFile(gv, gv.data.fileAnalizzate, data=sf.analizzate)



    if action == 'copySongs':
        choice = gv.Ln.getKeyboardInput(gv, "    Continuare per copiare le canzoni sulla destinazione?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
        if choice.lower() in ['x', 'no']:
            sys.exit()

        RECs = sf.validSongs[:]
        logger.info('trovate {0} canzoni da copiare'.format(len(RECs)))
        if gv.INPUT_PARAM.fCHECK_SOURCE:
            gv.Prj.checkSourceSongs(gv, RECs)
        else:
            gv.Prj.copySongs(gv, RECs)

    else:
        C.printRed('Action {0} not yet implemented...!'.format(action), tab=8)
        sys.exit()