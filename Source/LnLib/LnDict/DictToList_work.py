# #########################################################################################
# = Merge di due Dictionary.
# = I valori del secondo sovrascrivono le chiavi del primo
# = Se non si vuole ricoprire il primo dict bisogna preventivamente averne fatto una copia
# =   dictCopia = dict.copy()
# #########################################################################################
# DictTYPES=None
retLIST = []
def DictToList_(myDict, level=0, myDictTYPES=[], line=[]):
    global retLIST

    # line = []
    for key, val in myDict.items():                  # per tutte le chiavi del dict2
        valType = type(val)                            # otteniamo il TYPE
            # - Se è un DICT iteriamo
        if valType in myDictTYPES:
            line.append(key)
            # print ('dict1.{LVL} - {LINE}'.format(LVL=level, LINE=line))
            line = DictToList(val, level=level+1, myDictTYPES=myDictTYPES, line=line)    # in questo caso il return value non mi interessa
            #line.extend(appoLine)
            retLIST.append(line)
            # print ("dict2.{LVL} - {LINE}".format(LVL=level, LINE=line))
            line = []

        elif valType in [str, bool, float, int]:
            line.append(val)
            # print ('str.{LVL} - {LINE}'.format(LVL=level, LINE=line))

            # - Se è una LIST copiamo valore per valore
        elif valType in [list, tuple]:
            for item in val:                    # - cerchiamo l'item nella lista1.
                line.append(item)
            # print ('list.{LVL} - {LINE}'.format(LVL=level, LINE=line))
        else:
            print ('pass.{LVL} - {LINE}'.format(LVL=level, LINE=line))
            pass


    # print ('exit.{LVL} - {LINE}'.format(LVL=level, LINE=line))
    if level == 0:
        print("dictionaries - completed")
        return retLIST
    else:
        return line


retLIST = []
import sys
# - ritorna la struttura di tutti i dict
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
        # - viene eseguito solo alla fine della recursività
        # - lavorando sul livello cerchiamo di costruire
        # - una lista per ogni path
        # ----------------------------------------------------
    prevLevel = -1
    retLIST = []
    currPTR = []

    for line in keyList:
        if line.strip() == '':  continue
        # print (line)
        level, item = line.split('-', 1)
        level = int(level.strip())
        item = item.strip()

        # print (level, item)

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
    retLIST.append([])
    return retLIST




def printDictValues(myDict, pointer, myDictTYPES):
    level = 0
    MAX_LEVEL=0
    myTAB=' '*4
    BLANK=' '
    baseStartValue = 52
    for key in pointer:
        myDict = myDict[key]
        thisTYPE = str(type(myDict)).split("'")[1][-6:]
        if "DotMap" in thisTYPE: thisTYPE = 'LnDict'
        line = '[{LVL:2}] - {TYPE:<8}- {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=thisTYPE, KEY=key)
        print (line)
        level += 1

    # level += 1
    MAX_LEVEL = level
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
