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

        # ---------- I M P O R T
    if gv.INPUT_PARAM.actionCommand == 'sqlite.import':
        csvData = gv.Prj.ReadCSVFile(gv, gv.INPUT_PARAM.csvInputFile, gv.song.colsName)
        rCode   = DB.InsertRow(tblName=DBdict.songTableName, record=csvData[1:], fCOMMIT=True)


        # ---------- M E R G E
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.merge':
            # ---- lettura DBase
        # RECs         = DB.TableToList(DBdict.songTableName)
        gv.song.dict = DB.TableToDict(DBdict.songTableName, startAttributesField=gv.song.field.SongName+1, myDict=gv.Ln.LnDict)

            # -----------------------------------------------------------------------
            # - Merging del dictionary con la directory sorgente e ...
            # - ... validazione con i file
            # -----------------------------------------------------------------------
        fieldsName, *rest = DB.GetStruct(DBdict.songTableName)
        attributeNames = fieldsName[4:]
        gv.Prj.Merge(gv, gv.ini.MAIN.MP3SourceDir, gv.song.dict, attributeNames)
        songList = gv.Prj.Validate(gv, gv.ini.MAIN.MP3SourceDir, gv.song.dict)

        # update della tabella
        print ("Aggiornamento DBase... nRecords: {0}".format(len(songList)))
        rCode   = DB.InsertRow(tblName=DBdict.songTableName, record=songList, fCOMMIT=True)



        # ---------- R E O R D E R --- columns
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.reorder':
        songDict = DB.TableToDict(DBdict.songTableName, startAttributesField=gv.song.field.SongName+1, myDict=gv.Ln.LnDict)

        keyList = songDict.KeyList()
        logger.info('andiamo a validare {0} records'.format(len(keyList)))


        songLIST = []  # conterrà le canzoni in formato listOfList
        for songQualifiers in keyList:
            if songQualifiers == []: continue

                # - otteniamo il pointer alla canzone
            ptrSong = songDict.Ptr(songQualifiers)

            # ================================================
            # - Convertiamo il dict-record in una LIST
            # ================================================
                # - prepare newSongEntry
            mySong = songQualifiers[:]

                # - get song attributes values
            songAttr = ptrSong.GetValue(fPRINT=False)
            mySong.append(songAttr['ToBeDeleted'])
            # mySong.append(songAttr['Punteggio']) # remove
            mySong.append(songAttr['Analizzata'])
            mySong.append(songAttr['Recomended'])
            mySong.append(songAttr['Loreto'])
            mySong.append(songAttr['Buona'])
            mySong.append(songAttr['Soft'])
            mySong.append(songAttr['Vivace'])
            mySong.append(songAttr['Molto Viv'])
            mySong.append(songAttr['Camera'])
            mySong.append(songAttr['Car'])
            mySong.append(songAttr['Lenta'])
            mySong.append(songAttr['Country'])
            mySong.append(songAttr['Strumentale'])
            mySong.append(songAttr['Classica'])
            mySong.append(songAttr['Lirica'])
            mySong.append(songAttr['Live'])
            mySong.append(songAttr['Discreta'])
            mySong.append(songAttr['Undefined'])
            mySong.append(songAttr['Avoid it'])
            mySong.append(songAttr['Confusionaria'])
            mySong.append(songAttr['Song Size'])
            songLIST.append(mySong)

    for record in songLIST[:10]:
        print (record)
