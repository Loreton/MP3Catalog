#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-

# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

# ####################################################################################################
# Due metodi:
# ####################################################################################################
import sqlite3

    # choice=gv.LN.sys.getKeyboardInput(gv, ColNames, validKeys="c", exitKey='XQ')
def createTable(gv, DB, TblName=None, forceCreate=False, ColNames=None, script=None):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))


        # -----------------------------------
        # - Creating/Connecting SQLite table
        # -----------------------------------
    try:
        cursor = DB.cursor()

        if forceCreate:
            comando = 'DROP TABLE if exists     {TABLE}'.format(TABLE=TblName)
            logger.info(comando)
            cursor.execute(comando)

        if script:
            comando = script
            logger.info(comando)
            cursor.executescript(comando)

        else:
            comando = 'CREATE TABLE if not exists {TABLE} ({FIELDS})'.format(TABLE=TblName, FIELDS=ColNames)
            logger.info (comando)
            cursor.execute(comando)

    except (sqlite3.OperationalError) as why:
        logger.error ('ERROR', str(why))

    except Exception as why:
        gv.LN.exit(gv, 1001, str(why), printStack=True)

    DB.commit()
    logger.info('exiting - [called by:{CALLER}]'.format(CALLER=calledBy(1)))
