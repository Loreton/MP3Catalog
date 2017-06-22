#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# ####################################################################################################################
import sys
import os
import sqlite3
import inspect
from ..LnCommon.LnColor  import LnColor
C=LnColor()


# https://en.wikibooks.org/wiki/A_Beginner's_Python_Tutorial/Classes
INFO = 1
class LnSqLite:

    def _internaLogger(self, package=None):
        ##############################################################################
        # - classe che mi permette di lavorare nel caso il logger non sia richiesto
        ##############################################################################
        class nullLogger():
                def __init__(self, package=None, stackNum=1):
                    pass
                def info(self, data):
                    self._print(data)
                def debug(self, data):
                    self._print(data)
                def error(self, data):  pass
                def warning(self, data):  pass

                def _print(self, data):
                    caller = inspect.stack()[4]
                    dummy, programFile, lineNumber, funcName, lineCode, rest = caller
                    if funcName == '<module>': funcName = '__main__'
                    str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=funcName, LINENO=lineNumber, DATA=data)
                    print (str)

        return nullLogger()


        # ***********************************************
        # *
        # ***********************************************
    def __init__(self, DBFile, createFile=False, logger=None):
        self._dbfile         = DBFile
        # self._create         = create
        self._conn           = None
        # self._cursor         = None
        self.description    = "This shape has not been described yet"
        self.author         = "Nobody has claimed to make this shape yet"
        self.myLogger = None

        if logger:
            # self._logger = logger(package=__name__)
            self._setLogger = logger
            # self._setLogger = logger
        else:
            self._setLogger = self._internaLogger

        # self._mainLogger = self._setLogger(package=__name__)

        # if createFile or not os.path.isfile(self._dbfile):
        self._OpenDB(createFile)
        # else:
            # self._conn   = sqlite3.connect(self._dbfile)

        # ***********************************************
        # * OpenDBase
        # ***********************************************
    def _OpenDB(self, createFile=False):
        logger = self._setLogger(package=__name__)
        if os.path.isfile(self._dbfile):
            logger.info("DBFile already exists: {DBFILE}".format(DBFILE=self._dbfile) )
            if createFile:
                msg = """
                    DBFile already exists: {DBFILE}
                    Press 'y' to replace current file
                    Press 'i' ignore and continue using current DB file
                    Press 'x' to exit : """.format(DBFILE=self._dbfile)

                choice = self._getInput(msg, validKey='yi', exitKey='xX')
                if choice.lower() == 'y':
                    logger.info("deleting DBFILE: {0}".format(self._dbfile) )
                    os.remove(self._dbfile)

        # -----------------------------------
        # - Connecting to the database file
        # - Il file viene creato se non esiste
        # -----------------------------------
        logger.info("connecting to DBFILE: {0}".format(self._dbfile) )
        self._conn   = sqlite3.connect(self._dbfile)
        # self._cursor = self._conn.cursor()
        # print (self._cursor)


        # ***********************************************
        # *
        # ***********************************************
    def _getCursor(self):
        return self._conn.cursor()

        # ***********************************************
        # *
        # ***********************************************
    def nRows(self, tblName):
        logger = self._setLogger(package=__name__)
        cur = self._conn.cursor()
        comando="SELECT Count(*) FROM {TABLE}".format(TABLE=tblName)
        logger.info(comando)
        cur.execute(comando)
        nRows=cur.fetchone()[0]
        return nRows


        # ***********************************************
        # *
        # ***********************************************
    def Close(self):
        self.Commit()
        self._conn.close()

        # ***********************************************
        # *
        # ***********************************************
    def Commit(self):
        logger = self._setLogger(package=__name__)
        logger.info('Committing...')
        self._conn.commit()

        # ***********************************************
        # *
        # ***********************************************
    def _getInput(self, msg, validKey='\n', exitKey='xXqQ'):
        while True:
            choice = input(msg).strip()
            if choice == '':
                msg = "     Pleae enter something...: "
            elif choice in exitKey:
                sys.exit()
            elif choice in validKey:
                return choice.lower()
            else:
                msg = "     Try again...: "


        # ***********************************************
        # * Fa ENUM dei FIELDS, rimuovendo i BLANK nei nomi
        # ***********************************************
    def EnumFields(self, tblName, myDict):
        fieldsName, *rest = self.GetStruct(tblName)
        col = myDict()
        for index, name in enumerate(fieldsName):
            colName = name.replace(' ', '')
            col[colName] = index
        return col


        # ***********************************************
        # *
        # ***********************************************
    def _SQL_execute(self, command, fCOMMIT=False):
        logger = self._setLogger(package=__name__)
        logger.info(command)
        cur = self._getCursor()
        cur.execute(command)
        rCode = self._conn.total_changes
        if fCOMMIT:
            self.Commit()

        return rCode



        # ***********************************************
        # *
        # ***********************************************
    def Version(self, fPRINT=False):
        cur = self._getCursor()
        cur.execute('SELECT SQLITE_VERSION()')
        version = cur.fetchone()
        if fPRINT:
            print ("SQLite version: {VERSION}".format(VERSION=version))

        return version



        # ***********************************************
        # *
        # * struct  = create table if not exists ${Table.name} (
        # *                    "Type"              STRING  NOT NULL,
        # *                    "Author Name"       STRING  NOT NULL
        # *                )
        # ***********************************************
    def CreateTable(self, tblName, forceCreate=False, struct=None, script=None):
        logger = self._setLogger(package=__name__)
        cur = self._getCursor()

        if forceCreate:
            comando = 'DROP TABLE if exists     {TABLE}'.format(TABLE=tblName)
            logger.info(comando)
            cur.execute(comando)
            rcode = cur.fetchone()
            self.Commit()

        if script:
            comando = script
            logger.info(comando)
            cur.executescript(comando)

        else:
            comando = 'CREATE TABLE if not exists {TABLE} {STRUCT}'.format(TABLE=tblName, STRUCT=struct)
            logger.info(comando)
            cur.execute(comando)

        self.Commit()

        # ***********************************************
        # * return LIST with all records
        # ***********************************************
    def TableToList(self, tblName, LoL=False):
        logger = self._setLogger(package=__name__)
        cur = self._getCursor()


        tableData = cur.execute('SELECT * FROM {TABLE};'.format(TABLE=tblName))
        RECs = []
        for record in tableData:
            if LoL:
                RECs.append(record)
            else:
                # converte all items to string
                xx = [str(item) for item in record] # potrebbe dare errore se qualce item non è stringa
                RECs.append(';'.join(xx))

        return RECs

        # ####################################################################
        # - Creazione del dictionary
        # - startAttributesField : indica il numero di campo da cui iniziano
        # -                        i valori e saranno inseriti come val del
        # -                        tree delle key
        # ####################################################################
    def TableToDict(self, tblName, startAttributesField, myDict):
        logger = self._setLogger(package=__name__)
        mainDict            = myDict()
        RECs = self.TableToList(tblName, LoL=True)

        fieldsName, *rest = self.GetStruct(tblName)

        for record in RECs:
            # print(len(record), record)
            ptr = mainDict

                # --------------------------------------------------
                # - creazione dictionary tree con tutti i field
                # - identificati come key-dict.
                # - (Es. per mp3:  type.author.album.songName)
                # --------------------------------------------------
            for key in record[:startAttributesField]:
                if not key in ptr:
                    ptr[key] = myDict()
                ptr = ptr[key]

                # su ogni tree mettiamo i vari attributi
            for index, value in enumerate(record[startAttributesField:]):
                # print(index, startAttributesField)
                attrName  = fieldsName[index+startAttributesField]
                ptr[attrName] = value


        # mainDict.PrintTree()
        return mainDict



        # ###################################################################
        # - Inserisce una riga in una tabella.
        # - Se record==[LIST di [LIST]] allora fa una massInsert/executeMany
        # - INSERT into LOGTABLE (ts, level, message)   VALUES (111, "autoinc test", "autoinc test");
        # - INSERT into LOGTABLE                        VALUES (111, "autoinc test", "autoinc test");
        # ###################################################################
    def InsertRow(self, tblName, colName='', record="", fCOMMIT=False):
        logger  = self._setLogger(package=__name__)
        cur     = self._getCursor()

        EXECUTE_MANY = False
        if isinstance(record, list):
            if isinstance(record[0], list):
                EXECUTE_MANY = True
                nFields = len(record[0])
                logger.info('Massive insertions')
            else:
                nFields = len(record)   # TESTED OK
        else:
            msg = "\n\nInsertRow: LIST type is required as row data\n\n"
            logger.info(msg)
            sys.exit()

        fields = '?'
        for inx in range(1, nFields):
            fields += ',?'

        RECs = self._Validate(tblName, record)

        InsertCommand = 'INSERT or IGNORE into {TABLE} {COLS} VALUES ({FIELDS})'.format(TABLE=tblName, FIELDS=fields, COLS=colName)
        InsertCommand = 'INSERT or REPLACE into {TABLE} {COLS} VALUES ({FIELDS})'.format(TABLE=tblName, FIELDS=fields, COLS=colName)
        logger.info(InsertCommand)
        logger.info('inserting {0} records'.format(len(RECs)))

        if EXECUTE_MANY:
            cur.executemany(InsertCommand, RECs)
        else:
            cur.execute(InsertCommand, RECs)

        if fCOMMIT:
            self.Commit()




    def DeleteRow(self, tblName, colName, value, fCOMMIT=False):
        comando = 'DELETE from {TABLE} where "{COL}"="{VAL}"'.format(TABLE=tblName, COL=colName, VAL=value)
        changes = self._SQL_execute(comando, fCOMMIT=fCOMMIT)
        print ('changes:', changes)




    def Describe(self):
        cursor = self._conn.cursor()
        tablesToIgnore = ["sqlite_sequence"]
        TAB = ' '*5

        totalTables = 0
        totalColumns = 0
        totalRows = 0
        totalCells = 0

        # Get List of Tables:
        tableListQuery = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        cursor.execute(tableListQuery)
        # tables = map(lambda t: t[0], cursor.fetchall())   # originale
        tables = cursor.fetchall()                          # Loreto


        for tbl in tables:
            table = tbl[0]

            if (table in tablesToIgnore):
                continue

            print ('\n'*2)
            # self._Print(TAB + "{TABLE:<23}{NCOLS:<10}{NROWS:<10}{CELLS:<10}".format(TABLE='TableName', NCOLS='Columns', NROWS='Rows', CELLS='Cells'))
            columnsQuery = "PRAGMA table_info(%s)" % table
            cursor.execute(columnsQuery)
            numberOfColumns = len(cursor.fetchall())

            rowsQuery = "SELECT Count() FROM %s" % table
            cursor.execute(rowsQuery)
            numberOfRows = cursor.fetchone()[0]

            numberOfCells = numberOfColumns*numberOfRows

            # self._Print("%s\t%d\t%d\t%d" % (table, numberOfColumns, numberOfRows, numberOfCells))
            self._Print("""
                TableName:  {TABLE}
                nColumns:   {NCOLS}
                nRows:      {NROWS}
                nCells:     {CELLS}
                """.format( TABLE=table,
                            NCOLS=numberOfColumns,
                            NROWS=numberOfRows,
                            CELLS=numberOfCells))

            totalTables     += 1
            totalColumns    += numberOfColumns
            totalRows       += numberOfRows
            totalCells      += numberOfCells

            # Recs = self.TableToList(table)
            # for row in Recs:
            #     print (TAB, row)



        self._Print(TAB +  "" )
        self._Print(TAB +  "Number of Tables:   {0:>10}".format(totalTables ))
        self._Print(TAB +  "Number of Columns:  {0:>10}".format(totalColumns ))
        self._Print(TAB +  "Number of Rows:     {0:>10}".format(totalRows ))
        self._Print(TAB +  "Number of Cells:    {0:>10}".format(totalCells ))

        for tbl in tables:
            table = tbl[0]

            if (table in tablesToIgnore):
                continue

    ##############################################################
    # #
    ##############################################################
    def GetStruct(self, tblName):
        logger  = self._setLogger(package=__name__)
        cur     = self._getCursor()

            # --------------------------
            # - get structure
            #    = (FieldNO, fieldName, fieldType, NOT_NULL, DEF_VALUE, PRI_KEY)
            # --------------------------
        comando = 'PRAGMA TABLE_INFO({TABLE})'.format(TABLE=tblName)
        logger.info(comando)
        struct = cur.execute(comando)

        fieldName    = []
        fieldType    = []
        fieldNotNULL = []
        defaultVAL   = []

        for field in struct:
            logger.debug(field)
            seq, NAME, TYPE, NOT_NULL, DEFAULT, PRI_KEY = field
            fieldName.append(NAME)
            fieldType.append(TYPE)
            fieldNotNULL.append(NOT_NULL)
            defaultVAL.append(DEFAULT)

        logger.info('fieldName: {0}'.format(fieldName))
        logger.info('fieldType: {0}'.format(fieldType))
        logger.info('defaultVAL: {0}'.format(defaultVAL))
        logger.info('fieldNotNULL: {0}'.format(fieldNotNULL))

        return fieldName, fieldType, fieldNotNULL, defaultVAL



    ##############################################################
    # #
    ##############################################################
    def _Validate(self, tblName, tableData):
        logger  = self._setLogger(package=__name__)
        cur     = self._getCursor()

        fieldName, fieldType, fieldNotNULL, defaultVAL = self.GetStruct(tblName)
        nFLD = len(fieldName)
        '''
        if not tableData: # leggiamo la tabella
            cur       = self._getCursor()
            tableData = cur.execute('SELECT * FROM {TABLE};'.format(TABLE=tblName))
        '''

        RECs  = []
        for row in tableData:
            if not len(row) == nFLD:
                print()
                C.printYellow('errore nella lunghezza del record di input', tab=4)
                print()
                C.printYellow( "len:{0:02} - {1}".format(len(row), row), tab=4)
                print()
                C.printYellow( "len:{0:02} - {1}".format(len(fieldName), fieldName), tab=4)
                C.printYellow( "len:{0:02} - {1}".format(len(fieldType), fieldType), tab=4)
                C.printYellow( "len:{0:02} - {1}".format(len(fieldNotNULL), fieldNotNULL), tab=4)
                C.printYellow( "len:{0:02} - {1}".format(len(defaultVAL), defaultVAL), tab=4)
                print()
                import traceback
                traceback.print_stack()
                '''
                print ('--------------')
                traceback.print_exc()
                import inspect
                for item in reversed(inspect.stack()):
                    print (item[1:])
                print ('--------------')
                for item in inspect.trace():
                    print (item[1:])
                '''
                sys.exc_info()[2]
                sys.exit()

            myRow = []
            for inx, field in enumerate(row):

                    # --------------------------------------------
                    # - se il campo ha valore prendiamo quello,
                    # - altrimenti se è impostato NOT_NULL
                    # - prendiamo il DEFAULT se c'è altrimenti 0
                    # --------------------------------------------
                if fieldType[inx] == 'INTEGER':
                    if field:
                        val = int(field)
                    else:
                        if fieldNotNULL[inx]:
                            if defaultVAL[inx]:
                                val = defaultVAL[inx]
                            else:
                                val = 0
                    # val = int(field) if field else defaultVAL[inx]
                    myRow.append(val)

                elif fieldType[inx] == 'TEXT':
                    if field:
                        val = field
                    else:
                        if fieldNotNULL[inx]:
                            if defaultVAL[inx]:
                                val = defaultVAL[inx]
                            else:
                                val = '_'

                    if val == '.': val = defaultVAL[inx]

                    # val = field if field else defaultVAL[inx]
                    # if fieldNotNULL[inx]: val = defaultVAL[inx]
                    myRow.append(val)

                else:
                    myRow.append(field)

            RECs.append(myRow)

            # DEBUG
        # for record in RECs[0:10]: print (record)


        return RECs




    def _Print(self, msg):
        outputFilename = None

        if (outputFilename != None):
            outputFile = open(outputFilename,'a')
            print >> (outputFile, msg)
            outputFile.close()
        else:
            print (msg)



#################################################################
#   M   A   I   N
#################################################################

if __name__ == '__main__':

    myDB = LnDB("/tmp/aaa.db", create=True, logger=True)
    myDB.Version(fPRINT=True)

    TableName   =  'ProvaTable'
    TableStruct   =  '''(
                            'Interface Name'        TEXT  NOT NULL,
                            "Family"                TEXT  NOT NULL,
                            "IP Address"            TEXT  ,
                            "IP Broadcat"           TEXT  ,
                            "Gateway"               TEXT  ,
                            "Default GW"            INTEGER DEFAULT(0)  ,
                            'Network mask'          TEXT ,
                            'Route table'           TEXT ,
                            'Subnet'                CAHR(15) ,
                            primary key ("Interface Name", Family)
                        )
            '''


    myDB.CreateTable(TableName, forceCreate=False,  struct=TableStruct, script=None, fCOMMIT=True)
    Recs = (myDB.TableToList(TableName))
    nRows = myDB.nRows(TableName)
    print ("TableName1 Records:", len(Recs), "nRows:", nRows)
    # print (Recs)

    record = []
    record.append('name1')
    record.append('family1')
    record.append('address1')
    record.append('bcast1')
    record.append('gateway1')
    record.append(True)
    record.append('nmask1')
    record.append('table1')
    record.append('subnet1')
    myDB.InsertRow(TableName, record=record, fCOMMIT=False)
    # print ('nRows:', myDB.nRows(TableName))
    record = []
    record.append('name2')
    record.append('family2')
    record.append('address2')
    record.append('bcast2')
    record.append('gateway2')
    record.append(True)
    record.append('nmask2')
    record.append('table2')
    record.append('subnet2')
    myDB.InsertRow(TableName, record=record, fCOMMIT=False)
    # print ('nRows:', myDB.nRows(TableName))
    record = []
    record.append('name1')
    record.append('family1')
    record.append('address1')
    record.append('bcast1')
    record.append('gateway1')
    record.append(True)
    record.append('nmask1')
    record.append('table1')
    record.append('subnet1')
    myDB.InsertRow(TableName, record=record, fCOMMIT=False)
    # print ('nRows:', myDB.nRows(TableName))
    record = []
    record.append('name2')
    record.append('family2')
    record.append('address2')
    record.append('bcast2')
    record.append('gateway2')
    record.append(True)
    record.append('nmask2')
    record.append('table2')
    record.append('subnet2')
    myDB.InsertRow(TableName, record=record, fCOMMIT=False)
    myDB.Commit()

    Recs = (myDB.TableToList(TableName))
    print ("TableName1 Records:", len(Recs), "nRows:", nRows)
    # print (Recs)

    record = []
    record.append('name3')
    record.append('family3')
    record.append('address3')
    record.append('bcast3')
    record.append('gateway3')
    record.append(True)
    record.append('nmask3')
    record.append('table3')
    record.append('subnet3')

    myDB.InsertRow(TableName, colName=Recs[0], record=record, fCOMMIT=False)
    Recs = (myDB.TableToList(TableName))
    nRows = myDB.nRows(TableName)
    print ("TableName1 Records:", len(Recs), "nRows:", nRows)
    # print (Recs)


    print ('\n'*5)


        # con ID autoincremental
    TableName2   =  'ProvaTable2'
    TableStruct2   =  '''(
                            'recNO'                 INTEGER PRIMARY_KEY,
                            'Interface Name'        TEXT  ,
                            "Family"                TEXT  ,
                            "IP Address"            TEXT  ,
                            "IP Broadcat"           TEXT  ,
                            "Gateway"               TEXT  ,
                            "Default GW"            INTEGER DEFAULT(0)  ,
                            'Network mask'          TEXT ,
                            'Route table'           TEXT ,
                            'Subnet'                CAHR(15)
                        )
            '''

    myDB.CreateTable(TableName2, forceCreate=False, struct=TableStruct2, script=None, fCOMMIT=True)
    Recs = (myDB.TableToList(TableName2))
    nRows = myDB.nRows(TableName2)
    print ("TableName2 Records:", len(Recs), "nRows:", nRows)
    # print (Recs)

    record = []
    record.append(None)
    record.append('name1')
    record.append('family1')
    record.append('address1')
    record.append('bcast1')
    record.append('gateway1')
    record.append(True)
    record.append('nmask1')
    record.append('table1')
    record.append('subnet1')
    myDB.InsertRow(TableName2, colName=Recs[0], record=record, fCOMMIT=False)
    record = []
    record.append(None)
    record.append('name2')
    record.append('family2')
    record.append('address2')
    record.append('bcast2')
    record.append('gateway2')
    record.append(True)
    record.append('nmask2')
    record.append('table2')
    record.append('subnet2')
    myDB.InsertRow(TableName2, colName=Recs[0], record=record, fCOMMIT=False)
    record = []
    record.append(None)
    record.append('name1')
    record.append('family1')
    record.append('address1')
    record.append('bcast1')
    record.append('gateway1')
    record.append(True)
    record.append('nmask1')
    record.append('table1')
    record.append('subnet1')
    myDB.InsertRow(TableName2, colName=Recs[0], record=record, fCOMMIT=False)
    record = []
    record.append(None)
    record.append('name2')
    record.append('family2')
    record.append('address2')
    record.append('bcast2')
    record.append('gateway2')
    record.append(True)
    record.append('nmask2')
    record.append('table2')
    record.append('subnet2')
    myDB.InsertRow(TableName2, colName=Recs[0], record=record, fCOMMIT=False)


    # ---- DELETE -----
    Recs = myDB.TableToList(TableName2)
    print ("TableName2 Records:", len(Recs), "nRows:", myDB.nRows(TableName2))

    # myDB.DeleteRow(TableName2, 'recNO', '5', fCOMMIT=True)
    myDB.DeleteRow(TableName2, 'Family', 'family1', fCOMMIT=False)
    Recs = myDB.TableToList(TableName2)
    print ("TableName2 Records:", len(Recs), "nRows:", myDB.nRows(TableName2))

    myDB.DeleteRow(TableName, 'Interface Name', 'eth0', fCOMMIT=True)
    Recs = myDB.TableToList(TableName)
    print ("TableName1 Records:", len(Recs), "nRows:", myDB.nRows(TableName))

    # SELECT rowid,Family FROM ProvaTable

    myDB.Describe()
    myDB.Close()
    sys.exit()

