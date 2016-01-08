#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os
import types



#############################################
# readExcelData(gv)
#############################################
def readExcelData(gv):

    try:
        ExcelSectID              = gv.INI.dict['EXCEL']
        Excel                    = gv.LnClass()
        Excel.fileName           = os.path.abspath(os.path.join(gv.MAIN.mainDataDIR, ExcelSectID['EXCEL_File']))
        Excel.csvFull            = ExcelSectID['CSV_File_fullData']
        Excel.csvValid           = ExcelSectID['CSV_File_validData']
        Excel.sheetName          = ExcelSectID['SheetName']
        Excel.MaxRowsToRead      = int(ExcelSectID['MaxRowsToRead'])
        primaryCols                 = ExcelSectID['Nomi Colonne Primarie']
        Excel.PrimaryColName     = [x.strip('\n').strip() for x in primaryCols.split('\n') if x]
        attrCols                    = ExcelSectID['Nomi Colonne Attributi']
        Excel.AttributeColName   = [x.strip('\n').strip() for x in attrCols.split('\n') if x]

        Excel.ColumnNames        = Excel.PrimaryColName[:]              # create a new copy of LIST
        Excel.ColumnNames.extend(Excel.AttributeColName)

    except Exception as why:
        gv.LN.sys.exit(gv, 1001, "Chiave non trovata: {0} nel file.ini".format(str(why)), printStack=True)

        # -------------------------------------------------------------------------------
        # - Leggiamo il file Excel di Input  e creiamo:
        #      la lista newLIST[]
        # -------------------------------------------------------------------------------
    CSVdata = readCatalog(gv, Excel)
    print (len(CSVdata))
    newLIST = []
    nFields = 0
    for line in CSVdata:
        checkFLD = line[1].strip('"')   # excel la colonna.0 è vuota
        newLine = []
        if not checkFLD in ['', 'Type', '@', '#', 'MP3 Base Directory', 'MP3 Player']:
            for inx, colName in enumerate(Excel.ColumnNames):
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


    gv.LN.file.writeFile(gv, Excel.csvValid, newLIST, append=False, lineSep='\n', exitOnError=True)
    print (Excel.csvValid + ' - Written records: ', len(newLIST))
    return newLIST







# =======================================================================
# ReadExcelCatalog()
# =======================================================================
def readCatalog(gv, Excel):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered   - [called by:{0}]'.format(calledBy(1)))


    fDEBUG = False
    # excelFileName   = Excel.fileName

        # -------------------------
        # - Lettura del WorkBook
        # -------------------------
    wb = gv.LN.excel.read(gv, Excel.fileName, keep_vba=True)
    logger.info('Analisi del foglio: {0}'.format(Excel.sheetName))

        # -------------------------------------------------------
        # - Acquisizione del folgio richiesto in formato CSV
        # -------------------------------------------------------
    if not Excel.sheetName in wb.get_sheet_names():
        gv.LN.exit(gv, 1001, "Il nome del foglio richiesto {0} non e' presente nel file {1}".format(Excel.sheetName, Excel.fileName))
    ExcelCSV = gv.LN.excel.exportToCSV(gv, wb, Excel.sheetName, outFname=Excel.csvFull, maxrows=Excel.MaxRowsToRead, fPRINT=False)


    return  ExcelCSV
