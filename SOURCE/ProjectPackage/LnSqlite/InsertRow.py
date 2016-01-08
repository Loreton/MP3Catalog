#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-

import sqlite3


###########################################################
# - Inserisce una riga in una tabella.
# - Se record=LIST di LIST allora fa una massInsert/executeMany
###########################################################
def insertRow(gv, DB, TblName=None, record=""):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))

    logger.info('Adding record to Table: {TABLE}'.format(TABLE=TblName))
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


    logger.info('Fields:       {FIELDS}'.format(FIELDS=fields))
    logger.info('EXECUTE_MANY: {FLAG}'.format(FLAG=EXECUTE_MANY))
    InsertCommand = 'INSERT  OR IGNORE INTO {TABLE} VALUES ({FIELDS})'.format(TABLE=TblName, FIELDS=fields)
    logger.info (InsertCommand)

    try:
        cursor = DB.cursor()
        if EXECUTE_MANY:
            cursor.executemany(InsertCommand, record)
        else:
            cursor.execute(InsertCommand, record)

    except (sqlite3.OperationalError) as why:
        gv.LN.exit(gv, 1002, str(why), printStack=True)


    DB.commit()
    logger.info('exiting - [called by:{CALLER}]'.format(CALLER=calledBy(1)))
