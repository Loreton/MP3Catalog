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
        # choice=gv.LN.sys.getKeyboardInput(gv, "Uscita Temporanea", validKeys="X", exitKey='XQ')


        appo                            = MainSectID['Nomi Colonne Attributi']
        gv.MainVars.AttributeColName    = [x.strip('\n').strip() for x in appo.split('\n') if x]
        # gv.MainVars.AttributeColName    = appo
        gv.LN.dict.printDictionaryTree(gv, gv.MainVars, header="MainVars Vars [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)



    except Exception as why:
        msg = "Chiave non trovata: {0} nel file.ini".format(str(why))
        gv.LN.sys.exit(gv, 1001, "Chiave non trovata: {0} nel file.ini".format(str(why)))


    gv.MainVars.ColumnNames = gv.MainVars.PrimaryColName[:]              # create a new copy of LIST
    gv.MainVars.ColumnNames.extend(gv.MainVars.AttributeColName)


        # -------------------------------------------------------------------------------
        # - Accesso al DB
        # -------------------------------------------------------------------------------
    gv.Prj.sql.createTable(gv, "d:/tmp/LnSQLit3.db", 'Tabella01', gv.MainVars.ColumnNames)

    choice=gv.LN.sys.getKeyboardInput(gv, "Uscita Temporanea", validKeys="X", exitKey='XQ')



        # -------------------------------------------------------------------------------
        # - Leggiamo il file Excel di Input  e creiamo:
        #      il DB gv.MP3.Dict
        # -------------------------------------------------------------------------------
    gv.Prj.excel.readCatalog(gv, gv.MP3.Dict)


    if gv.MainVars.action == 'EXTRACT':
        extractID = Prj.extract.ReadIniData(gv)
        Prj.extract.PercentNormalization(gv, extractID)
        # gv.LN.dict.printDictionaryTree(gv, gv.extract, header="Extract Vars [{0}]".format(calledBy(0), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2))




