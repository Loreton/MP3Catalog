#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-
# dictTYPES = [dict, configparser.ConfigParser, configparser.SectionProxy, gv.Prj.LnClass, gv.gv.Ln.LnClass, collections.OrderedDict]
#
# Scope:  Funzioni per operare sul python dictionary
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import sys, os
import types
import collections, configparser
import argparse



allDictTYPES = []
import inspect

from ..LnCommon.LnLogger import SetLogger
from ..LnCommon.LnColor  import LnColor

# #########################################################################################
# - printDictionaryTree() ordered
# - CALL: printDictionaryTree(CfgDict, MaxDeepLevel=3, values=True, lTAB=' '*12)
# - PARAMS:
# -     level:          serve per tenere traccia delle iterazioni ed anche per l'indentazione
# -     MaxDeepLevel:   Indica il numero MAX di profondità (iterazioni) da raggiungere
# -     values:         Indica se ritornare anche il valore delle keys
# -     lTAB:           Prefix a sinistra della riga
# -     retCols:         'LTV'
# -                        L  se vogliamo LevelCol
# -                        T  se vogliamo Type
# -                        V  se vogliamo Value
# -     header:
#           None  - Viene calcolato automaticamente
#           NO    - Non viene visualizzato
#           altro - Viene visualizzato ..altro
# -
# #########################################################################################

# ########################################################################
def  printDictionaryTree(gv, dictID, extDict=[], header=None, MaxDeepLevel=999, level=0, retCols='LTV', lTAB='', listInLine=5, fEXIT=False, fCONSOLE=True, stackLevel=1):
    # color = gv.Ln.Colors()
    global allDictTYPES, myDictTYPES
    myDictTYPES = []
    myDictTYPES.extend(extDict)
    if 'myDictTYPES' in gv: myDictTYPES.extend(gv.myDictTYPES)

    pyDictTYPES = [ dict,
                    configparser.ConfigParser,
                    configparser.SectionProxy,
                    collections.OrderedDict,
                    ]

    allDictTYPES.extend(pyDictTYPES)
    allDictTYPES.extend(myDictTYPES)

    lista = getDictionaryTree(dictID, MaxDeepLevel=MaxDeepLevel, level=level, retCols=retCols, listInLine=listInLine)

    caller = inspect.stack()[stackLevel]
    dummy, fileName, funcLineNO, funcName, lineCode, rest = caller
    fName       = os.path.basename( fileName.split('.')[0])
    if funcName == '<module>': funcName = '__main__'
    caller = "Called by: [{FNAME}.{FUNC}:{LINEO}]".format(FNAME=fName, FUNC=funcName, LINEO=funcLineNO)

        # ---- Cerchiamo di catturare il dictionary richiamato
        # ---- da verificare con attenzione
    dictionaryName =  (lineCode[0].split('.printDict')[0].split()[-1])
    if dictionaryName:
        header2 = "dictionary: {DICT}".format(DICT=dictionaryName)
    else:
        header2 = None


    if fEXIT and not header:
        header = True

    if not header: header = caller
    if fCONSOLE:
        print()
        LnColor.printCyan("*"*60, tab=8)
        LnColor.printCyan("*     {0}".format(header), tab=8)
        if header2: LnColor.printCyan("*     {0}".format(header2), tab=8)
        LnColor.printCyan("*"*60, tab=8)


        for line in lista:
            if not isAscii(line): line = str.encode(line, 'utf-8')
            # print("{0}{1}{2}".format(COLOR, lTAB, line))
            LnColor.printCyan(line, tab=len(lTAB))

    if fEXIT:
        print("Exiting on user request. {CALLER}".format(CALLER=caller))
        sys.exit(0)

    return lista


def isAscii(s):
    try:
        return all(ord(c) < 128 for c in s)
    except TypeError:
        return False


# #########################################################################################
# - getDictionaryTree()
# -
# - PARAMS:
# -     level:          serve per tenere traccia delle iterazioni ed abche per l'indentazione
# -     MaxDeepLevel:   Indica il numero MAX di profondità (iterazioni) da raggiungere
# -     values:         Indica se ritornare anche il valore delle keys
# -
# - RETURN: LIST of the keys with level indication:
# -            LVL TYPE       KeyName
# -            [0] dict       JbossColl
# -            [1] list           PATHS
# -            [1] str            Source System
# -            [1] str            Target System
# -            [0] int        LOG_CONSOLE
# -            [0] int        LOG_FILE
# -            [0] dict       Portit_DiscoL
# -            [1] dict           Flusso_DiscoL_With_BACKUP
# -            [2] list               PATHS
# -            [2] str                Source System
# -            [2] str                Target System
# -            [0] str        Type_of_Command
# -            [0] str        esil601
# -     Es.:
# -       [0] str          user.timezone                    : GMT+1
# -       [0] bool         javax.xml.jaxp-provider          : True
# -       [0] int          BdI.txn-status-manager.port      : 4713
# -
# - E' possibile utilizzarlo anche per leggere un modulo caricato con il comando:
# -         configFileID = loadConfigModule(Fname)
# -         CfgDict = vars(configFileID)        # con il comando vars trasformo il modulo in dictionary
# -
# -         lista = getDictionaryTree_Prev(vars(configFileID))
# -         lista = getDictionaryTree_Prev(CfgDict)
# #########################################################################################
def getDictionaryTree(dictID, MaxDeepLevel=999, level=0, retCols='LTV', listInLine=5):
    lista = []
    TabSize = 3
    if MaxDeepLevel < 0: return lista

    thisDictType = type(dictID)
    values = (True if 'V' in retCols else False)
    if not thisDictType in allDictTYPES:
        return lista

    if thisDictType in myDictTYPES:
        dictID = vars(dictID) # custom class


        # ------ Stiamo trattando un dictionary
    for key, val in sorted(dictID.items()):
            # ------------------------------------------------------------------
            # - La riga seguente serve per impedire di analizzare
            # - la variabile 'gv.myDictTYPES' in quanto darebbe errore.
            # - Tale variabile è usata solo per contenere mie classi specifiche
            # ------------------------------------------------------------------
        if key == 'myDictTYPES': continue
        if key == '_dynamicDotMap': continue

        if type(val) in myDictTYPES:
            val = vars(val)
            valueTypeStr = 'LnDict'
        else:
            valueTypeStr = str(type(val)).split("'")[1]

        valueType = type(val)
        # print('---------- valueType ------------------', valueType)
        # print('---------- valueTypeStr ---------------', valueTypeStr)
        # print('---------- key       ------------------', key)
        # print('---------- value     ------------------', val)
        if isinstance(key, str):
            if key.startswith('__') and key.endswith('__'): continue    # elimina tutti i built-in (presente in un modulo)

        if valueType == types.ModuleType:
            continue                                # elimina eventuali import (presente in un modulo)


        newLine = "{0} {1}".format(' '*level*TabSize, key)        # base della Linea
        if 'T' in retCols: newLine = "{0:<13} {1}".format(valueTypeStr, newLine)  # aggiungiamo il TYPE
        if 'L' in retCols: newLine = "[{0:2}] {1}".format(level, newLine)          # aggiungiamo il LEVEL

        if valueType in allDictTYPES:
            continue

        if values:
            if valueType in [bytes, str]:
                if val.strip() == '':
                    val = '"' + val + '"'
                val = val.replace('\n', ' ')        # vale per le righe multiline (tipo nel file.ini)
                newLine = "{0:<50}: {1}".format(newLine.rstrip(), val.strip())
                lista.append(newLine)

            elif isinstance(val, enumerate):
                lista.append("{0:<50}: [".format(newLine.rstrip()))          # Apertura LIST
                for index, name in val:
                    newLine = prepareListValueLine(name, retCols, level)
                    lista.append(newLine)

                lista.append('{0:<50}: ]'.format(' ') )                # Chiusura LIST

            elif valueTypeStr == "datetime.date":
                newLine = "{0:<50}: {1}".format(newLine.rstrip(), val)
                lista.append(newLine)

            elif valueTypeStr.endswith('.enumerateClass'):
                ENUM_SORTED_BY_VALUE = True
                lista.append("{0:<50}: [".format(newLine.rstrip()))   # Apertura LIST
                thisDICT = vars(val)                            # Devo trasformarlo in DICT per analizzarlo.
                if ENUM_SORTED_BY_VALUE:                        # print sorted by value (comodo se il valore è numerico)
                    for w in sorted(thisDICT, key=thisDICT.get, reverse=False):
                        lista.append('{0:<54}: {1:<20}.{2:2}:'.format(" ", w, thisDICT[w]))
                else:                                           # print normale
                    for key, value in sorted(thisDICT.items()):
                        lista.append('{0:<54}: {1:<20}.{2:2}:'.format(" ", key, value))
                lista.append('{0:<50}: ]'.format(' ') )                # Chiusura LIST


            elif valueType == list:
                if len(val) == 0:                                               # Enpty LIST
                    newLine = "{0:<50}: []".format(newLine.rstrip())                  # Enpty LIST
                    lista.append(newLine)

                else:
                    lista.append("{0:<50}: [".format(newLine.rstrip()) )             # Apertura LIST
                    counter = 0
                    for line in val:
                        if type(line) in allDictTYPES:            # Dictionary interno ad una LIST
                            counter += 1
                            level += 1
                            lista.append('')
                            lista.append('[{0:02}] dict-{1:02}'.format(level, counter))
                            newLista = getDictionaryTree(line, MaxDeepLevel=MaxDeepLevel-1, level=level+1, retCols=retCols)
                            lista.extend(newLista)
                            level -= 1
                            continue

                        newLine = prepareListValueLine(line, retCols, level+1)
                        lista.append(newLine)

                    newLine = prepareListValueLine(': ]', retCols, level) # Chiusura LIST
                    lista.append(newLine)
                    lista.append('')

            elif valueType in (bool, type(None), int, float):
                newLine = "{0:<50}: {1}".format(newLine.rstrip(), val)
                lista.append(newLine)

            else:
                lista.append(newLine)

        else:
            lista.append(newLine)

    if lista and lista[-1] != '':
        lista.append('')    # separator se non esiste di già


        # Analisi di tutte le chiavi che sono a livello del dictionary.
    for key, val in sorted(dictID.items()):
        valueTypeStr = str(type(val)).split("'")[1]
        valueType    = type(val)
        if   valueType in myDictTYPES: valueTypeStr = 'LnDict'
        elif valueTypeStr == 'configparser.ConfigParser': valueTypeStr = 'ConfigParser'
        elif valueTypeStr == 'configparser.SectionProxy': valueTypeStr = 'INISection'
        # elif valueTypeStr == 'collections.OrderedDict' and key == '_map':   continue
        elif valueTypeStr == 'collections.OrderedDict': valueTypeStr = 'ordDict' + key

        if isinstance(key, str):
            if key.startswith('__') and key.endswith('__'): continue    # elimina tutti i built-in (presente in un modulo)

        if valueType == types.ModuleType: continue                  # elimina eventuali import (presente in un modulo)

        if valueType in allDictTYPES:
                # ------------------------------
                # - Tentativo di allineamento
                # - Es.:
                # -    DotMap        MAIN
                # -    OrderedDict   MAIN
                # ------------------------------
            if 'T' in retCols:
                newLine = '{VALUE_TYPE:<13} {INDENT} {LINE}'.format(VALUE_TYPE=valueTypeStr, INDENT=' '*level*TabSize, LINE=key)
            else:
                newLine = '{INDENT} {LINE}'.format(INDENT=' '*level*TabSize, LINE=key)

            if 'L' in retCols: newLine = "[{LEVEL:2}] {LINE}".format(     LEVEL=level,             LINE=newLine)        # aggiungiamo il LEVEL


                # riga riguardante dotMap - Non serve! Loreto
            if key == '_map':
                level -= 1
            else:
                lista.append(newLine)

            newLista = getDictionaryTree(val, MaxDeepLevel=MaxDeepLevel-1, level=level+1, retCols=retCols)
            lista.extend(newLista)

    return lista



###################################################################
#
###################################################################
def prepareListValueLine(line, retCols, level):
    newLine = ''
    offSet = ' '*5

    valueTypeStr = str(type(line)).split("'")[1]

    if isinstance(line, str):
        if line == ': ]':
            valueTypeStr = 'endOfLIST.........'
            valueTypeStr = 'end list...'
            offSet = ''                             # per la formattazione
        elif line.endswith(': ['):
            valueTypeStr = 'startOfLIST'

    if 'T' in retCols:
        str(type(line)).split("'")[1]
        newLine = "{0:<12} {1}".format(valueTypeStr, newLine)        # aggiungiamo il TYPE
    if 'L' in retCols:
        newLine = "[{0:2}] {1}".format(level, newLine)        # aggiungiamo il LEVEL

    newLine = "{0:<49}{1} {2}".format(newLine, offSet, line)
    return newLine


if __name__ == "__main__":
    gv=''
    dictID={}
    fEXIT       = 'fEXIT'
    fEXIT       = True
    console     = 'console'
    console     = True
    pippo       = 'pippo'
    header      = 'header'
    print("fEXIT        = {0}".format(fEXIT))
    print("console      = {0}".format(console))
    print("pippo        = {0}".format(pippo))
    print("header       = {0}".format(header))
    print()
    printDictionaryTree(gv, dictID, header=header, MaxDeepLevel=999, level=0, retCols='LTV', lTAB='', listInLine=5, fEXIT=fEXIT)
