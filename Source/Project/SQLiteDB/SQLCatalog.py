#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import ast




################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def ReadSqlLiteDB(gv, iniDict):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()

    DB          = gv.Ln.LnDict()
    DB.filename = iniDict.filename

    '''
    DBdict = gv.DB.IniSectID
    for key, val in DBdict.items():
        # print (key)
        if key.startswith('Table.'):
            (left, midName, right) = key.split('.')
            if right == 'script':
                varName = '{LEFT}.{MID}.name'.format(LEFT=left, MID=midName)
                tableName = DBdict[varName]
                DB = gv.Prj.sql.createTable(gv, gv.DB.File, create=True, TblName=tableName, script=val)
                if midName == 'MP3':
                    cur = DB.cursor()
                    csvData = readExcelData(gv)
                    rCode = gv.Prj.sql.insertRow(gv, cur, TblName=tableName, record=csvData)
                    DB.commit()
                    DB.close()
    '''



