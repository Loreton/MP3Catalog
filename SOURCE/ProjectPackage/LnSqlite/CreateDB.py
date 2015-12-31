#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-

# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

# ####################################################################################################
# Due metodi:
# ####################################################################################################
import sqlite3

def createDB_0(gv, sqlite_file):
    sqlite_file = 'my_first_db.sqlite'      # name of the sqlite database file
    table_name1 = 'my_table_1'              # name of the table to be created
    table_name2 = 'my_table_2'              # name of the table to be created
    new_field = 'my_1st_column'             # name of the column
    field_type = 'INTEGER'                  # column data type

    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Creating a new SQLite table with 1 column
    c.execute('CREATE TABLE {tn} ({nf} {ft})'\
            .format(tn=table_name1, nf=new_field, ft=field_type))

    # Creating a second table with 1 column and set it as PRIMARY KEY
    # note that PRIMARY KEY column must consist of unique values!
    c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
            .format(tn=table_name2, nf=new_field, ft=field_type))

    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()




def createTable(gv, DBFile, TblName, ColNames):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy



    # Connecting to the database file

    conn = sqlite3.connect(DBFile)
    c = conn.cursor()

    # Creating a new SQLite table with 1 column
    # c.execute('CREATE TABLE {tn} ({nf} {ft})'\
    try:
        c.execute('CREATE TABLE if not exists {tn} ({nf})'.format(tn=TblName, nf=ColNames))

    except (sqlite3.OperationalError) as why:
        print ('ERROR', str(why))


    conn.commit()
    conn.close()

    # gv.LN.dict.printDictionaryTree(gv, DB, header="DBase [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)
    # printDict(DB)
    # myprint(DB)



    # DB = LnClass()
    # DB.Table01 = LnClass()
    # DB.Table02 = LnClass()
    # DB.Table02.Autore.type = 'STRING'
    # DB.Table02.Albun.type = 'STRING'
    # DB.Table02.Albun.type = 'STRING'

def printDict(dict):
    for k, v in dict.items():
        if type(v) is dict:
            print()
            printDict(v)
        else:
            print ("{0} : {1}".format(k, v))

def myprint(d):
    stack = d.items()
    while stack:
        k, v = stack.pop()
        if isinstance(v, dict):
            stack.extend(v.items())
        else:
            print("%s: %s" % (k, v))

if __name__ == "__main__":
    DB = {
        'name'   : 'LoretoMP3',
        'Tabella01' : {
            'name'      : 'LoretoMP3',
            'Autore'    : ['', 'STRING'],
            'Album'     : ['', 'STRING'],
            'Song Name' : ['', 'STRING'],
        },
    }
    ColNamesx = [
        ('Type'          , 'STRING'),
        ('Author Name'   , 'STRING'),
        ('Album Name'    , 'STRING'),
        ('Song Name'     , 'STRING') ,
        ('Punteggio'     , 'INTEGER'),
        ('Analizzata'    , 'STRING'),
        ('Recomended'    , 'STRING'),
        ('Loreto'        , 'STRING'),
        ('Buona'         , 'STRING'),
        ('Soft'          , 'STRING'),
        ('Vivace'        , 'STRING'),
        ('Molto Viv'     , 'STRING'),
        ('Camera'        , 'STRING'),
        ('Car'           , 'STRING'),
        ('Lenta'         , 'STRING'),
        ('Country'       , 'STRING'),
        ('Strumentale'   , 'STRING'),
        ('Classica'      , 'STRING'),
        ('Lirica'        , 'STRING'),
        ('Live'          , 'STRING'),
        ('Discreta'      , 'STRING'),
        ('Undefined'     , 'STRING'),
        ('Avoid it'      , 'STRING'),
        ('Confusionaria' , 'STRING'),
        ('Song Size'     , 'STRING') ,
    ]

    printDict(DB)
    # myprint(DB)

