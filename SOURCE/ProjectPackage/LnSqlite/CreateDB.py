#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-

# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

# ####################################################################################################
# Due metodi:
# ####################################################################################################
import sqlite3

    # choice=gv.LN.sys.getKeyboardInput(gv, ColNames, validKeys="c", exitKey='XQ')
def createTable(gv, DBFile, TblName=None, create=False, ColNames=None, script=None):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

        # -----------------------------------
        # - Connecting to the database file
        # -----------------------------------
    conn    = sqlite3.connect(DBFile)
    c       = conn.cursor()

        # -----------------------------------
        # - Creating/Connecting SQLite table
        # -----------------------------------
    try:
        if create:
            comando = 'DROP TABLE if exists     {TABLE}'.format(TABLE=TblName)
            c.execute(comando)
            logger.info(comando)

        if script:
            comando = script
            logger.info(comando)
            c.executescript(comando)

        else:
            comando = 'CREATE TABLE if not exists {TABLE} ({FIELDS})'.format(TABLE=TblName, FIELDS=ColNames)
            logger.info (comando)
            c.execute(comando)

    except (sqlite3.OperationalError) as why:
        logger.error ('ERROR', str(why))

    except Exception as why:
        gv.LN.exit(gv, 1001, str(why), printStack=True)

    conn.commit()
    # conn.close()
    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return conn


def insertRow(gv, cursor, TblName=None, record=""):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    logger.info('type(record): {TYPE}'.format(TYPE=type(record)))
    EXECUTE_MANY = False
    if isinstance(record, list):
        if isinstance(record[0], list):
            nFields = len(record[0])
            EXECUTE_MANY = True
        else:
            nFields = len(record)   # TESTED OK
    else:
        print ("\n\nAttesa LIST per i vari campi\n\n")
        return 1

    logger.info('nFields: {NFIELDS}'.format(NFIELDS=nFields))
    fields = '?'
    for inx in range(1, nFields):
        fields += ',?'


    logger.info('Fields: {FIELDS}'.format(FIELDS=fields))
    logger.info('EXECUTE_MANY: {0}'.format(EXECUTE_MANY))
    #@TODO: Devo completare la scrittura su DB .
    # InsertCommand = 'INSERT INTO {TABLE} VALUES ({FIELDS})'.format(TABLE=TblName, FIELDS=fields)
    InsertCommand = 'INSERT  OR IGNORE INTO {TABLE} VALUES ({FIELDS})'.format(TABLE=TblName, FIELDS=fields)
    logger.info (InsertCommand)

    try:
        if EXECUTE_MANY:
            cursor.executemany(InsertCommand, record)
        else:
            cursor.execute(InsertCommand, record)
    except (sqlite3.OperationalError) as why:
        gv.LN.exit(gv, 1002, str(why), printStack=True)


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return
