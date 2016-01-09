#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-


def getTableInfo(gv, cur, TblName):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))

    logger.info('reading Table: [{TABLE}]'.format(TABLE=TblName))

    # Retrieve column information
    # Every column will be represented by a tuple with the following attributes:
    # (id, name, type, notnull, default_value, primary_key)
    cur.execute('PRAGMA TABLE_INFO({TABLE})'.format(TABLE=TblName))

    # collect names in a list
    names = [tup[1] for tup in cur.fetchall()]
    # print(names)
    return names
    # e.g., ['id', 'date', 'time', 'date_time']
