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
        # gv.MainVars.AttributeColName    = appo

        gv.DB = gv.LnClass()
        gv.DB.TableName                  = MainSectID['LoretoMP3 TableName']
        gv.DB.TableCreationScript        = MainSectID['LoretoMP3 Script']
        gv.DB.File                       = MainSectID['LoretoMP3 DBFile']

        # gv.LN.dict.printDictionaryTree(gv, gv.DB, header="MainVars Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)

    except Exception as why:
        msg = "Chiave non trovata: {0} nel file.ini".format(str(why))
        gv.LN.sys.exit(gv, 1001, "Chiave non trovata: {0} nel file.ini".format(str(why)))


    gv.MainVars.ColumnNames = gv.MainVars.PrimaryColName[:]              # create a new copy of LIST
    gv.MainVars.ColumnNames.extend(gv.MainVars.AttributeColName)


    # cursor = 1
    # gv.Prj.sql.insertRow(gv, cursor, TblName='tab01', record="CIAO")
    # gv.Prj.sql.insertRow(gv, cursor, TblName='tab01', record=[1])
    # gv.Prj.sql.insertRow(gv, cursor, TblName='tab01', record=[1,2,3,4])
    # gv.Prj.sql.insertRow(gv, cursor, TblName='tab01', record=[[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]])
    # sys.exit()


        # -------------------------------------------------------------------------------
        # - Leggiamo il file Excel di Input  e creiamo:
        #      il DB gv.MP3.Dict
        # -------------------------------------------------------------------------------
    #@TODO: devo leggere il file excel e verificare le colonne
    CSVdata = gv.Prj.excel.readCatalog(gv, gv.MP3.Dict)
    print (len(CSVdata))
    # sys.exit()
    newLIST = []
    nFields = 0
    for line in CSVdata:
        checkFLD = line[1].strip('"')   # excel la colonna.0 è vuota
        # print ("<{0}>".format(checkFLD))
        newLine = []
        if not checkFLD in ['', 'Type', '@', '#', 'MP3 Base Directory', 'MP3 Player']:
            for inx, colName in enumerate(gv.MainVars.ColumnNames):
                value = line[inx+1]
                # print ("{INX:4}- {COLNAME}: {VALUE}".format(INX=inx, COLNAME=colName, VALUE=value))

                if isinstance(value, int):
                    pass
                elif value.startswith('='):  # rimpiazza la formula
                    value = 0
                elif value.lower() in "abcdefghijklmnopqrstuvwxyz":
                    value = colName[0].upper()
                else:
                    value = value.strip()

                newLine.append(value)
                # print ("{INX:4}- {COLNAME}: {VALUE}".format(INX=inx, COLNAME=colName, VALUE=value))
            newLine.append(0) # valore per l'ultima colonna aggiunta di ToBeDeleted
            newLIST.append(newLine)
            if nFields == 0: nFields = len(newLine)

            # print (line)
            # print (newLine)
            # print()
            # choice=gv.LN.sys.getKeyboardInput(gv, "Uscita Temporanea", validKeys="c", exitKey='XQ')

    outFname = 'd:/tmp/exportedData.csv'
    gv.LN.file.writeFile(gv, outFname, newLIST, append=False, lineSep='\n', exitOnError=True)
    print ('d:/tmp/exportedData.csv  - Written records: ', len(newLIST))
    # if gv.MainVars.action == 'EXTRACT':
        # extractID = Prj.extract.ReadIniData(gv)
        # Prj.extract.PercentNormalization(gv, extractID)
        # gv.LN.dict.printDictionaryTree(gv, gv.extract, header="Extract Vars [{0}]".format(calledBy(0), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2))



        # -------------------------------------------------------------------------------
        # - Accesso al DB con un fiedl solo
        # -------------------------------------------------------------------------------

    DB = gv.Prj.sql.createTable(gv, gv.DB.File, create=True, TblName=gv.DB.TableName, script=gv.DB.TableCreationScript)
    cur = DB.cursor()
    rCode = gv.Prj.sql.insertRow(gv, cur, TblName=gv.DB.TableName, record=newLIST)
    DB.commit()
    DB.close()
    # choice=gv.LN.sys.getKeyboardInput(gv, "Continue to create DB", validKeys="c", exitKey='XQ')

    '''
    for record in newLIST:
        # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    '''


