#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys



    # print ('.......readFile.....')
def readFile(gv, csvFile, encoding='utf-8'):
    logger = gv.Ln.SetLogger(package=__name__)
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    logger.debug('reading file: {0}'.format(csvFile))
    try:
        # f = open(csvFile, "r", encoding="latin-1")
        f = open(csvFile, "r", encoding=encoding)
    except (Exception) as why:
        gv.Ln.Exit(1, str(why), printStack=True)

    for line in f:
        row.append(line.strip())
    f.close()

    logger.debug('number of lines found: {0}'.format(len(row)))
    return row

def readType02(csvFile, encoding='utf-8'):
    row = []
    # with open(csvFile, encoding='ascii', errors="surrogateescape") as f:
    # with open(csvFile, 'r', encoding='latin-1') as f:
    with open(csvFile, 'r', encoding=encoding) as f:
        row = f.read()
    row = row.split('\n').strip()

    return row


def writeFile(gv, outFile, data=[], encoding='utf-8'):
    logger = gv.Ln.SetLogger(package=__name__)
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    logger.debug('writing file: {0}'.format(outFile))
    logger.debug('number of lines to write: {0}'.format(len(data)))
    # f = open(outFile, "w", encoding="latin-1")
    f = open(outFile, "w", encoding=encoding)
    for line in data:
        if isinstance(line, list):
            # converte all items to string
            lineStr = [str(item) for item in line]
            f.write(';'.join(lineStr)) # potrebbe dare errore se qualce item non è stringa
        else:
            f.write(line)
        f.write('\n')
    f.close()




