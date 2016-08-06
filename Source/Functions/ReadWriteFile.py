#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys



    # print ('.......readFile.....')
def readFile(gv, csvFile):
    logger = gv.Ln.setLogger(package=__name__, CONSOLE=gv.INPUT_PARAM.LogCONSOLE)
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    logger.debug('reading file: {0}'.format(csvFile))
    f = open(csvFile, "r", encoding="latin-1")
    for line in f:
        row.append(line.strip())
    f.close()
    logger.debug('number of lines found: {0}'.format(len(row)))
    return row

def readType02(csvFile):
    row = []
    # with open(csvFile, encoding='ascii', errors="surrogateescape") as f:
    with open(csvFile, 'r', encoding='latin-1') as f:
        row = f.read()
    row = row.split('\n').strip()

    return row


def writeFile(gv, outFile, data=[]):
    logger = gv.Ln.setLogger(package=__name__, CONSOLE=gv.INPUT_PARAM.LogCONSOLE)
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    logger.debug('writing file: {0}'.format(outFile))
    logger.debug('number of lines to write: {0}'.format(len(data)))
    f = open(outFile, "w", encoding="latin-1")
    for line in data:
        f.write(';'.join(line))
        f.write('\n')
    f.close()



