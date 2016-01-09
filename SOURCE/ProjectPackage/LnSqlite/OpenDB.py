#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-

# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html
# http://zetcode.com/db/sqlitepythontutorial/

import os
import sqlite3, pandas

def open(gv, DBFile, create=False, printVersion=False):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))

    if create:
        if os.path.isfile(DBFile):
            msg = "\n   DBFile already exists: {DBFILE}\n   Press 'd' top destroy".format(DBFILE=DBFile)
            choice=gv.LN.sys.getKeyboardInput(gv, msg, validKeys="dD", exitKey='XQ')
            if choice in 'dD':
                logger.info('removing DBFile {DBFILE}]'.format(DBFILE=DBFile))
                os.remove(DBFile)


        # -----------------------------------
        # - Connecting to the database file
        # - Il file viene creato se non esiste
        # -----------------------------------
    conn = sqlite3.connect(DBFile)
    cur = conn.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    version = cur.fetchone()
    logger.info ("SQLite version: {VERSION}".format(VERSION=version))

    if printVersion:
        print ("SQLite version: {VERSION}".format(VERSION=version))

    logger.debug('exiting - [called by:{CALLER}]'.format(CALLER=calledBy(1)))
    return conn
