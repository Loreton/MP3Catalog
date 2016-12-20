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

    filename, create        = gv.ini.SqLite.DB_filename.split(',')
    DBdict.filename         = os.path.abspath(os.path.join(gv.Prj.dataDIR, filename.strip()))
    DBdict.filecreate       = True if create.strip().lower() == 'create' else False

    songTable, create       = gv.ini.SqLite['songTable.name'].split(',')
    DBdict.songTableName    = songTable.strip()
    DBdict.songTableCreate  = True if create.strip().lower() == 'create' else False

    DBdict.songTableStruct  = gv.ini.SqLite['songTable.struct']

        # --------------------------------------------
        # - connessione al DB.
        # - creazione file in base al flag.filecreate
        # --------------------------------------------
    DB = gv.Ln.LnSqLite(DBdict.filename, DBdict.filecreate, logger=gv.Ln.SetLogger)

        # --------------------------------------------
        # - Apertura/creazione Table in base al flag
        # --------------------------------------------
    if DBdict.songTableCreate:
        DB.CreateTable(DBdict.songTableName, forceCreate=DBdict.songTableCreate, struct=DBdict.songTableStruct, script=None)
        DB.Describe()


    # RECs = DB.TableToList(DBdict.songTableName)
    # sys.exit()



        # ---------- I M P O R T
    if gv.INPUT_PARAM.actionCommand == 'sqlite.import':
        csvData = gv.Prj.ReadCSVFile(gv, gv.INPUT_PARAM.csvInputFile, gv.song.colsName)
        rCode   = DB.InsertRow(tblName=DBdict.songTableName, record=csvData[1:], fCOMMIT=True)



        # ---------- M E R G E
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.merge':
            # -----------------------------------------------------------------------
            # - Leggiamo il DB
            # -----------------------------------------------------------------------
        # print(DB.nRows(DBdict.songTableName))
        RECs = DB.TableToList(DBdict.songTableName)
        for index, record in enumerate(RECs):
            if index > 2: break
            print (record)
        RECs = DB.TableToDict(DBdict.songTableName, startAttributesField=gv.song.field.SongName+1, myDict=gv.Ln.LnDict)

        sys.exit()

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
        '''
        # ---------------------------------------
        # - lettura directory sorgente di MP3
        # ---------------------------------------
        sourceDir = gv.INPUT_PARAM.MP3SourceDir
        listaFile = gv.Ln.DirList(sourceDir, patternLIST=['*.mp3'], onlyDir=False, maxDeep=99)
        if listaFile == []:
            gv.Ln.Exit(43, 'non sono stati trovati file nella directory indicata: {0}'.format(sourceDir))
        print (len(listaFile))
        '''




