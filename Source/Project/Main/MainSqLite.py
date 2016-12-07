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
def Main(gv, action):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()

    # gv.data = gv.Ln.LnDict()

        # -------------------------------------------
        # creazione struttura DBdict
        # prelievo filename e create flag ed altro
        # -------------------------------------------
    DBdict                  = gv.Ln.LnDict()
    DBdict.filename         = os.path.abspath(os.path.join(gv.Prj.dataDIR, gv.ini.SqLite.DB_filename))
    DBdict.filecreate       = True if gv.ini.SqLite.DB_filecreate.lower() == 'true' else False
    DBdict.songTableName    = gv.ini.SqLite['songTable.name']
    DBdict.songTableCreate  = True if gv.ini.SqLite['songTable.forcecreate'].lower() == 'true' else False
    DBdict.songTableStruct  = gv.ini.SqLite['songTable.struct']

        # --------------------------------------------
        # - connessione al DB.
        # - force creazione file in base al flag
        # --------------------------------------------
    DB = gv.Ln.LnSqLite(DBdict.filename, DBdict.filecreate, logger=gv.Ln.SetLogger)


        # --------------------------------------------
        # - Apertura/creazione Table in base al flag
        # --------------------------------------------
    if DBdict.songTableCreate:
        DB.CreateTable(DBdict.songTableName, forceCreate=DBdict.songTableCreate, struct=DBdict.songTableStruct, script=None, fCOMMIT=True)
        DB.Describe()

    # DBdict.PrintTree(fEXIT=True)

    # gv.song.dict.PrintTree(fEXIT=True, MaxLevel=3)

        # ---------- I M P O R T
    if gv.INPUT_PARAM.actionCommand == 'sqlite.import':
        csvData = gv.Prj.ReadCSVFile(gv, gv.INPUT_PARAM.csvInputFile, gv.song.colsName)
        print (len(csvData))
        rCode = DB.InsertRow(TblName=DBdict.songTableName, record=csvData, fCOMMIT=True)

    elif gv.INPUT_PARAM.actionCommand == 'sqlite.verify':
        # ---------------------------------------
        # - lettura directory sorgente di MP3
        # ---------------------------------------
        sourceDir = gv.INPUT_PARAM.MP3SourceDir
        listaFile = gv.Ln.DirList(sourceDir, patternLIST=['*.mp3'], onlyDir=False, maxDeep=99)
        if listaFile == []:
            gv.Ln.Exit(43, 'non sono stati trovati file nella directory indicata: {0}'.format(sourceDir))
        print (len(listaFile))




