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
        DBSectID         = gv.INI.dict['DB_Tables']

        gv.ImportExcel   = True if MainSectID['IMPORT_FROM_EXCEL'] == 'True' else False
        gv.preLoadTables = True if DBSectID['PreLoadTables'] == 'True' else False


        gv.DB            = gv.LnClass()
        gv.DB.File       = os.path.abspath(os.path.join(gv.MAIN.mainDataDIR, DBSectID['DBFile']))

        # gv.LN.dict.printDictionaryTree(gv, gv, header="MainVars Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)

    except Exception as why:
        gv.LN.sys.exit(gv, 1001, "Chiave non trovata: {0} nel file.ini".format(str(why)))


        # -----------------------------------
        # - Importing Excel File if required
        # -----------------------------------
    csvData = gv.Prj.excel.readExcelData(gv) if gv.ImportExcel else []


        # -----------------------------------
        # - Connecting to the database file
        # -----------------------------------
    dbMP3 = gv.Prj.sql.open(gv, gv.DB.File, create=False, printVersion=True)
    cur   = dbMP3.cursor()

        # -----------------------------------
        # - Creating Tables
        # -----------------------------------
    createTables(gv, dbMP3, DBSectID, csvData)


        # -----------------------------------
        # - preLoadTables Tables (solo se serve)
        # -----------------------------------
    # if gv.preLoadTables:
    #     preLoadTables(gv, dbMP3, DBSectID)


    gv.LN.sys.exit(gv, 9999, "Uscita temporanes", printStack=True)

    RECs = gv.Prj.sql.readTable(gv, cur, 'LoretoMP3')
    print (len(RECs))


    dbMP3.commit()
    dbMP3.close()

    DB = gv.Prj.sql.createTable(gv, gv.DB.File, create=True, TblName=gv.DB.TableName, script=gv.DB.TableCreationScript)
    cur = DB.cursor()
    rCode = gv.Prj.sql.insertRow(gv, cur, TblName=gv.DB.TableName, record=newLIST)
    DB.commit()
    DB.close()
    # choice=gv.LN.sys.getKeyboardInput(gv, "Continue to create DB", validKeys="c", exitKey='XQ')





#####################################################################
# - createTables(gv)
# - Analizza la sezione del DB_Tables e cerca di crere le tabelle
#
#    Table.MP3.name         = LoretoMP3
#    Table.MP3.forceCreate  = False
#    Table.MP3.script       = create table if not exists ${Table.MP3.name} (
#                                "Type"              STRING  NOT NULL,
#                                "Author Name"       STRING  NOT NULL
#                            )
#####################################################################
def createTables(gv, DB, DBSectID, csvData):
    for key, val in DBSectID.items():
        # print (key)
        if key.startswith('Table.') and key.endswith('.script'):
            (left, midName, right) = key.split('.')
            keyName     = '{LEFT}.{MID}.name'.format(LEFT=left, MID=midName)
            tableName   = DBSectID[keyName]
            keyName     = '{LEFT}.{MID}.forceCreate'.format(LEFT=left, MID=midName)
            forceCreate = True if DBSectID[keyName] == 'True' else False

            gv.Prj.sql.createTable(gv, DB, forceCreate=forceCreate, TblName=tableName, script=val)
            if midName == 'MP3' and not csvData == []:
                rCode = gv.Prj.sql.insertRow(gv, DB, TblName=tableName, record=csvData)

            if gv.preLoadTables:
                keyName = '{LEFT}.{MID}.data'.format(LEFT=left, MID=midName)
                data = DBSectID.get(keyName)
                if data:
                    preLoadTables(gv, DB, tableName, data)



def preLoadTables(gv, DB, tableName, inpData):
    print ('working on ' + tableName)
    data = []
    for x in inpData.split('\n'):
        if x:
            Vals = x.split(':')
            line = []
            for val in Vals:
                line.append(val.strip())
            data.append(line)
    # print (data)
    gv.Prj.sql.insertRow(gv, DB, TblName=tableName, record=data)

