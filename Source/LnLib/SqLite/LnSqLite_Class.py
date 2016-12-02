#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# ####################################################################################################################
import sys
import os
import sqlite3
import inspect

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
                def debug(self, data):  pass
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
    def __init__(self, DBFile, create=False, logger=False):
        self._dbfile         = DBFile
        self._create         = create
        self.conn           = None
        self.cursor         = None
        self.description    = "This shape has not been described yet"
        self.author         = "Nobody has claimed to make this shape yet"
        self.myLogger = None

        if logger:
            self._logger = logger
        else:
            self._logger = self._internaLogger()
        if self._create or not os.path.isfile(self._dbfile):
            self._CreateDB()


        # ***********************************************
        # *
        # ***********************************************
    def _CreateDB(self):
        # print (self._dbfile)

        if os.path.isfile(self._dbfile):
            self._logger.info("DBFile already exists: {DBFILE}".format(DBFILE=self._dbfile) )
            msg = """
                DBFile already exists: {DBFILE}
                Press 'd' to destroy current file
                Press 'c' to continue with current DB file
                Press 'xq' to exit : """.format(DBFILE=self._dbfile)

            choice = self._getInput(msg, validKey='dDcC', exitKey='qQxX')
            if choice == 'd':
                self._logger.info("deleting DBFILE: {0}".format(self._dbfile) )
                os.remove(self._dbfile)

        # -----------------------------------
        # - Connecting to the database file
        # - Il file viene creato se non esiste
        # -----------------------------------
        self._logger.info("creating DBFILE: {0}".format(self._dbfile) )
        self.conn   = sqlite3.connect(self._dbfile)
        self.cursor = self.conn.cursor()


        # ***********************************************
        # *
        # ***********************************************
    def Cursor(self):
        return self.conn.cursor()

        # ***********************************************
        # *
        # ***********************************************
    def nRows(self, tblName):
        cur = self.conn.cursor()
        comando="SELECT Count(*) FROM {TABLE}".format(TABLE=tblName)
        self._logger.info(comando)
        cur.execute(comando)
        nRows=cur.fetchone()[0]
        return nRows


        # ***********************************************
        # *
        # ***********************************************
    def Close(self):
        self.Commit()
        self.conn.close()

        # ***********************************************
        # *
        # ***********************************************
    def Commit(self):
        self._logger.info('Committing...')
        self.conn.commit()

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
        # *
        # ***********************************************
    def _SQL_execute(self, command, fCOMMIT=False):
        self._logger.info(command)
        cur = self.Cursor()
        cur.execute(command)
        rCode = self.conn.total_changes
        if fCOMMIT:
            self.Commit()

        return rCode



        # ***********************************************
        # *
        # ***********************************************
    def Version(self, fPRINT=False):
        cur = self.Cursor()
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
    def CreateTable(self, TblName, forceCreate=False, struct=None, script=None, fCOMMIT=False):
        cur = self.Cursor()

        if forceCreate:
            comando = 'DROP TABLE if exists     {TABLE}'.format(TABLE=TblName)
            self._logger.info(comando)
            cur.execute(comando)
            rcode = cur.fetchone()

        if script:
            comando = script
            self._logger.info(comando)
            cur.executescript(comando)

        else:
            comando = 'CREATE TABLE if not exists {TABLE} {STRUCT}'.format(TABLE=TblName, STRUCT=struct)
            self._logger.info(comando)
            cur.execute(comando)

        if fCOMMIT:
            self._logger.info('committing...')
            self.Commit()

        # ***********************************************
        # * return LIST qith all records
        # ***********************************************
    def ReadTable(self, TblName):
        cur = self.Cursor()

            # get structure
        comando = 'PRAGMA TABLE_INFO({TABLE})'.format(TABLE=TblName)
        self._logger.info(comando)
        cur.execute(comando)

        colsName = [tup[1] for tup in cur.fetchall()]

        if False:
            cur.execute('PRAGMA TABLE_INFO({TABLE})'.format(TABLE=TblName))
            print ('................ Table:', TblName)
            # cur.fetchall() = (FieldNO, fieldName, fieldType, NOT_NULL, DEF_VALUE, PRI_KEY)
            for tup in cur.fetchall():
                print (tup)

            # (0, 'recNO', 'INTEGER PRIMARY_KEY', 0, None, 0)

            # get Records
        RECs  = []
        RECs.append(tuple(colsName))
        for row in cur.execute('SELECT * FROM {TABLE};'.format(TABLE=TblName)):
            # RECs.append(list(row)) # LIST
            RECs.append(row) # tuple

        return RECs

        # ***********************************************
        # - Inserisce una riga in una tabella.
        # - Se record==LIST di LIST allora fa una massInsert/executeMany
        # - INSERT into LOGTABLE (ts, level, message)   VALUES (111, "autoinc test", "autoinc test");
        # - INSERT into LOGTABLE                        VALUES (111, "autoinc test", "autoinc test");
        # ***********************************************
    def InsertRow(self, TblName, colName='', record="", fCOMMIT=False):
        cur = self.Cursor()

        EXECUTE_MANY = False
        if isinstance(record, list):
            if isinstance(record[0], list):
                nFields = len(record[0])
                EXECUTE_MANY = True
                self._logger.info('Massive insertions')
            else:
                nFields = len(record)   # TESTED OK
        else:
            msg = "\n\nInsertRow: Attesa LIST per i campi\n\n"
            self._logger.info(msg)
            sys.exit()

        fields = '?'
        for inx in range(1, nFields):
            fields += ',?'

        InsertCommand = 'INSERT or IGNORE into {TABLE} {COLS} VALUES ({FIELDS})'.format(TABLE=TblName, FIELDS=fields, COLS=colName)
        self._logger.info(InsertCommand)

        if EXECUTE_MANY:
            cur.executemany(InsertCommand, record)
        else:
            cur.execute(InsertCommand, record)

        if fCOMMIT:
            self.Commit()

    def DeleteRow(self, TblName, colName, value, fCOMMIT=False):
        comando = 'DELETE from {TABLE} where "{COL}"="{VAL}"'.format(TABLE=TblName, COL=colName, VAL=value)
        changes = self._SQL_execute(comando, fCOMMIT=fCOMMIT)
        print ('changes:', changes)




    def Describe(self):
        cursor = self.conn.cursor()
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

            print ('\n'*5)
            self._Print(TAB + "{TABLE:<23}{NCOLS:<10}{NROWS:<10}{CELLS:<10}".format(TABLE='TableName', NCOLS='Columns', NROWS='Rows', CELLS='Cells'))
            columnsQuery = "PRAGMA table_info(%s)" % table
            cursor.execute(columnsQuery)
            numberOfColumns = len(cursor.fetchall())

            rowsQuery = "SELECT Count() FROM %s" % table
            cursor.execute(rowsQuery)
            numberOfRows = cursor.fetchone()[0]

            numberOfCells = numberOfColumns*numberOfRows

            # self._Print("%s\t%d\t%d\t%d" % (table, numberOfColumns, numberOfRows, numberOfCells))
            self._Print(TAB + "{TABLE:<15}{NCOLS:10}{NROWS:10}{CELLS:10}".format(TABLE=table, NCOLS=numberOfColumns, NROWS=numberOfRows, CELLS=numberOfCells))

            totalTables += 1
            totalColumns += numberOfColumns
            totalRows += numberOfRows
            totalCells += numberOfCells

            Recs = self.ReadTable(table)
            for row in Recs:
                print (TAB, row)



        self._Print(TAB +  "" )
        self._Print(TAB +  "Number of Tables:         {0:>10}".format(totalTables ))
        self._Print(TAB +  "Total Number of Columns:  {0:>10}".format(totalColumns ))
        self._Print(TAB +  "Total Number of Rows:     {0:>10}".format(totalRows ))
        self._Print(TAB +  "Total Number of Cells:    {0:>10}".format(totalCells ))

        for tbl in tables:
            table = tbl[0]

            if (table in tablesToIgnore):
                continue




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
    Recs = (myDB.ReadTable(TableName))
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

    Recs = (myDB.ReadTable(TableName))
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
    Recs = (myDB.ReadTable(TableName))
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
    Recs = (myDB.ReadTable(TableName2))
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
    Recs = myDB.ReadTable(TableName2)
    print ("TableName2 Records:", len(Recs), "nRows:", myDB.nRows(TableName2))

    # myDB.DeleteRow(TableName2, 'recNO', '5', fCOMMIT=True)
    myDB.DeleteRow(TableName2, 'Family', 'family1', fCOMMIT=False)
    Recs = myDB.ReadTable(TableName2)
    print ("TableName2 Records:", len(Recs), "nRows:", myDB.nRows(TableName2))

    myDB.DeleteRow(TableName, 'Interface Name', 'eth0', fCOMMIT=True)
    Recs = myDB.ReadTable(TableName)
    print ("TableName1 Records:", len(Recs), "nRows:", myDB.nRows(TableName))

    # SELECT rowid,Family FROM ProvaTable

    myDB.Describe()
    myDB.Close()
    sys.exit()

