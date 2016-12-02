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
def Main(gv, action):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()
    # gv.data = gv.Ln.LnDict()

    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()

    DBdict            = gv.Ln.LnDict()

    DBdict.filename   = os.path.abspath(os.path.join(gv.Prj.dataDIR, gv.ini.SqLite.DB_filename))
    DBdict.filecreate = True if gv.ini.SqLite.DB_filecreate.lower() == 'true' else False
    DB         = gv.Ln.LnSqLite(DBdict.filename, DBdict.filecreate)
    # gv.ini.SqLite.PrintTree()
    # DBdict      = gv.ini.SqLite
    # DBdict.songTable        = gv.Ln.LnDict()
    DBdict.songTableName   = gv.ini.SqLite['songTable.name']
    DBdict.songTableCreate = True if gv.ini.SqLite['songTable.forcecreate'].lower() == 'true' else False
    DBdict.songTableStruct = gv.ini.SqLite['songTable.struct']


    DB.CreateTable(DBdict.songTableName, forceCreate=DBdict.songTableCreate, struct=DBdict.songTableStruct, script=None, fCOMMIT=False)

    DBdict.PrintTree(fEXIT=True)
    DB.createTable = gv.Prj.sql.createTable(gv, gv.DB.File, create=True, TblName=tableName, script=val)
    if midName == 'MP3':
        cur = DB.cursor()
        csvData = readExcelData(gv)
        rCode = gv.Prj.sql.insertRow(gv, cur, TblName=tableName, record=csvData)
        DB.commit()
        DB.close()


