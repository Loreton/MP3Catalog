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



    # file = 'j:\\GIT-REPO\\Python3\\MP3Catalog\\data\\LnMP3DBase_201612.csv'
    # LnZip('d:\\zTemp\\pippo.zip', 'j:\\GIT-REPO\\Python3', file)
    # sys.exit()

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

    if not os.path.isfile(DBdict.filename):
        DBdict.songTableCreate = True
    else:
        if os.stat(DBdict.filename).st_size == 0:
            DBdict.songTableCreate = True

    C.printYellow("working on DBase: {0}".format(DBdict.filename))
    C.printYellow("working on Table: {0}".format(DBdict.songTableName))

        # =======================================
        # - connessione al DB.
        # - creazione se flag.filecreate
        # =======================================
    DB = gv.Ln.LnSqLite(DBdict.filename, DBdict.filecreate, logger=gv.Ln.SetLogger)
    # DBdict.DB = DB

        # --------------------------------------------
        # - Apertura/creazione Table in base al flag
        # --------------------------------------------
    if DBdict.songTableCreate:
        DB.CreateTable(DBdict.songTableName, forceCreate=DBdict.songTableCreate, struct=DBdict.songTableStruct, script=None)
        DB.Describe()

    fieldsName = DB.GetStruct(DBdict.songTableName)[0]
    fieldsName, *rest = DB.GetStruct(DBdict.songTableName)

    # gv.song.FIELD           = gv.Ln.LnEnum(fieldsName, myDict=gv.Ln.LnDict)
    # gv.song.FIELD_WEIGHTED  = gv.Ln.LnEnum(fieldsName, myDict=gv.Ln.LnDict, weighted=True)

        # =======================================
        # ---------- I M P O R T
        # =======================================
    if gv.INPUT_PARAM.actionCommand == 'sqlite.import':
        csvData = gv.Prj.ReadCSVFile(gv, gv.INPUT_PARAM.csvInputFile, fieldsName)
        rCode   = DB.InsertRow(tblName=DBdict.songTableName, record=sorted(csvData[1:]), fCOMMIT=True)


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
        attributeNames              = fieldsName[4:]
        mergeChanges                = gv.Prj.Merge(gv, gv.ini.MAIN.MP3SourceDir, gv.song.dict, attributeNames)
        songList, validateChanges   = gv.Prj.Validate(gv, gv.ini.MAIN.MP3SourceDir, gv.song.dict, fieldsName)

            # - update della tabella
        # ----- AGGIORNAMENTO DBase
        if mergeChanges > 0:
            print ("Aggiornamento DBase... nRecords : {0}".format(len(songList)))
            print ("merge    changes                : {0}".format(mergeChanges))
            print ("validate changes                : {0}".format(validateChanges))
            choice = gv.Ln.getKeyboardInput("    Vuoi aggiornare il DBase?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
            if choice.lower() in ['yes']:
                msg = 'writing data to table: {0}'.format(DBdict.songTableName)
                rCode = DB.InsertRow(tblName=DBdict.songTableName, record=sorted(songList), fCOMMIT=True)

                    # modifichiamo il default char '_' in punto '.'
                for colName in attributeNames:
                    comando = "UPDATE {TBL} SET {COL1}='.' WHERE {COL1}='_'".format(TBL=DBdict.songTableName, COL1=colName)
                    changes = DB.ExecuteSQL(comando, fCOMMIT=False)
                DB.Commit()

        # =======================================
        # - E X P O R T
        # =======================================
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.fullexport':
        csvFile = DB.TableExport(tblName=DBdict.songTableName)
        print ()
        C.printYellowH("il file {0} e' stato correttamente creato".format(csvFile), tab=4)
        print ()

        # =======================================
        # - B A C K U P
        # =======================================
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.backup':
        zipFile = DB.TableBackup(tblName=DBdict.songTableName)
        print ()
        C.printYellowH("il file {0} e' stato correttamente creato".format(zipFile), tab=4)
        print ()

       # =======================================
        # - E X P O R T
        # =======================================
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.export':
        if gv.INPUT_PARAM.exportQuery:
           print (gv.INPUT_PARAM.exportQuery)
           queryStr = ''
           for item in gv.INPUT_PARAM.exportQuery:
                if ' ' in item:
                    item = '"{0}"'.format(item)
                queryStr += ' ' + item
           print (queryStr)

        elif gv.ini.SqLite.exportString:
           queryStr = gv.ini.SqLite.exportString
        else:
           queryStr = 'SELECT * FROM {TABLE};'.format(TABLE=DBdict.songTableName)

        DB.TableExport(tblName, queryStr=queryStr)




       # =======================================
        # - E X P O R T
        # =======================================
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.export_OLD':
            # ---- lettura DBase
        # songDict = DB.TableToDict(DBdict.songTableName, startAttributesField=4, myDict=gv.Ln.LnDict)
        # songLIST = songDict.ToList()

        if gv.INPUT_PARAM.exportQuery:
           print (gv.INPUT_PARAM.exportQuery)
           queryStr = ''
           for item in gv.INPUT_PARAM.exportQuery:
                if ' ' in item:
                    item = '"{0}"'.format(item)
                queryStr += ' ' + item
           print (queryStr)

        elif gv.ini.SqLite.exportString:
           queryStr = gv.ini.SqLite.exportString
        else:
           queryStr = 'SELECT * FROM {TABLE};'.format(TABLE=DBdict.songTableName)

        songLIST = DB.TableToList(DBdict.songTableName, query=queryStr)



        songLIST = sorted(songLIST)
        songLIST.insert(0, ';'.join(fieldsName))
        # for record in songLIST[:20]: print(record)
        csvOutputFile = gv.INPUT_PARAM.csvOutputFile

        basedir, dbfname = os.path.split(DBdict.filename)
        fname, ext = os.path.split(dbfname)
        if not csvOutputFile:
            csvOutputFile = os.path.splitext(DBdict.filename)[0] + '.csv'

        fileList = [dbfname, csvOutputFile ]

        zipFileName = os.path.join(gv.Prj.dataDIR, dbfname) + '.zip'
        gv.Ln.CreateZipBackupFile(zipFileName, basedir=gv.Prj.dataDIR, fileList=fileList)

        gv.Prj.WriteCSVFile(gv, csvOutputFile, data=songLIST)




        # =======================================
        # - C O P Y S O N G S
        # =======================================
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.copySongs':
        songLIST = DB.TableToList(DBdict.songTableName, LoL=True)
        validSONGS = gv.Prj.songFilter(gv, songLIST, fieldsName)
        # validSONGS = gv.Prj.SqlSongFilter(gv, DBdict)

        choice = gv.Ln.getKeyboardInput("    Vuoi procedere con la copia delle canzoni sulla DEST?" , keySep=",", validKeys='yes,no', exitKey='X', deepLevel=2)
        if choice.lower() in ['yes']:
            gv.Prj.copySongs(gv, validSONGS, fieldsName)
            # songList    = gv.songList




        # =======================================
        # - E X E C U T E    S Q L
        # - mettere il comando di comodo
        # - Es.:
        # -     UPDATE LoretoMP3 SET Lenta='.' WHERE Lenta='_'
        # =======================================
    elif gv.INPUT_PARAM.actionCommand == 'sqlite.executeSQL':
        attributeName = fieldsName[4:-1] # elimina type, author, album, songName,...., songSize

        '''
        for colName in attributeName:
            comando = "UPDATE {TBL} SET {COL1}='x' WHERE NOT {COL2} IN ('_', '.')".format(TBL=DBdict.songTableName, COL1=colName, COL2=colName)
            changes = DB.ExecuteSQL(comando, fCOMMIT=False)
            print ("[{0:9}] - {1}".format(changes, comando))

        print()

        for colName in attributeName:
            comando = "UPDATE {TBL} SET {COL1}='.' WHERE {COL2}='_'".format(TBL=DBdict.songTableName, COL1=colName, COL2=colName)
            changes = DB.ExecuteSQL(comando, fCOMMIT=False)
            print ("[{0:9}] - {1}".format(changes, comando))
        '''

        EXCLUDE_DATA = """
                       Avoid='x'
                    OR Confusionaria='x'
                    OR Discreta='x'
                    OR MoltoVivace='x'
                    OR Classica='x'
                    OR Lirica='x'
                    OR Live='x'
                    OR Undefined='x'
                    """

            # set Car if ...
        myCommand = """
            UPDATE {TBL}
             SET Car='x'
                WHERE (
                    Soft='x'
                    )
                AND NOT (
                    Car='x'
                    OR Avoid='x'
                    OR Confusionaria='x'
                    OR Discreta='x'
                    OR MoltoVivace='x'
                    OR Classica='x'
                    OR Lirica='x'
                    OR Live='x'
                    OR Undefined='x'
                )
            """.format(TBL=DBdict.songTableName)


            # set Car if ...
        myCommand = """
            UPDATE {TBL}
                SET Car='.'
                    WHERE (
                           Avoid='x'
                        OR Confusionaria='x'
                        OR Discreta='x'
                        OR MoltoVivace='x'
                        OR Classica='x'
                        OR Lirica='x'
                        OR Live='x'
                        OR Undefined='x'
                    )
                    AND NOT (
                        Car='.'
                    )
            """.format(TBL=DBdict.songTableName)


            # set Loreto if ...
        myCommand = """
            UPDATE {TBL}
                SET Loreto='x'
                    WHERE (
                        Recomended='x'
                    )
                    AND NOT (
                        Loreto='x'
                    )
            """.format(TBL=DBdict.songTableName)


            # set Loreto if ...
        myCommand = """
            SELECT Type, AuthorName, AlbumName, SongName
                FROM {TBL}
                WHERE (
                    Loreto='x'
                AND NOT (
                    {EXCLUDE}
                )
            """.format(TBL=DBdict.songTableName, EXCLUDE=EXCLUDE_DATA)

            # set Car if ...
        myCommand = """
            UPDATE {TBL}
                SET Camera='.'
                    WHERE (
                        Soft='x'
                        AND Vivace='.'
                        AND NOT Camera='x'
                    )
                    AND NOT (
                        {EXCLUDE}
                    )
            """.format(TBL=DBdict.songTableName, EXCLUDE=EXCLUDE_DATA)



            # set Car if ...
        myCommand = """
            SELECT Type, AuthorName, AlbumName, SongName
                FROM {TBL}
                WHERE (
                    Soft='x'
                    AND Vivace='.'
                    AND NOT Camera='x'
                )
                AND NOT (
                    {EXCLUDE}
                )
            """.format(TBL=DBdict.songTableName, EXCLUDE=EXCLUDE_DATA)

                    # AND Loreto='x'
        WhereClause = """
                WHERE (
                    Soft='x'
                    AND Loreto='x'
                    AND Vivace='.'
                    AND NOT Camera='x'
                )
                AND NOT (
                    {EXCLUDE}
                )
            """.format(EXCLUDE=EXCLUDE_DATA)




        myCommandUpdate =  '''
                UPDATE {TBL}
                    SET Camera='x'
                    {WHERE_CLAUSE}
                '''.format(TBL=DBdict.songTableName, EXCLUDE=EXCLUDE_DATA, WHERE_CLAUSE=WhereClause)

        myCommandSelect =  '''
                SELECT Type, AuthorName, AlbumName, SongName FROM {TBL}
                    {WHERE_CLAUSE}
                '''.format(TBL=DBdict.songTableName, EXCLUDE=EXCLUDE_DATA, WHERE_CLAUSE=WhereClause)



        updateCommand = (x.strip() for x in myCommandUpdate.split())
        updateCommand = ' '.join(updateCommand)
        selectCommand = (x.strip() for x in myCommandSelect.split())
        selectCommand = ' '.join(selectCommand)
        print ()
        print(selectCommand)
        print ()
        print(updateCommand)
        print ()
        changes = DB.ExecuteSQL(updateCommand, fCOMMIT=False)
        print ("[{0:9}] - {1}".format(changes, updateCommand))



        if gv.INPUT_PARAM.fEXECUTE:
            DB.Commit()


