#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope: Lettura e scrittura di un file di configurazione nel formato INI
# ######################################################################################

'''
# The ast library consumes a lot of memory and is slower than json.
def toDict(gv, string):
    import ast
    return ast.literal_eval(str)

def toYaml(gv, string):
    import yaml
    return yaml.load(str)

'''


# JSON  decoder wants double quotes around keys and values.
import json
def toJson(gv, data):
    try:
        jsonData = json.load(data)
    except ValueError as why:
        if ('Expecting property name enclosed in double quotes') in str(why):
            json_acceptable_string = data.replace("'", '"')
            jsonData = json.load(data)
        else:
            jsonData = ''

    return jsonData

