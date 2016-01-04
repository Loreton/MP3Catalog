#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ....
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os
import sys
import httplib2
import json
import xml

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


    # gv.LN.dict.printDictionaryTree(gv, gv.INI, header="Global Vars [{0}]".format(calledBy(0), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2))

        # =========================================================
        # * Prelievo delle informazioni di base dalla "MAIN" Section
        # =========================================================


    try:
        MainSectID = gv.INI.configParser['MAIN']
        gv.MainVars.excelInputFile      = os.path.abspath(os.path.join(MainSectID['excelInputFile']))
        gv.MainVars.excelOutputFile     = os.path.abspath(os.path.join(MainSectID['excelOutputFile']))
        gv.MainVars.sheetName           = MainSectID['sheetName']
        gv.MainVars.action              = MainSectID['ACTION']
        # gv.MainVars.MaxOutDirSize       = MainSectID['MaxOutDirSize']
        gv.MainVars.MaxRowsToRead       = int(MainSectID['MaxRowsToRead'])
        gv.MainVars.ExcelStartCol       = MainSectID['EXCEL_START_COLUMN']
        gv.MainVars.ExcelColNamesRow    = int(MainSectID['EXCEL_COLUMNS_NAMES_ROW'])
        gv.MainVars.ExcelfirstSongRow   = MainSectID['EXCEL_FIRST_SONG_ROW']
        gv.MainVars.ExcelLastSongRow    = MainSectID['EXCEL_LAST_SONG_ROW']

        appo                            = MainSectID['Nomi Colonne Primarie']
        gv.MainVars.PrimaryColName      = [x.strip('\n').strip() for x in appo.split('\n') if x]
        # gv.MainVars.PrimaryColName      = [x.strip('\n').strip() for x in appo.split('FIELD=') if x]
        # gv.MainVars.PrimaryColName      = appo.split('),')
        # print (type(gv.MainVars.PrimaryColName))
        # print (type(appo))
        # print (PrimaryColsStr)
        # choice=gv.LN.sys.getKeyboardInput(gv, "Uscita Temporanea", validKeys="X", exitKey='XQ')


        appo                            = MainSectID['Nomi Colonne Attributi']
        gv.MainVars.AttributeColName    = [x.strip('\n').strip() for x in appo.split('\n') if x]

        gv.DB                           = gv.LnClass()
        gv.DB.IniSectID                 = gv.INI.configParser['DB_Data']
        gv.DB.IniSectID                 = gv.INI.dict['DB_Data']
        gv.DB.File                      = gv.DB.IniSectID['DBFile']

        # gv.LN.dict.printDictionaryTree(gv, gv.DB.IniSectID, header="MainVars Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)

    except Exception as why:
        msg = "Chiave non trovata: {0} nel file.ini".format(str(why))
        gv.LN.sys.exit(gv, 1001, "Chiave non trovata: {0} nel file.ini".format(str(why)))



    # DBDict = gv.LN.dict.iniConfigAsDict(gv.INI.configParser, sectionName='DB_Data', inputData=None, raw=False)

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



    gv.LN.sys.exit(gv, 9999, "Uscita temporanes", printStack=True)


        # -------------------------------------------------------------------------------
        # - Accesso al DB con un fiedl solo
        # -------------------------------------------------------------------------------




    DB = gv.Prj.sql.createTable(gv, gv.DB.File, create=True, TblName=gv.DB.TableName, script=gv.DB.TableCreationScript)
    cur = DB.cursor()
    rCode = gv.Prj.sql.insertRow(gv, cur, TblName=gv.DB.TableName, record=newLIST)
    DB.commit()
    DB.close()
    # choice=gv.LN.sys.getKeyboardInput(gv, "Continue to create DB", validKeys="c", exitKey='XQ')







def readExcelData(gv):
    gv.MainVars.ColumnNames = gv.MainVars.PrimaryColName[:]              # create a new copy of LIST
    gv.MainVars.ColumnNames.extend(gv.MainVars.AttributeColName)
        # -------------------------------------------------------------------------------
        # - Leggiamo il file Excel di Input  e creiamo:
        #      la lista newLIST[]
        # -------------------------------------------------------------------------------
    CSVdata = gv.Prj.excel.readCatalog(gv, gv.MP3.Dict)
    print (len(CSVdata))
    newLIST = []
    nFields = 0
    for line in CSVdata:
        checkFLD = line[1].strip('"')   # excel la colonna.0 è vuota
        newLine = []
        if not checkFLD in ['', 'Type', '@', '#', 'MP3 Base Directory', 'MP3 Player']:
            for inx, colName in enumerate(gv.MainVars.ColumnNames):
                value = line[inx+1]
                # print ("{INX:4}- {COLNAME}: {VALUE}".format(INX=inx, COLNAME=colName, VALUE=value))

                if isinstance(value, int):
                    pass
                elif value.startswith('='):  # rimpiazza la formula
                    value = 0
                elif inx == 5 and value != '.': # Analizzata
                    value = 'Y'
                elif value.lower() in "abcdefghijklmnopqrstuvwxyz":
                    # value = colName[0].upper()
                    value = 1
                else:
                    value = value.strip()

                newLine.append(value)
            newLine.append(0) # valore per l'ultima colonna aggiunta di ToBeDeleted
            newLIST.append(newLine)
            if nFields == 0: nFields = len(newLine)


    outFname = 'd:/tmp/exportedData.csv'
    gv.LN.file.writeFile(gv, outFname, newLIST, append=False, lineSep='\n', exitOnError=True)
    print ('d:/tmp/exportedData.csv  - Written records: ', len(newLIST))
    return newLIST


