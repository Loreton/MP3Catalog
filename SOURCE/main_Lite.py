#!/usr/bin/env python3
#
#-*- coding: iso-8859-1 -*-
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys; sys.dont_write_bytecode = True
import os

import codecs
################################################################################
# - M A I N
################################################################################

    # print ('.......TYPE01.....')
def type01(csvFile):
    row = []
    # f = codecs.open(csvFile, "r", "utf-8")
    # f = open(csvFile, 'r', encoding="ascii", errors="surrogateescape")
    f = open(csvFile, "r", encoding="latin-1")
    for line in f:
        row.append(line)
    f.close()
    # print (type(row), len(row))
    return row

    # print ('.......TYPE02.....')
def type02(csvFile):
    row = []
    # with open(csvFile, encoding='ascii', errors="surrogateescape") as f:
    with open(csvFile, 'r', encoding='latin-1') as f:
        row = f.read()
    row = row.split('\n')
    # print (type(row), len(row))

    return row

class enumerateClass1(object):
    def __init__(self, names, splitStr):
        for number, name in enumerate(names.split(splitStr)):
            setattr(self, name, number)


# ############################################
# Numbers = LnEnum('ZERO', 'ONE', 'TWO')
#   Numbers.ZERO
#   Numbers.ONE
# ############################################
def LnEnum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


if __name__ == "__main__":
    csvFile = '../data/MP3_Master_2015-08-10.csv'
    rowList = type01(csvFile)
    RECs = []
    for row in rowList:
        # print(row.strip('\n').strip())
        tokens = [token.strip() for token in row.split(';') if token]
        RECs.append(tokens[1:]) # se il primo è vuoto

    # Mi ritrovo una lista di liste
    # Type;Author Name;Album Name;Song Name;Punteggio;Analizzata;Recomended;Loreto;Buona;Soft;Vivace;Molto Viv;Camera;Car;Lenta;Country;Strumentale;Classica;Lirica;Live;Discreta;Undefined;Avoid it;Confusionaria;Song Size;;;;
    # for
    # print(RECs, len(RECs))
    # COLS = enumerateClass1(row[0], splitStr=';')
    # COLS = LnEnum(RECs[0])
    # print (COLS.Punteggio)

    d = {
        'a':1,
        'b':2,
        'subD': {'c':3, 'd':4}
    }

    for token in RECs[0]:
        print (token)


    # COLS = enumerateClass1(RECs[0])
    # print (aa[0])

