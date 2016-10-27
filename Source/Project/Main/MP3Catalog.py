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
    logger  = gv.Ln.setLogger(gv, package=__name__)
    C       = gv.Ln.Colors()
    gv.data = gv.Ln.LnDict()

    # extraSections       = gv.Ln.LnDict()
    # extraSections.MAIN  = gv.Ln.LnDict()

    iniConfigParser, iniDict = gv.Ln.ReadIniFile(gv, gv.Prj.iniFileName, RAW=False, exitOnError=True, subSectionChar='.')

    # gv.Ln.printDict(gv, iniDict)
    gv.ini = gv.Ln.LnDict(iniDict)
    if gv.fDEBUG:
        gv.ini.printDict(gv)


        # -----------------------------------
        # - Importing Excel File if required
        # -----------------------------------
    xlsFile = os.path.abspath(os.path.join(gv.Prj.dataDIR, gv.ini.EXCEL.EXCEL_File))
    csvFile = xlsFile.rsplit('.', -1)[0] + '.csv'

    if gv.fIMPORT_EXCEL:
        mydata = gv.Ln.Excel(xlsFile)
        mydata.exportToCSV2('Catalog', outFname=csvFile, rangeString="B2:Z17", colNames=4, fPRINT=False)
        # mydata.exportToDict('Catalog', fPRINT=False)

    fileScartate        = gv.Prj.dataDIR + '/_Scartate.csv'
    fileAnalizzate      = gv.Prj.dataDIR + '/_Analizzate.csv'
    fileValidSongs      = gv.Prj.dataDIR + '/_ValidSongs.csv'
    fileDuplicateSongs  = gv.Prj.dataDIR + '/_DuplicateSongs.csv'

    gv.Ln.exit(gv, 0, "--------------- debugging exit ----------------", printStack=False, stackLevel=9, console=True)


        # ----------------------------------------------
        # - Preleviamo tutte le canzoni analizzate
        # - Analizzata;Recomended;Loreto;Buona;Soft;Vivace;Molto Viv;Camera;Car;Lenta;Count
        # ----------------------------------------------
    gv.songList = gv.Ln.LnDict()
    songList = gv.songList
    songList.validSongs  = [gv.Prj.songColumsName]  # init con il nome delle colonne
    songList.analizzate  = [gv.Prj.songColumsName]  # init con il nome delle colonne
    songList.scartate    = [gv.Prj.songColumsName]  # init con il nome delle colonne
    songList.duplicate   = [gv.Prj.songColumsName]  # init con il nome delle colonne


        # ------------------------------------------------------------
        # - Lettura del file.csv
        # - La prima riga conriene il nome delle colonne
        # - Eliminiamo i blank nei nomi colonne
        # ------------------------------------------------------------
    rowList = gv.Prj.readFile(gv, csvFile)
    rowList[0] = rowList[0].replace(' ', '')   # eliminiamo i BLANK nei nomi colonne
    if not rowList[0].strip().strip(';') == ';'.join(gv.Prj.songColumsName):
        C.printYellowH('i nomi delle colonne non coincidono', tab=4)
        C.printYellowH('file     : {0}'.format(rowList[0]), tab=4)
        C.printYellowH('required : {0}'.format(';'.join(gv.Prj.songColumsName)), tab=4)
        sys.exit()

        # RECs creazione di una lista di liste/canzoni [[],[],..]
    RECs = []
    for row in rowList[1:]:
        tokens = [token.strip() for token in row.split(';') if token]
        RECs.append(tokens)
    gv.Prj.songFilter(gv, RECs)
    choice = gv.Ln.getKeyboardInput(gv, "    Vuoi salvare i dati sui relativi file?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
    if choice.lower() in ['x']:
        sys.exit()

    elif choice.lower() in ['yes']:
        C.printYellow('writing file: {0}'.format(fileScartate), tab=4)
        gv.Prj.writeFile(gv, fileScartate,   data=songList.scartate)

        C.printYellow('writing file: {0}'.format(fileValidSongs), tab=4)
        gv.Prj.writeFile(gv, fileValidSongs,   data=songList.validSongs)

        C.printYellow('writing file: {0}'.format(fileAnalizzate), tab=4)
        gv.Prj.writeFile(gv, fileAnalizzate, data=songList.analizzate)



    if action == 'copySongs':
        choice = gv.Ln.getKeyboardInput(gv, "    Continuare per copiare le canzoni sulla destinazione?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
        if choice.lower() in ['x', 'no']:
            sys.exit()

        RECs = songList.validSongs[:]
        logger.info('trovate {0} canzoni da copiare'.format(len(RECs)))
        if gv.INPUT_PARAM.fCHECK_SOURCE:
            gv.Prj.checkSourceSongs(gv, RECs)
        else:
            gv.Prj.copySongs(gv, RECs)
            print()
            C.printYellow('writing file: {0}'.format(fileDuplicateSongs), tab=4)
            print()
            gv.Prj.writeFile(gv, fileDuplicateSongs, data=songList.duplicate)

            gv.copySong.printDict(gv)

    else:
        C.printRed('Action {0} not yet implemented...!'.format(action), tab=8)
        sys.exit()