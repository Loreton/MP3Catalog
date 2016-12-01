#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import collections

from ..LnCommon.LnColor  import LnColor
C=LnColor()

# #######################################################
# # Ritorna una lista che contiene
# # l'alberatura delle key di un dictionary
# #    [level - keyName ]
# #######################################################
def KeyTree(myDict, myDictTYPES=[], keyList=[], level=0, fPRINT=False):
    ''' RECURSIVE '''

    if level > 100:   # per sicurezza
        import sys
        sys.exit()

    for key, val in myDict.items():                  # per tutte le chiavi del dict2
        valType = type(val)                            # otteniamo il TYPE

            # - Se è un DICT iteriamo
        if valType in myDictTYPES:
            entry = '{0} - {1}{2}'.format(level, level*' '*4, key)
            keyList.append(entry) #  ottendo una lista di tutte le entry
            if fPRINT: print (entry)
            KeyTree(val, myDictTYPES=myDictTYPES, keyList=keyList, level=level+1, fPRINT=fPRINT)    # in questo caso il return value non mi interessa

            # assumiamo di aver raggiunto l'ultimo livello del dict
        else:
            pass

    if not level == 0:
        return


    return keyList


# #######################################################
# # Ritorna una lista che contiene una lista di liste.
# #    [keya, keya1, keya2]
# #    [keyb, keyb1, keyb2]
# #    [.....]
# #######################################################
def KeyList(myDict, myDictTYPES=[]):
        # Leggiamo l'l'alberatura
    keyList = KeyTree(myDict, myDictTYPES=myDictTYPES)

    prevLevel = -1
    retLIST = []
    currPTR = []

    for line in keyList:
        if line.strip() == '':  continue
        level, item = line.split('-', 1)
        level = int(level.strip())
        item  = item.strip()

        if level == 0:        # siamo sulla root
            if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # salviamo il precedente
            currPTR = [item]
            prevLevel = 0

        elif level > prevLevel:    # andiamo in basso nella struttura
            if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # salviamo il precedente
            currPTR.append(item)
            prevLevel = level

        elif level == prevLevel:   # vuol dire che stiamo risalendo nella struttura
            if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # salviamo il precedente
            delta = 1
            currPTR = currPTR[:-delta]  # saliamo di un livello
            currPTR.append(item)    # aggiungiamo il current item

        elif level < prevLevel:   # vuol dire che stiamo risalendo nella struttura
            delta = prevLevel-level + 1
            if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # salviamo il precedente
            currPTR = currPTR[:-delta]  # saliamo di due livelli
            currPTR.append(item)    # aggiungiamo il current item
            prevLevel = level

    if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # last entry
    retLIST.append([]) # inserisci la root
    return retLIST






# #######################################################
# # Stampa i soli valori contenuti in un ramo, indicato
# #  da dotQualifers, partendo dal dict myDictRoot
# #######################################################
def PrintValue_(mainRootDict, listOfQualifiers, myDictTYPES, fPRINT=True):
    rootDict = mainRootDict
    level = 0
    myTAB=' '*4
    baseStartValue = 52
    for key in listOfQualifiers:
        rootDict = rootDict[key]
        thisTYPE = str(type(rootDict)).split("'")[1][-6:]
        if "DotMap" in thisTYPE: thisTYPE = 'LnDict'
        if fPRINT:
            line = '[{LVL:2}] - {TYPE:<8}- {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=thisTYPE, KEY=key)
            C.printYellowH(line, tab=4)
        level += 1

        # - dict forzato nell'ordine di immissione
    retValue = collections.OrderedDict()
    for key, val in rootDict.items():
        if key == '_myDictTYPES': continue
        if not type(val) in myDictTYPES:    # ignoriamo le entrate che sono dictionary
            retValue[key] = val
            if fPRINT:
                thisTYPE = str(type(val)).split("'")[1]
                line0 = '[{LVL:2}] - {TYPE:<8}- {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=thisTYPE, KEY=key)
                line  = '{LINE:<{LUN}}: {VAL}'.format(LINE=line0, LUN=baseStartValue, VAL=val)
                C.printGreenH(line, tab=4)


    if fPRINT: print()
    return retValue




# #######################################################
# # Stampa l'alberatura di un dict: mainDictRoot
# #######################################################
def PrintTree_(mainRootDict, myDictTYPES):
    keyList = KeyList(mainRootDict, myDictTYPES=myDictTYPES)

    for listOfQualifiers in keyList:
        PrintValue(mainRootDict, listOfQualifiers, myDictTYPES)









































# #######################################################
# # Ritorna una lista che contiene
# # l'alberatura delle key di un dictionary
# #    [level - keyName ]
# #######################################################
DICT_LINE   = C.printCyanH

VALUE_LINE  = C.printYellow
VALUE_LINE  = C.printCyan

VALUE_DATA  = C.printGreenH

def PrintTree(myDict, myDictTYPES=[], keyList=[], level=0, fPRINT=False, fEXIT=False):
    ''' RECURSIVE '''

    if level > 100:   # per sicurezza
        import sys
        sys.exit()

    myTAB=' '*4
    for key, val in sorted(myDict.items()):                  # per tutte le chiavi del dict2
        if key == '_myDictTYPES': continue
            # - Se è un DICT iteriamo
        if type(val) in myDictTYPES:
            thisTYPE = str(type(val)).split("'")[1][-6:]
            if "DotMap" in thisTYPE: thisTYPE = 'LnDict'
            line0 = '[{LVL:2}] {TYPE:<8} {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=thisTYPE, KEY=key)
            DICT_LINE(line0, tab=4)
            PrintTree(val, myDictTYPES=myDictTYPES, keyList=keyList, level=level+1, fPRINT=fPRINT)    # in questo caso il return value non mi interessa

        else:
            _PrintValue(key, val, level, myDictTYPES, fPRINT=True)

    if not level == 0:
        print()
        return

    if fEXIT:
        import sys
        sys.exit()
    return keyList

# #######################################################
# # Stampa i soli valori contenuti in un ramo, indicato
# #  da dotQualifers, partendo dal dict myDictRoot
# #######################################################
def _PrintValue(key, value, level, myDictTYPES, fPRINT=True):

    # level = 0
    myTAB=' '*4
        # - dict forzato nell'ordine di immissione

    retValue  = collections.OrderedDict()
    valueTYPE = str(type(value)).split("'")[1]
    listOfValue = []

    # ------------------------------
    # - valutazione del valore
    # ------------------------------

    if valueTYPE == 'str':
        s = value
        if s.find('\n') >= 0:
            listOfValue.extend(s.split('\n'))
        elif s.find(';') >= 0:
            listOfValue.extend(s.split(';'))
        else:
            STEP = 60
            while s:
                listOfValue.append(s[:STEP])
                s = s[STEP:]

    elif valueTYPE == 'list':
        listOfValue.append('[')
            # indentiamo leggermete i valori
        x = ['  ' + item for item in value]
        listOfValue.extend(x)
        listOfValue.append(']')

    else:
        listOfValue.append(value)



    # =========================================
    # = P R I N T
    # =========================================
        # - print della riga con la key a lunghezza fissa baseStartValue
    baseStartValue = 52
    line0 = '[{LVL:2}] {TYPE:<8} {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=valueTYPE, KEY=key)
    line0 = line0.ljust(baseStartValue)
    # C.printYellowH(line0, tab=4, end='')
    VALUE_LINE(line0, tab=4, end='')

        # - aggiungiamo i ':' prima del valore
    VALUE_DATA (': ', end='')

        # - print del valore della prima entry della lista
    line  = '{VAL}'.format(VAL=listOfValue[0])
    VALUE_DATA(line)

        # - print delle altre righe se presenti
    for line in listOfValue[1:]:
        line  = '{LINE:<{LUN}}  {VAL}'.format(LINE=' ', LUN=baseStartValue, VAL=line)
        VALUE_DATA(line, tab=4)
    else:
        retValue[key] = value




if __name__ == '__main__':

    example_dict = { 'key1' : 'value1',
                     'key2' : 'value2',
                     'key3' : { 'key3a': 'value3a' },
                     'key4' : {
                                'key4b': 'value4b',

                                'key4a':    {
                                                'key4aa': 'value4aa',
                                                'key4ab': 'value4ab',
                                                'key4ac': 'value4ac'
                                            },

                                'key4c' :   {
                                                'key4ca': 'value4ca'
                                            },
                            }
                    }




    # keyTree = gv.song.dict.KeyTree(fPRINT=False)
    # for line in keyTree: print(line)

    # keyList = gv.song.dict.KeyList()
    # for line in keyList: print(line)

    # ptrDict = gv.song.dict.Ptr(['Bambini', "Canzoni sotto l'albero"])
    # ptrDict.PrintTree()

    # gv.song.dict.PrintTree(listOfQualifiers=['Bambini', "Canzoni sotto l'albero", 'Varie', 'Alla scoperta di Babbo NATALE'])