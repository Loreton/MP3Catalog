#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ....
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os
import sys

# gv.LN.dict.printDictionaryTree(gv, gv.INI, header="Global Vars [{0}]".format(calledBy(0), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2))
# choice=gv.LN.sys.getKeyboardInput(gv, "Uscita Temporanea", validKeys="X", exitKey='XQ')
################################################################################
# - M A I N
################################################################################
def Main(gv):
    logger      = gv.LN.setLogger(gv, __name__, LnConsole=False)
    calledBy    = gv.LN.sys.calledBy

    logger.info('entered - [called by:{0}]'.format(calledBy(1)))

        # =========================================================
        # * Prelievo delle informazioni di base dalla "MAIN" Section
        # =========================================================
    try:
        # MainSectID       = gv.INI.configParser['MAIN']
        DBSectID         = gv.INI.dict['DB_Tables']

        gv.ImportExcel   = True if DBSectID['IMPORT_FROM_EXCEL'] == 'True' else False



        gv.DB               = gv.dotMap()
        File                = DBSectID['DBFile'].split(',')
        gv.DB.File          = os.path.abspath(os.path.join(gv.MAIN.mainDataDIR, File[0].strip()))
        gv.DB.FileCreation  = True if File[1].strip().lower() == 'forcecreate' else False


    except Exception as why:
        gv.LN.sys.exit(gv, 1001, "Chiave non trovata: {0} nel file.ini".format(str(why)))

    gv.LN.dict.printDictionaryTree(gv, gv, header="MainVars Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TVL', lTAB=' '*4, listInLine=2)

        # -----------------------------------
        # - Importing Excel File if required
        # -----------------------------------
    csvData = gv.Prj.excel.readExcelData(gv) if gv.ImportExcel else []


        # -----------------------------------
        # - Connecting to the database file
        # -----------------------------------
    dbMP3 = gv.Prj.sql.open(gv, gv.DB.File, create=gv.DB.FileCreation, printVersion=False)
    cur   = dbMP3.cursor()

        # -----------------------------------
        # - Prepare Tables
        # -----------------------------------
    gv.Prj.funcs.prepareTables(gv, dbMP3, DBSectID, csvData)

    gv.Table.MP3.colNames     = gv.Prj.sql.getTableInfo(gv, cur, gv.Table.MP3.name)
    gv.Table.Weight.colNames  = gv.Prj.sql.getTableInfo(gv, cur, gv.Table.Weight.name)
    gv.Table.Percent.colNames = gv.Prj.sql.getTableInfo(gv, cur, gv.Table.Percent.name)
    gv.Table.Percent.val      = gv.Prj.sql.readTable(gv, cur, gv.Table.Percent.name)



        # -----------------------------------------------------------
        # - Tentativo di creare le altre tabelle in modo dinamico
        # -     senza usare il file.ini
        # - Funziona ma al momento accantonato
        # -----------------------------------------------------------
    gv.Prj.funcs.createPercentTable(gv, DB=dbMP3, iniSectID=DBSectID, newTblPfx='Table.Percent', mainTable=gv.Table.MP3.name)

    dbMP3.commit()
    dbMP3.close()
    # gv.Prj.extract.PercentNormalization(gv, xxxDict)
    # gv.Prj.extract.PercentNormalization(gv, gv.Table.Percent.val)
    # gv.LN.dict.printDictionaryTree(gv, gv.Table.Percent, header="Global Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)

    gv.LN.sys.exit(gv, 9999, "Uscita temporanes", printStack=False)

    RECs = gv.Prj.sql.readTable(gv, cur, 'LoretoMP3')
    print (len(RECs))
