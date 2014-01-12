#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# =======================================================================
# Sample call:
# -a extract -i "d:\inp.xls"
# -a extract -inpfile="inp.xls" -outfile="inp_extracted.xls"
#
# return:   extracted Dictionary
# =======================================================================
def Mp3Extract():
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

    mainSectID      = globalARGs[PTR_MAIN_SECTION]
    extractSectID   = globalARGs[PTR_EXTRACT_SECTION]
    songAttrName    = globalARGs[NOME_CALONNE_ATTRIBUTI]


    LnLoggerCLASS.enableConsoleLogger(extractSectID.get('LOG_CONSOLE', logging.INFO))
    LnLoggerCLASS.enableRotateLogger(extractSectID.get('LOG_FILE', logging.INFO))

        # -------------------------------------------------
        # - get configuration parameters
        # -------------------------------------------------
    try:
        Punteggi = extractSectID['Punteggi']

        globalARGs[PUNTEGGI_LIST]       = Punteggi
        globalARGs[EXCEL_INPUT_FILE]    = extractSectID["excelInputFile"]
        globalARGs[EXCEL_OUTPUT_FILE]   = extractSectID["excelOutputFile"]

    except KeyError, why:
        msg = "Key NOT FOUND in config file: %s"  % (why)
        LnSys.exit(10, msg, stackLevel=2)

    # globalARGs[EXTRACTION_TYPE] = 'Punteggio'

    globalARGs.printDictionary()

    # LnLoggerCLASS.enableConsoleLogger('DEBUG')

    MyLogger.debug("inpFile:           %s" % (globalARGs[EXCEL_INPUT_FILE]))
    MyLogger.debug("outFile:           %s" % (globalARGs[EXCEL_OUTPUT_FILE]))
    MyLogger.debug("Punteggi:          %s" % (Punteggi))


        # -----------------------------------------------------
        # - Creiamo una lista con gli indici degli attributi
        # -----------------------------------------------------
    convertToList=False
    attribToExtract = []
    attribToAvoid   = []

    MyLogger.info("Punteggi validi    %s" % (Punteggi))
    # ###################################
    # choice = LnSys.getKeyboardInput("--------- Temporary DEBUG Exit -------", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################

    prepareExcelHeader()                    # prepara le variabili delle colonne

        # -----------------------------------------------------
        # - Leggi il file Excel
        # -----------------------------------------------------
    MP3Dict = ReadExcelCatalog()

        # ------------------------------------------------------------
        # - Estrai i files interessati e ... crea il file di output
        # ------------------------------------------------------------
    extractedDict = extractSelected(MP3Dict, Punteggi=Punteggi, attribToExtract=attribToExtract, attribToAvoid=attribToAvoid)


    if convertToList == True:
        (nLevels, outList) = mp3Dict.dictionaryToList(MaxDeepLevel=99, OutList='Full', Attrib=True, sortIt=True)    # ritorna una lista di liste
        # outList.sort()
        for linea in outList: MyLogger.info(linea)
        # return outList


        # ------------------------------------------------------------
        # - Crea il file di Output
        # ------------------------------------------------------------
    excelOutputFile = globalARGs[EXCEL_OUTPUT_FILE]
    WriteCatalogToExcel(excelOutputFile, extractedDict)
    MyLogger.info("\n\nfile [%s] has been created\n\n" % (excelOutputFile) )
    return extractedDict


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
