#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

def DictToList(myDict, myDictTYPES=[], keyList=[], level=0, fPRINT=False):
        # ----------------------------------------------------
        # - creiamo una lista che contiene:
        # -    [level - keyName ]
        # ----------------------------------------------------
    for key, val in myDict.items():                  # per tutte le chiavi del dict2
        valType = type(val)                            # otteniamo il TYPE
            # - Se è un DICT iteriamo
        if valType in myDictTYPES:
            entry = '{0} - {1}{2}'.format(level, level*' '*4, key)
            keyList.append(entry) #  ottendo una lista di tutte le entry
            if fPRINT: print (entry)
            DictToList(val, myDictTYPES=myDictTYPES, keyList=keyList, level=level+1, fPRINT=fPRINT)    # in questo caso il return value non mi interessa

            # assumiamo di aver raggiunto l'ultimo livello del dict
        else:
            pass

    if not level == 0:
        return

        # ----------------------------------------------------
        # - siamo alla fine della recursività
        # - lavorando sul livello cerchiamo di costruire
        # - una lista di liste ...
        # - ... una lista per ogni path
        # ----------------------------------------------------
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




def printDictValues(myDict, pointer, myDictTYPES):
    level = 0
    myTAB=' '*4
    baseStartValue = 52
    for key in pointer:
        myDict = myDict[key]
        thisTYPE = str(type(myDict)).split("'")[1][-6:]
        if "DotMap" in thisTYPE: thisTYPE = 'LnDict'
        line = '[{LVL:2}] - {TYPE:<8}- {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=thisTYPE, KEY=key)
        print (line)
        level += 1

    for key, val in myDict.items():
        if key == '_myDictTYPES': continue
        if not type(val) in myDictTYPES:    # ignoriamo le entrate che sono dictionary
            thisTYPE = str(type(val)).split("'")[1]
            line0 = '[{LVL:2}] - {TYPE:<8}- {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=thisTYPE, KEY=key)
            line = '{LINE:<{LUN}}: {VAL}'.format(LINE=line0, LUN=baseStartValue, VAL=val)
            print (line)

    print()

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

    # print_dict(example_dict)
    ret = DictToList(example_dict, myDictTYPES=[dict])
    print ()
    print ()
    for index, item in enumerate(ret):
        # print ('{0:02} - {1}'.format(index, item))
        printDictValues(example_dict, pointer=item, myDictTYPES=[dict])
        # if index >10: sys.exit()
