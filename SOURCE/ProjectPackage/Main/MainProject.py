#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ....
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os
import sys
import pandas

# gv.LN.dict.printDictionaryTree(gv, gv.INI, header="Global Vars [{0}]".format(calledBy(0), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2))
# choice=gv.LN.sys.getKeyboardInput(gv, "Uscita Temporanea", validKeys="X", exitKey='XQ')
################################################################################
# - M A I N
# - Prevede:
# -  1 - Impostazioni dei path per il corretto import dei moduli personali
# -  3 - Lettura del file di configurazione applicazione (per logFile)
# -  4 - Inizializzazione del logger
# -  2 - Controllo parametri di input per capire il file di config da utilizzare
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy

    logger.info('entered - [called by:{0}]'.format(calledBy(1)))

        # =========================================================
        # * Prelievo delle informazioni di base dalla "MAIN" Section
        # =========================================================
    try:
        MainSectID       = gv.INI.configParser['MAIN']
        DBSectID         = gv.INI.dict['DB_Data']

        gv.ImportExcel   = True if MainSectID['IMPORT_FROM_EXCEL'] == 'True' else False


        gv.DB            = gv.LnClass()
        gv.DB.File       = os.path.abspath(os.path.join(gv.MAIN.mainDataDIR, DBSectID['DBFile']))

        # gv.LN.dict.printDictionaryTree(gv, gv, header="MainVars Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)

    except Exception as why:
        gv.LN.sys.exit(gv, 1001, "Chiave non trovata: {0} nel file.ini".format(str(why)))

    if gv.ImportExcel:
        csvData = gv.Prj.excel.readExcelData(gv)

        print (len(csvData))

    gv.LN.sys.exit(gv, 9999, "Uscita temporanes", printStack=True)


    createTables(gv, csvData)

        # -----------------------------------
        # - Connecting to the database file
        # -----------------------------------
    dbMP3 = gv.Prj.sql.open(gv, gv.DB.File, create=False, printVersion=True)
    cur = dbMP3.cursor()

        # prtiamo i record in una LIST
    RECs = gv.Prj.sql.readTable(gv, cur, 'LoretoMP3')
    print (len(RECs))


    dbMP3.commit()
    dbMP3.close()
    gv.LN.sys.exit(gv, 9999, "Uscita temporanes", printStack=True)

    DB = gv.Prj.sql.createTable(gv, gv.DB.File, create=True, TblName=gv.DB.TableName, script=gv.DB.TableCreationScript)
    cur = DB.cursor()
    rCode = gv.Prj.sql.insertRow(gv, cur, TblName=gv.DB.TableName, record=newLIST)
    DB.commit()
    DB.close()
    # choice=gv.LN.sys.getKeyboardInput(gv, "Continue to create DB", validKeys="c", exitKey='XQ')





#############################################
# createTables(gv)
#############################################
def createTables(gv):
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






