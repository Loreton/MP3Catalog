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



def DictToList(myDict, myDictTYPES=[], line=[], level=0):
    global retLIST

    for key, val in myDict.items():                  # per tutte le chiavi del dict2
        valType = type(val)                            # otteniamo il TYPE

            # - Se è un DICT iteriamo
        if valType in myDictTYPES:
            print ('{0}{1}'.format(level*' ', key))
            appoLine = DictToList(val, myDictTYPES=myDictTYPES, line=line, level=level+1)    # in questo caso il return value non mi interessa

            # assumiamo di aver raggiunto l'ultimo livello del dict
        else:
            pass


    return retLIST


def print_dict(dictionary, ident = '', braces=1):
    """ Recursively prints nested dictionaries."""

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print ('%s%s%s%s' %(ident,braces*'[',key,braces*']'))
            print_dict(value, ident+'  ', braces+1)
        else:
            print (ident+'%s = %s' %(key, value))


def getValues(myDict):

    line = []
    for key, val in myDict.items():                  # per tutte le chiavi del dict2
        valType = type(val)                            # otteniamo il TYPE

        if valType in [str, bool, float, int]:
            line.append(val)

            # - Se è una LIST copiamo valore per valore
        elif valType in [list, tuple]:
            for item in val:                    # - cerchiamo l'item nella lista1.
                line.append(item)

        else:
            print (valType, '... must be impmelented' )

    return line


if __name__ == '__main__':

    example_dict = { 'key1' : 'value1',
                     'key2' : 'value2',
                     'key3' : { 'key3a': 'value3a' },
                     'key4' : { 'key4a': { 'key4aa': 'value4aa',
                                           'key4ab': 'value4ab',
                                           'key4ac': 'value4ac'},
                                'key4b': 'value4b'}
                   }

    print_dict(example_dict)

