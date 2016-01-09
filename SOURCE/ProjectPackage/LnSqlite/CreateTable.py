#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-

# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

# ####################################################################################################
# Due metodi:
# ####################################################################################################
import sqlite3

    # choice=gv.LN.sys.getKeyboardInput(gv, ColNames, validKeys="c", exitKey='XQ')
def createTable(gv, DB, TblName, forceCreate=False, ColNames=None, struct=None, script=None):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))


        # -----------------------------------
        # - Creating/Connecting SQLite table
        # -----------------------------------
    logger.info('Table: {TABLE} - creation requested.'.format(TABLE=TblName))
    try:
        cursor = DB.cursor()

        if forceCreate:
            comando = 'DROP TABLE if exists     {TABLE}'.format(TABLE=TblName)
            logger.debug(comando)
            cursor.execute(comando)

        if struct:
            comando = 'CREATE TABLE if not exists {TABLE} {STRUCT}'.format(TABLE=TblName, STRUCT=struct)
            logger.debug(comando)
            cursor.executescript(comando)

        elif script:
            comando = script
            logger.debug(comando)
            cursor.executescript(comando)

        else:
            comando = 'CREATE TABLE if not exists {TABLE} ({FIELDS})'.format(TABLE=TblName, FIELDS=ColNames)
            logger.debug (comando)
            cursor.execute(comando)

    except (sqlite3.OperationalError) as why:
        print(comando)
        gv.LN.exit(gv, 1002, str(why), printStack=True)

    except Exception as why:
        gv.LN.exit(gv, 1001, str(why), printStack=True)

    DB.commit()
    logger.info('Table: {TABLE} - successful created.'.format(TABLE=TblName))
    logger.debug('exiting - [called by:{CALLER}]'.format(CALLER=calledBy(1)))
