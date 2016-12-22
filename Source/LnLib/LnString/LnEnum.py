#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:
# ######################################################################################
from  collections import OrderedDict as oDict

def LnEnum(data, myDict=oDict, weighted=False):
    ENUM = myDict()
    for index, name in enumerate(data):
        itemName = name.strip().replace(' ', '_')
        if weighted:
                # - ritorna il nome con una sequenza binaria
            ENUM[itemName] = 2**index
        else:
                # - ritorna il nome con una sequenza unitaria
            ENUM[itemName] = index

    return ENUM



