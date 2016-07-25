#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys



    # print ('.......readFile.....')
def readFile(csvFile):
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    f = open(csvFile, "r", encoding="latin-1")
    for line in f:
        row.append(line.strip())
    f.close()
    return row

def readType02(csvFile):
    row = []
    # with open(csvFile, encoding='ascii', errors="surrogateescape") as f:
    with open(csvFile, 'r', encoding='latin-1') as f:
        row = f.read()
    row = row.split('\n').strip()

    return row


def writeFile(outFile, data=[]):
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    f = open(outFile, "w", encoding="latin-1")
    for line in data:
        f.write(';'.join(line))
        f.write('\n')
    f.close()




