#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

# unicode tips https://www.safaribooksonline.com/library/view/fluent-python/9781491946237/ch04.html

# import os, sys

from ..LnCommon.LnLogger import SetLogger

def readTextFile(inputFname, encoding='utf-8'):
    logger = SetLogger(package=__name__)
    row = []
    logger.debug('reading file: {0}'.format(inputFname))
    try:
        f = open(inputFname, "r", encoding=encoding)
    except (Exception) as why:
        gv.Ln.Exit(1, str(why), printStack=True)

    for line in f:
        row.append(line.strip())
    f.close()

    logger.debug('number of lines read: {0}'.format(len(row)))
    return row

def readTextFile02(inputFname, encoding='utf-8'):
    row = []
    with open(inputFname, 'r', encoding=encoding) as f:
        row = f.read()
    row = row.split('\n').strip()

    return row


def writeTextFile(outFname, data=[], encoding='utf-8'):
    logger = SetLogger(package=__name__)
    logger.debug('writing file:             {0}'.format(outFname))
    logger.debug('number of lines to write: {0}'.format(len(data)))

    f = open(outFname, "w", encoding=encoding)
    for line in data:
        if isinstance(line, list):
            # converte all items to string
            lineStr = [str(item) for item in line] # potrebbe dare errore se qualce item non è stringa
            f.write(';'.join(lineStr))
        else:
            f.write(line)
        f.write('\n')
    f.close()




