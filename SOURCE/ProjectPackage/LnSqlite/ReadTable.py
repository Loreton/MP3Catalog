#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-


def readTable(gv, cur, TblName):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))

    logger.info('reading Table: [{TABLE}]'.format(TblName))

    RECs = []
    for row in cur.execute('SELECT * FROM {TABLE};'.format(TABLE=TblName)):
        RECs.append(row)


    logger.info('exiting - [called by:{CALLER}]'.format(CALLER=calledBy(1)))
    return RECs
