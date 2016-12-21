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
    gv.song = gv.Ln.LnDict()

    # gv.data = gv.Ln.LnDict()

        # -------------------------------------------
        # creazione struttura DBdict
        # prelievo filename e create flag ed altro
        # -------------------------------------------
    DBdict                  = gv.Ln.LnDict()

    filename, create        = gv.ini.SqLite.DB_filename.split(',')
    DBdict.filename         = os.path.abspath(os.path.join(gv.Prj.dataDIR, filename.strip()))
    DBdict.filecreate       = True if create.strip().lower() == 'create' else False
    print (DBdict.filename)
    csvFileInput            = os.path.splitext(DBdict.filename)[0] + '.csv'
    print (csvFileInput)

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

        # =======================================
        # ---------- I M P O R T
        # =======================================
    if gv.INPUT_PARAM.actionCommand == 'sqlite.import':
        csvData = gv.Prj.ReadCSVFile(gv, gv.INPUT_PARAM.csvInputFile, gv.song.colsName)
        rCode   = DB.InsertRow(tblName=DBdict.songTableName, record=csvData[1:], fCOMMIT=True)


        # =======================================
        # -  M E R G E
        # =======================================
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.merge':

            # ---- lettura DBase
        gv.song.dict = DB.TableToDict(DBdict.songTableName, startAttributesField=4, myDict=gv.Ln.LnDict)

            # -----------------------------------------------------------------------
            # - Merging del dictionary con la directory sorgente e ...
            # - ... validazione con i file
            # -----------------------------------------------------------------------
        fieldsName, *rest = DB.GetStruct(DBdict.songTableName)
        attributeNames = fieldsName[4:]
        gv.Prj.Merge(gv, gv.ini.MAIN.MP3SourceDir, gv.song.dict, attributeNames)
        songList = gv.Prj.Validate(gv, gv.ini.MAIN.MP3SourceDir, gv.song.dict)

            # - update della tabella
        print ("Aggiornamento DBase... nRecords: {0}".format(len(songList)))
        # for record in songList[:20]: print(record)

        # ----- AGGIORNAMENTO DBase
        choice = gv.Ln.getKeyboardInput("    Vuoi aggiornare il DBase?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
        if choice.lower() in ['yes']:
            msg = 'writing data to table: {0}'.format(DBdict.songTableName)
            rCode = DB.InsertRow(tblName=DBdict.songTableName, record=songList, fCOMMIT=True)


        # =======================================
        # - E X P O R T
        # =======================================
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.export':
            # ---- lettura DBase
        # songDict = DB.TableToDict(DBdict.songTableName, startAttributesField=4, myDict=gv.Ln.LnDict)
        # songLIST = songDict.ToList()

        songLIST = DB.TableToList(DBdict.songTableName)



        fieldsName = DB.GetStruct(DBdict.songTableName)[0]
        songLIST = sorted(songLIST)
        songLIST.insert(0, ';'.join(fieldsName))
        # for record in songLIST[:20]: print(record)
        csvOutputFile = gv.INPUT_PARAM.csvOutputFile
        if not csvOutputFile: csvOutputFile = os.path.splitext(DBdict.filename)[0] + '.out.csv'
        gv.Prj.WriteCSVFile(gv, csvOutputFile, data=songLIST)