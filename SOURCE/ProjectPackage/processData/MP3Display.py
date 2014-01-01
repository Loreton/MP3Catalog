#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


 # =======================================================================
# Sample call:
# -a display --dir="d:\MP3\Italiani\Baglioni Claudio"
# -a display -i "d:\inp.xls"
# - dir2Scan pu?sere una singola dir oppure una lista separati da ';'
# =======================================================================
def Mp3Display(iniDB, dir2Scan=None, excelInputFile=None):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))


    # fDEBUG = True
    fDEBUG = False
    if fDEBUG:
        MyLogger.info("Action:  " , "Display")
        MyLogger.info("inpFile: " , excelInputFile)
        MyLogger.info("inpDir:  " , dir2Scan)
        # MyLogger.info('..................... DEBUG EXIT ...............')
        # sys.exit()

    if dir2Scan == None and excelInputFile == None:
            # -------------------------
            # - get Excel Section data
            # -------------------------
        DisplaySection  = 'Excel_Display'
        MyLogger.info("Reading [%s] INI section:" % (DisplaySection) )
        DisplaySectID   = iniDB.getValue(DisplaySection,  iniDB.ExitOnMissingKEY)
        dir2Scan = DisplaySectID.getValue('inputDIR',  None)

        if dir2Scan == None:
            excelInputFile  = DisplaySectID.getValue('inputFILE',  None)
            if excelInputFile == None:
                Msg1 = "Il file di Input oppura una directory sono indispensabili per selezionare le canzoni\n\n"
                LnSys.exit(10, Msg1, stackLevel=2)


    if dir2Scan != None:
        prepareExcelHeader(iniDB, None) # prepara le variabili delle colonne
        dir2Scan = dir2Scan.split(';')
        # dirs = []
        # if dir2Scan == types.StringType:
            # dir2Scan = [dir2Scan]

        for dir in dir2Scan:
            dir = dir.strip()
            MyLogger.info("\n\nReading directory [%s]" % (dir) )
            MP3Dict = insertDirectory(dir)

    elif excelInputFile != None:
        MP3Dict = ReadExcelCatalog(iniDB, excelInputFile)
    else:
        Msg1 = "Il file di Input oppura una directory sono indispensabili per selezionare le canzoni\n\n"
        LnSys.exit(10, Msg1, stackLevel=2)

    MP3Dict.printDictionary(deepLevel=3, listAttributes=globalARGs[NOME_CALONNE_ATTRIBUTI], TREE=False)



    logger.info('exiting - [called by:%s]' % (calledBy(1)))
