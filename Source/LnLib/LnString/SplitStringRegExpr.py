#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
# -O Optimize e non scrive il __debug__

import types
# from   types import *                     # per StringType, etc


# #################################################################
# #  link:  http://stackoverflow.com/questions/4998629/python-split-string-with-multiple-delimiters
# #  splitString with multiple delimiters
# #  delimiters:    LIST of delimiters
# #################################################################

def splitStringRE(string, delimiters, maxsplit=0):
    import re

    if isinstance(delimiters, str):
    # if type(delimiters) in [types.StringType]:
        delimiters = [delimiters]

    regexPattern = '|'.join(map(re.escape, delimiters))
    # re.compile(regexPattern) per velocizzare ma solo se il pattern è sempre lo stesso

    return re.split(regexPattern, string, maxsplit)


# Se non si vuole richiamare la funzione si può utilizzare
#       import re
#       re.split('[:= ;]', string, maxsplit)

# #################################################################
# #  splitString Single delimeiter - Forse è meglio l'altra
# #     link: http://docs.python.org/2/library/re.html#re.RegexObject.split
# #################################################################

def splitStringSD(string, delimiter, maxsplit=0):
    import re
    m = re.search(delimiter, string)
    return (string[:m.start()], string[m.end():])