#!/usr/bin/python -O
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#!/usr/bin/python
#!/usr/bin/python /usr/lib/python2.4/pdb.py
# -O Optimize e non scrive il __debug__

# =========================================================================================================
# = ToDo:
# =========================================================================================================


import os, sys, types
import random, getopt
import optparse

(baseDir, FileName)     = os.path.split(os.path.abspath(sys.argv[0]))
scriptName              = os.path.splitext(FileName)[0]


# ################################################################
# - initLog()
# ################################################################
MyLogger = None
import logging
import LnLogger_Class as LnLOG

def initLog():
    global MyLogger, LnLoggerCLASS
    try:
        (LnLoggerCLASS, MyLogger) = LnLOG.initLog('MP3Catalog', init=True)
        LnLoggerCLASS.enableConsoleLogger(logging.CRITICAL)
        MyLogger.info("Logger for %-20s has been initialized. - called by %s" % (__name__, LnLOG.calledBy(3)))
    except AttributeError, why:
        print ("\n\n--- ERROR opening Logger for %-20s\n  - [%s]\n  - [%s]" % (__name__, why, LnLOG.calledBy(-2)))
        sys.exit(-2)
        
if MyLogger == None: initLog()

# ################################################################
# - initLog()
# - Prevede che la variabile Project sia stata impostata prima del lancio
# - La variabile LnProject ?ndispensabile in quanto tutti i moduli la cercano
# ################################################################
def initUserLog(logID):

    if not logID:
        print 'initUserLog.............................', logID
        print
        print "initUserLog - Please set <%s> environment variable before start this program." % (logID)
        print
        sys.exit(88)
    
    try:
        # creazione del LOG
        (userLoggerCLASS, userLogger) = LnLOG.initLog(logID, init=True)
        
    except AttributeError, why:
        print ("\n\n--- ERROR opening Logger for %-20s\n  - [%s]\n  - [%s]" % (logID, why, LnLOG.calledBy(-2)))
        sys.exit(-2)
    
    userLoggerCLASS.enableConsoleLogger(logging.INFO)
    userLoggerCLASS.enableRotateLogger(logging.DEBUG)
    userLogger.info("Logger for %-20s has been initialized. - called by %s" % (logID, LnLOG.calledBy(3)))
    return userLogger, userLoggerCLASS



import LnSys
import LnFile
import LnDict
import LnString
import LnExcel

global MP3baseDir


import xlrd
import xlwt



# ---------------------------------------------------------------------------
# - variabili GLOBALI
# ---------------------------------------------------------------------------
actionARGS = {
    'display':          ['f:d:',    ['srcfile=', 'srcdir=']],               # d,f,      expect parameters
    'extract':          ['f:o:',    ['srcfile=', 'outfile=']],              # f,o,      expect parameters
    'merge':            ['f:d:o:',  ['srcfile=', 'srcdir=', 'outfile=']],   # f,d,o,    expect parameters
    'getrandom':        ['f:t:',    ['srcfile=', 'targetDir=']],            # f,t,      expect parameters
}

INPUT_ARG_ACTION        = 'ACTION'
EXCEL_INPUT_FILE        = 'Excel_INPUT FILE'
EXCEL_OUTPUT_FILE       = 'Excel_OUTPUT FILE'
DIRS_TO_SCAN            = 'Dirs To Scan'
MP3_BASE_DIR            = 'mp3 base dir'

PTR_MAIN_SECTION        = 'Ptr_Main_Section'
PTR_MERGE_SECTION       = 'Ptr_Merge_Section'
PTR_EXTRACT_SECTION     = 'Ptr_Extract_Section'
PTR_RANDOM_SECTION      = 'Ptr_Random_Section'




TYPES                   = []
NAME                    = '01 NAME'
AVAILABLE_SONGS         = '02 Ci sono canzoni disponibili?'     # BOOL  - False = NON ci sono più canzoni per questo TYPE
NEXT_SONG_POINTER       = '03 Prossima canzone disponibile'     # INT  - Pointer (canzoni copiate) alla lista delle canzoni
TOTAL_SONGS             = '04 Canzoni Totali Disponibili'       # LONG  - Numero totali di canzoni del TYPE
COPIED_SONGS            = '06 Canzoni Copiate'                  # INT  -
PERCENT                 = '07 PERCENTUALE'                      # FLOAT  -
BYTES_AVAILABLE         = '08 Bytes disponibili'                # INT - Numero MAX di byte disponibile per ogni type
BYTES_COPIED            = '09 Bytes copiati'                    # INT - Numero MAX di byte copiati
SONG_LIST               = 'LISTA canzoni'                       # LIST - Nomi delle canzoni
EXTRACTED_AUTHORS       = 'LISTA Autori'                        # DICT - Serve per verificare il numero MAX di song per autore
SHUFFLED_LIST           = 'SHUFFLED'                            # LIST


STATUS_HLQ              = 'STATUS'
STATUS_COPIED_BYTES     = 'TOTAL_COPIED_BYTES'
STATUS_COPIED_SONGS     = 'TOTAL_COPIED_SONGS'
STATUS_FILL_DISK        = 'FILL_DISK'
STATUS_MAX_BYTES        = 'MAX_OUT_DIR_SIZE'
STATUS_MAX_SONGS        = 'MAX_SONGS'
STATUS_DEST_DIR         = 'Destination Directory'
LIMIT_REACHED           = 'Some limit has been reached'
# STATUS_MAX_AUTHORS_SONGS = 'MAX_AUTHORS_SONGS'
STATUS_NO_MORE_SONGS    = 'NO MORE SONGS AVAILABLE'
STATUS_CURRENT_FREE_SPACE = 'Current Drive FreeSpace'

NOME_CALONNE_PRIMARIE   = 'Nomi Colonne Primarie'
NOME_CALONNE_ATTRIBUTI  = 'Nomi Colonne Attributi'
START_EXCEL_COLUMN      = 'START EXCEL COLUMN'
# EXTRACTION_TYPE         = 'Extraction Type'
PUNTEGGI_EXTRACTION_ORDER  = 'Extraction Order'
PUNTEGGI_LIST           = 'Lista Punteggi'


MP3baseDir, fldName, songAttr = '', '', ''
fldTYPE, fldAUTHOR, fldALBUM, fldSONGNAME, fldSONGSIZE = None, None, None, None, None
fldSTART_ATTR, attribSONGSIZE, attribPUNTEGGIO = None, None, None
# songAttrName    = []
# baseAttribValue = []

RCODE_OK                    = 0
RCODE_COPY_ERROR            = 1
RCODE_SKIP                  = 2
RCODE_NO_MORE_SPACE         = 3
RCODE_MAX_SONG_NUMBER       = 4
RCODE_MAX_SIZE              = 5
RCODE_MAX_AUTHOR_SONG_NUMBER  = 6

parser = None

def usage(message):
    # print message
    # parser.print_help()
    LnSys.exit(99, message, stackLevel=3)
    sys.exit()

def ParseInput(cfgFile=None):
    global parser
    usage = "\n\nUsage: %prog -c cfgFile -a action -d debug"
    usage = "\n\nUsage: %prog -c cfgFile -d debug"
    parser = optparse.OptionParser(usage, version="%prog 1.0")

    if cfgFile == None or cfgFile.upper() == 'AUTO':
        cfgFile = '%s.cfg' % (scriptName)
        MyLogger.info('Configuration file: %s' % (cfgFile) )
        
    # parser.add_option( "-a", "--action",
                       # type="string",
                       # dest="action",
                       # default='noGo',
                       # help="You may indicate the ACTION with the -a option. Default is: [noGo]")

    group = optparse.OptionGroup(parser,
                        "\n --------------- Optional parameters----------------",
                        "Use these options to set debug or other values.")

    group.add_option( "-c", "--cfgFile",
                       type="string",
                       dest="cfgFileName",
                       default=cfgFile,
                       help="You may indicate a cfgFile with the -c option. Default is one of the following (in the order): [%s]" % (cfgFile))

    group.add_option( "-d", "--debug",
                       action="store_true",
                       dest="debug",
                       default=False,
                       help="You may indicate a debug status with the -d option. Default is: [False]")

    parser.add_option_group(group)


    (options, args) = parser.parse_args()
    os.environ['ALIAS'] = ''
    return parser, options




def prepareExcelHeader(rowValue=None):
    mainSectID  = globalARGs[PTR_MAIN_SECTION]

    global fldName, songAttr, baseAttribValue
    global fldTYPE, fldAUTHOR, fldALBUM, fldSONGNAME, fldSONGSIZE
    global fldSTART_ATTR, attribSONGSIZE, attribPUNTEGGIO

    RandomSection   = 'Excel_Fields_Names'
    MyLogger.info("Reading [%s] INI section:" % (RandomSection) )


        # -----------------------------------------------------------------------------------------
        # Nomi delle prime colonne.
        # Nomi delle colonne successive relative agli attributi delle canzoni.
        # sono qui come riferimento ma vengono lette direttamente dal foglio excel di input
        # -----------------------------------------------------------------------------------------

    import pprint
    # PrimaryCols  = globalARGs[NOME_CALONNE_PRIMARIE]
    songAttrName = globalARGs[NOME_CALONNE_ATTRIBUTI]
    # pprint.pprint( songAttrName)


        # -------------------------------------------
        # - Valori base degli attributi delle canzoni
        # - Creiamo un
        # -------------------------------------------
    # baseAttribValue = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0']
    baseAttribValue = []
    for name in songAttrName:
        baseAttribValue.append('.')
    baseAttribValue[-1] = 0
    MyLogger.debug("\n%-20s = [%s]\n" % ('baseAttribValue', baseAttribValue))


    # ---------------------------------------------------------
    # - Unisci i nomi delle colonne e verifichiamo
    # - che sono uguali a quelle del foglio excel
    # - La verifica viene fatta solo se viene passato rowValue
    # ---------------------------------------------------------
    totalCols = globalARGs[NOME_CALONNE_PRIMARIE][:]              # create a new copy of LIST
    totalCols.extend(songAttrName)          # aggiungi le altre colonne
    
    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################
    if rowValue != None:
        for i in range(len(rowValue)-1):
            valoreExcel = rowValue[i].encode('utf-8')
            MyLogger.debug("[%s] - [%s]" % (valoreExcel, totalCols[i]))
            if rowValue[i].upper() != totalCols[i].upper():
                Msg = "Il nome colonna definito nel file.ini e' diverso da quanto trovato nel file Excel\n"
                Msg += "Si prega di correggere l'uno oppure l'altro valore\n"
                Msg += "Colonne interessate:    [%s] != [%s]" % (valoreExcel, totalCols[i])
                # pprint.pprint( rowValue)
                # pprint.pprint( totalCols)
                LnSys.exit(10, Msg, stackLevel=2)
        MyLogger.debug("Columns names check has been completed")

        # -------------------------------------------------------------------------------
        # - converte in string ed ENUMera i nomi delle colonne
        # -------------------------------------------------------------------------------
    sTotalCols = ''
    for name in totalCols:
        sTotalCols += ' ' + name.replace(' ', '_')
    MyLogger.debug("%-20s = [%s]" % ('sTotalCols', sTotalCols.upper()))

    strSongAttrName = ''
    for name in songAttrName:
        strSongAttrName += ' ' + name.replace(' ', '_')
    MyLogger.debug("\n%-20s = [%s]\n" % ('strSongAttrName', strSongAttrName.upper()))

    fldName  = LnSys.Enumerate (sTotalCols.upper())
    songAttr = LnSys.Enumerate (strSongAttrName.upper())

    fldTYPE         = fldName.TYPE
    fldAUTHOR       = fldName.AUTHOR_NAME
    fldALBUM        = fldName.ALBUM_NAME
    fldSONGNAME     = fldName.SONG_NAME
    fldPUNTEGGIO    = fldName.PUNTEGGIO
    fldSONGSIZE     = fldName.SONG_SIZE

    # fldSTART_ATTR   = fldSONGNAME+1
    fldSTART_ATTR   = fldPUNTEGGIO

    attribSONGSIZE  = songAttr.SONG_SIZE
    attribPUNTEGGIO  = songAttr.PUNTEGGIO

    if rowValue != None:
        MyLogger.debug("\n%-20s = [%s]\n" % ('attribSONGSIZE', rowValue[attribSONGSIZE]))
        MyLogger.debug("\n%-20s = [%s]\n" % ('fldSTART_ATTR', rowValue[fldSTART_ATTR]))
    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


def test01():
    MP3Dict     =   LnDict.SafeDict(name=' MP3Dict ')
    MP3Dict['Italian'] = LnDict.SafeDict(name= ' Italian ')
    MP3Dict['Italian']['Author1']  = LnDict.SafeDict()
    songDict = {'Song1':'11, 12', 'Song2':'21', 'Song3':'31'}
    MP3Dict['Italian']['Author1']['Album1'] = songDict
    MP3Dict.printDictionary(deepLevel=99, listAttributes=songAttrName)

    print

    dict = LnDict.SafeDict()
    ptr = dict.getSectionPointer(tree='Italian;Author1;Album1', fldSep=';', create=True)
    ptr['Song1'] = '11'                                     # ---------- YES
    ptr = dict.getSectionPointer(tree='Italian;Author1;Album1', fldSep=';', create=True)
    ptr['Song2'] = '21'                                     # ---------- YES
    dict.printDictionary(deepLevel=99, listAttributes=songAttrName)


    ptr = MP3Dict.getSectionPointer(tree='Italian;Author1;Album1', fldSep=';', create=True)
    ptr['Song4'] = '41, 42'                                     # ---------- YES
    ptr['Song2'] = '21'                                     # ---------- YES
    MyLogger.info("\n.................class............")
    MP3Dict.printDictionary(deepLevel=99, listAttributes=songAttrName)
    print

    sys.exit(1)


# =======================================================================
# Mp3Merge()
# =======================================================================
def Mp3Merge():

    mainSectID  = globalARGs[PTR_MAIN_SECTION]
    mergeSectID = globalARGs[PTR_MERGE_SECTION]

    LnLoggerCLASS.enableConsoleLogger(mergeSectID.get('LOG_CONSOLE', logging.INFO))
    LnLoggerCLASS.enableRotateLogger(mergeSectID.get('LOG_FILE', logging.INFO))


        # -------------------------------------------------
        # - input output files
        # -------------------------------------------------
    globalARGs[DIRS_TO_SCAN]        = mergeSectID.get('dir to scan', '')
    globalARGs[EXCEL_INPUT_FILE]    = mergeSectID.get("excelInputFile",  '')
    globalARGs[EXCEL_OUTPUT_FILE]   = mergeSectID.get("excelOutputFile", '')
    globalARGs.printDictionary()

    dir2Scan        = globalARGs[DIRS_TO_SCAN]
    excelInputFile  = globalARGs[EXCEL_INPUT_FILE]
    excelOutputFile = globalARGs[EXCEL_OUTPUT_FILE]

        # ------------------------------------------------------------------------
        # - Se le dir non sono passate come parametro cerchiamole nel file.ini
        # ------------------------------------------------------------------------
    if dir2Scan == '':
        for keyName, dirName in mergeSectID.items():
            if keyName.startswith('dirToAdd.'):
                dir2Scan = "%s;%s" % (dir2Scan, dirName)

    if dir2Scan == '' or excelInputFile == '':
        usage("..... inpDir and inpFile are mandatory parameters")


        # --------------------------------------------------------------------
        # - Leggiamo il file Excel di Input (se richiesto) e creimao il DB
        # - Altrimenti lo creiamo nuovo
        # --------------------------------------------------------------------
    MP3Dict = ReadExcelCatalog()


    # MP3Dict.printDictionary()

        # --------------------------------------------------------------------
        # - Ora facciamo lo scanning delle dirs e le aggiungiamo al DB
        # --------------------------------------------------------------------
    for dirName in dir2Scan:
        dirName = dirName.strip()
        MyLogger.info("scanning folder: [%s]" % (dirName))
        MP3Dict = insertDirectory(dirName, MP3Dict, fDEBUG=True)

        # --------------------------------------------------------------------
        # - Se il file.out non è richiesto allora facciamo il display a video
        # - Altrimenti creiamo un nuovo foglio Excel
        # --------------------------------------------------------------------
    if excelOutputFile == '':
        (nLevels, Mp3List) = MP3Dict.dictionaryToList( MaxDeepLevel=99, OutList='Normal', fPRINT=True)
        for linea in Mp3List:
            MyLogger.info(linea)
    else:
        WriteCatalogToExcel(excelOutputFile, MP3Dict)
        MyLogger.info("\n\nfile [%s] has been created\n\n" % (excelOutputFile))


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


# =======================================================================
# Sample call:
# -a display --dir="d:\MP3\Italiani\Baglioni Claudio"
# -a display -i "d:\inp.xls"
# - dir2Scan pu?sere una singola dir oppure una lista separati da ';'
# =======================================================================
def Mp3Display(iniDB, dir2Scan=None, excelInputFile=None):
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

# =======================================================================
# Sample call:
# -a extract -i "d:\inp.xls"
# -a extract -inpfile="inp.xls" -outfile="inp_extracted.xls"
#
# return:   extracted Dictionary
# =======================================================================
def Mp3Extract():
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


# ===============================================
# - Extracting SONG with valid attributes
# ===============================================
def Songs_Analyze(workingTYPES, RandomDict, outFileList, fPUNTEGGIO=-999):
    fDEBUG = False
    MyLogger.warning('*'*40)
    if fPUNTEGGIO == -999:
        MyLogger.warning('Extracting Flagged songs')
    else:
        MyLogger.warning('Extracting MAX Punteggio songs [%d]' % (fPUNTEGGIO))
    MyLogger.warning('*'*40)

    MyLogger.info( "Working on TYPES: %s" % workingTYPES )

    StatusSectID = RandomDict.getValue(STATUS_HLQ)
    while workingTYPES:                                         # finchè abbiamo un TYPE
        for typeName in workingTYPES:                           # selezioniamo il TYPE
            TypeSectID = RandomDict.getValue(typeName)
            if StatusSectID[LIMIT_REACHED]:
                workingTYPES = []                               # Usciamo
                break

            songIndex = Songs_GetNext(RandomDict, typeName, fPUNTEGGIO)
            if songIndex < 0:
                MyLogger.info('Removing TYPE %s from %s' % (typeName, workingTYPES) )
                workingTYPES.remove(typeName)
                continue

            (rCode, strCode) = CopySongToDest(RandomDict, typeName, songIndex, outFileList)

            songNO                              = TypeSectID[SHUFFLED_LIST][songIndex]
            SongPTR                             = TypeSectID[SONG_LIST][songNO]
            songSize                            = int(SongPTR[fldSONGSIZE])

            CHECK_REAL_DIR = False

            # if rCode == RCODE_OK or rCode == RCODE_SKIP:
            if rCode == RCODE_OK:
                MyLogger.info("[%4d] COPIED  [%s.%d/%d] %s" % (StatusSectID[STATUS_COPIED_SONGS], typeName, TypeSectID[NEXT_SONG_POINTER], TypeSectID[TOTAL_SONGS], strCode) )
                TypeSectID[SHUFFLED_LIST][songIndex]    = -1        # MARK della canzone come copiata

                destDIR     = StatusSectID[STATUS_DEST_DIR]
                outTypeDIR  = "%s\\%s" % (destDIR, typeName)

                StatusSectID[STATUS_COPIED_SONGS]       += 1
                StatusSectID[STATUS_COPIED_BYTES]       += songSize
                TypeSectID[COPIED_SONGS]                += 1
                TypeSectID[BYTES_COPIED]                += songSize

                    # Update del numero di Songs per Author
                ExtractedAuthID                         = TypeSectID[EXTRACTED_AUTHORS]
                authorName                              = SongPTR[fldAUTHOR]
                AuthorsSongs                            = ExtractedAuthID.getValue(authorName, 0)
                ExtractedAuthID[authorName]             = AuthorsSongs + 1  # non posso fare +=1 perche' potrebbe essere None

                    # ogni tot canzoni facciamo una query reale sull'output dir
                if StatusSectID[STATUS_COPIED_SONGS] % 20 == 0:
                    getRealDirStatus(RandomDict)


                # il file esiste di già. 
                # Non aggiorniamo i valori con questa song in quanto dovrebbero essere già considerati
                # NON SONO SICUTO
            elif rCode == RCODE_SKIP:
                MyLogger.info("[%4d] SKIPPING [%s.%d/%d] %s" % (StatusSectID[STATUS_COPIED_SONGS], typeName, TypeSectID[NEXT_SONG_POINTER], TypeSectID[TOTAL_SONGS], strCode) )

                # Non aggiorniamo i valori in quanto non abbiamo copiato alcuna canzone.
            elif rCode == RCODE_MAX_AUTHOR_SONG_NUMBER:
                MyLogger.warning("")
                MyLogger.warning("[%4d] SKIPPING [%s.%d/%d] %s" % (StatusSectID[STATUS_COPIED_SONGS], typeName, TypeSectID[NEXT_SONG_POINTER], TypeSectID[TOTAL_SONGS], strCode) )
                MyLogger.warning("")

            else:
                MyLogger.error("")
                MyLogger.error("[%4d] ERROR    [%s.%d/%d] %s" % (StatusSectID[STATUS_COPIED_SONGS], typeName, TypeSectID[NEXT_SONG_POINTER], TypeSectID[TOTAL_SONGS], strCode) )
                MyLogger.error("")
                # print '8a -------------- sono qui', len(workingTYPES), workingTYPES     
                break
            
            # ###################################
            # choice = LnSys.getKeyboardInput("--------- Temporary DEBUG Exit -------", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
            # ###################################


def getRealDirStatus(RandomDict):

    StatusSectID = RandomDict.getValue(STATUS_HLQ)
    destDIR      = StatusSectID[STATUS_DEST_DIR]

    for typeName in TYPES:
        TypeSectID  = RandomDict.getValue(typeName)
        outTypeDIR  = "%s\\%s" % (destDIR, typeName)
        StatusSectID[STATUS_COPIED_BYTES]   = LnFile.getDirSize(destDIR)
        
        # StatusSectID[STATUS_COPIED_SONGS]   = len(LnFile.dirListType1(destDIR, pattern='*.mp3', what='FS') )
        (rCode, list) = LnFile.dirListType1(destDIR, pattern='*.mp3', what='FS')
        if rCode: choice = LnSys.getKeyboardInput("ERROR Reading directory %s (see LOG file)" % (destDIR), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)        
        StatusSectID[STATUS_COPIED_SONGS]   = len(list)
        
        
        # StatusSectID[STATUS_COPIED_SONGS]   = len(LnFile.dirList(destDIR, includeFILES='*.mp3', what='FS', RETURN='INCL') )
        TypeSectID[BYTES_COPIED]            = LnFile.getDirSize(outTypeDIR)
        
        # TypeSectID[COPIED_SONGS]            = len(LnFile.dirListType1(outTypeDIR, pattern='*.mp3', what='FS') )
        (rCode, list) = LnFile.dirListType1(outTypeDIR, pattern='*.mp3', what='FS') 
        if rCode: choice = LnSys.getKeyboardInput("ERROR Reading directory %s (see LOG file)" % (outTypeDIR), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)        
        TypeSectID[COPIED_SONGS]   = len(list)
        
        
        # TypeSectID[COPIED_SONGS]            = len(LnFile.dirList(outTypeDIR, includeFILES='*.mp3', what='FS', RETURN='INCL') )


# ==============================================================================================================
# - Look for SONG with  attribute
# -     TypeSectID[SHUFFLED_LIST]       lista (numero) delle canzoni
# -     TypeSectID[SONG_LIST]           lista con in nomi delle canzoni
# -     TypeSectID[COPIED_SONGS]        counter delle canzoni copiate (escluse le Mandatory)
# -     TypeSectID[NEXT_SONG_POINTER]   pointer allo TypeSectID[SHUFFLED_LIST] dell'ultima canzone cercata
# ==============================================================================================================
def Songs_GetNext(dict, typeName, fPUNTEGGIO=-999):
    TypeSectID  = dict.getValue(typeName)

    if TypeSectID.getValue(BYTES_COPIED) > TypeSectID.getValue(BYTES_AVAILABLE):
        MyLogger.info("[%s] - NO More Byte available for this type" % (typeName))
        return -1

    if TypeSectID.getValue(COPIED_SONGS) >= TypeSectID.getValue(TOTAL_SONGS):
        MyLogger.info("[%s] - NO More songs available for this type" % (typeName))
        TypeSectID[NEXT_SONG_POINTER] = -1                # update NEXT Pointer
        return -1
    
    fDEBUG = False
    songIndex = -99
    LOOP = True

    while LOOP == True:                                         # finché è minore del numero di canzoni
        songIndex  = TypeSectID.getValue(NEXT_SONG_POINTER)        # get next Pointer all'interno della SHUFFLED_LIST
        TypeSectID[NEXT_SONG_POINTER] = songIndex+1                # update NEXT Pointer

        if songIndex >= TypeSectID[TOTAL_SONGS]:                   # finché è minore del numero di canzoni (parte da 0)
            MyLogger.warning("")
            MyLogger.warning("[%s] - NO More Songs available" % (typeName) )
            MyLogger.warning("")
            LOOP = False
            break

        songNO = TypeSectID[SHUFFLED_LIST][songIndex]              # Numero reale della canzone
        if songNO == -1:                                        # canzone gìà copiata
            continue

        SongPTR = TypeSectID[SONG_LIST][songNO]                 # get Song PTR
        if fPUNTEGGIO == -999:
            attrib  = int(SongPTR[fldName.PUNTEGGIO] )                    # get Song Attrib
            MyLogger.info("Found Punteggio[%d]: %s" % (attrib, SongPTR[0:5]) )
            if fDEBUG: print SongPTR
            return songIndex
        else:
            attrib  = int(SongPTR[fldName.PUNTEGGIO])                     # get Song Attrib
            if attrib == max(globalARGs[PUNTEGGI_LIST]):        # and check if PUNTEGGIO
                MyLogger.info("Found Punteggio[%d]: %s" % (attrib, SongPTR[0:5]) )
                return songIndex
            else:
                continue

    return -1




# ==============================================================
# Contenitore Dati
#    [RandomDict]
#          [Bambini]
#               LISTA               = []    - LIST
#               Percentuale         = xx    - Integer
#               CoeffDivisore       = xx    - Integer   Ogni quante canzoni devo inserirne una. Minore ?l valore pi?zoni devo inserire
#               CanzoniPrelevate    = xx    - Integer
#               Numero Canzoni      = xx    - Integer
#          [Italiani]
#               LISTA               = []    - LIST
#               Percentuale         = xx    - Integer
#               CoeffDivisore       = xx    - Integer
#               CanzoniPrelevate    = xx    - Integer
#               Numero Canzoni      = xx    - Integer
#               ....
#          [STATUS]
#               EXTRACTED_AUTHORS   = {}    - DICT          - Per ogni autore: Numero canzoni estratte
#               MAX_AUTHORS_SONGS   = xx    - Integer       - Numero mazzimo di canzoni permesse per ogni autore
#               TOTAL_COPIED_BYTES  = xx    - Integer
#               TOTAL_COPIED_SONGS  = xx    - Integer
#               FILL_DISK           = 'yyy' - String
#               MAX_SIZE            = xx    - long
#               MAX_SONGS           = xx    - integer
#               destDIR             = 'yyy' - String
# ==============================================================
# =======================================================================
# Sample call:
# mp3Dict:      Dictionary contenente eventuali dati
# =======================================================================
def RandomExtract(mp3Dict):
    mainSectID      = globalARGs[PTR_MAIN_SECTION]
    RndSectID       = globalARGs[PTR_RANDOM_SECTION]
    songAttrName    = globalARGs[NOME_CALONNE_ATTRIBUTI]

    LnLoggerCLASS.enableConsoleLogger(RndSectID.get('LOG_CONSOLE', logging.INFO))
    LnLoggerCLASS.enableRotateLogger(RndSectID.get('LOG_FILE', logging.INFO))

        # -------------------------------------------------
        # - get configuration parameters
        # -------------------------------------------------
    try:
        destDIR                   = RndSectID[STATUS_DEST_DIR]
        FILL_DISK                 = RndSectID[STATUS_FILL_DISK]
        MAX_SIZE                  = RndSectID[STATUS_MAX_BYTES]
        MAX_SONGS                 = RndSectID[STATUS_MAX_SONGS]
        EXTRACTION_ORDER          = RndSectID[PUNTEGGI_EXTRACTION_ORDER]
        PercentDictID             = RndSectID['PERCENT']

    except KeyError, why:
        msg = "Key NOT FOUND in config file: %s"  % (why)
        LnSys.exit(10, msg, stackLevel=2)


    MyLogger.debug("destDIR              : %s" % (destDIR))
    MyLogger.debug("FILL_DISK            : %s" % (FILL_DISK))
    MyLogger.debug("MAX_SIZE             : %s" % (MAX_SIZE))
    MyLogger.debug("MAX_SONGS            : %s" % (MAX_SONGS))
    MyLogger.debug("EXTRACTION_ORDER     : %s" % (EXTRACTION_ORDER))
    MyLogger.debug("Percentuali          : %s" % (PercentDictID))

    globalARGs.printDictionary()

    global TYPES

        # ------------------------------------------
        # - Creazione DB per le variabili di lavoro
        # ------------------------------------------
    RandomDict = LnDict.SafeDict(name=' Random Work Dictionary ')
    for key, val in PercentDictID.items():
        (percent, MaxBytes) = val
        if percent < 1: continue

        typeName = key.upper()

        TYPES.append(typeName)
            # Impostiamo i valori di base
        RandomDict[typeName]            = LnDict.SafeDict(name='RND %s' % (typeName) )
        TypeSectID                      = RandomDict.get(typeName)
        TypeSectID[NAME]                = typeName
        TypeSectID[PERCENT]             = percent
        TypeSectID[BYTES_AVAILABLE]     = MaxBytes
        TypeSectID[COPIED_SONGS]        = 0         # numero delle canzoni copiate (escluse le mandatory)
        TypeSectID[NEXT_SONG_POINTER]   = 0         # puntamento dello scanning. Punta alla shuffled-list
        TypeSectID[TOTAL_SONGS]         = 0         # numero totale delle canzoni per il TYPE
        TypeSectID[SONG_LIST]           = []        # lista delle canzoni
        TypeSectID[SHUFFLED_LIST]       = []        # shuffled list. continene il numero della song. '-' se già usata
        TypeSectID[EXTRACTED_AUTHORS]   = LnDict.SafeDict(name='RND extracted Author')
        TypeSectID[AVAILABLE_SONGS]     = True   # Qualsiasi valore != 0. Contiene 0 quando non ce ne sono

    RandomDict.printDictionary()

        # ---------------------------------------------------
        # - Valori di comodo per lo stato dell'estrazione
        # ---------------------------------------------------
    RandomDict[STATUS_HLQ]                  = LnDict.SafeDict(name='RND STATUS')
    StatusSectID                            = RandomDict.getValue(STATUS_HLQ)
    StatusSectID[STATUS_COPIED_BYTES]       = 0
    StatusSectID[STATUS_COPIED_SONGS]       = 0
    StatusSectID[STATUS_FILL_DISK]          = FILL_DISK
    StatusSectID[STATUS_MAX_BYTES]          = int(MAX_SIZE)
    StatusSectID[STATUS_MAX_SONGS]          = int(MAX_SONGS)
    StatusSectID[STATUS_DEST_DIR]           = destDIR
    StatusSectID[LIMIT_REACHED]             = False
    StatusSectID[STATUS_NO_MORE_SONGS]      = False
    StatusSectID[STATUS_CURRENT_FREE_SPACE] = LnFile.getDriveFreeSpace(destDIR, 'Bytes')
    # StatusSectID[STATUS_MAX_AUTHORS_SONGS]  = int(MAX_AUTHORS_SONGS)

    OutputFile = None

        # -----------------------------------------------------------
        # - Converti il Dictionary in LIST
        # -----------------------------------------------------------
    MyLogger.info("Converting dictionary to LIST")
    (nLevels, outList) = mp3Dict.dictionaryToList(MaxDeepLevel=99, OutList='Full', Attrib=True, sortIt=True)    # ritorna una lista di liste
    MyLogger.debug(len(outList))
    
        # ---------------------------------------------------------------------------------
        # - Creiamo una LIST per ogni TYPE all'interno di RandomDict[typeName][SONG_LIST]
        # ---------------------------------------------------------------------------------
    MyLogger.info("Creating LIST for each TYPE")
    for linea in outList:
        MyLogger.debug(linea)
        typeName = linea[0].upper()         # preleva il TYPE value
        if typeName in TYPES:
            TYPEListaID = RandomDict.getSectionPointer(typeName+';'+SONG_LIST, fldSep=';', create=True)
            TYPEListaID.append(linea)

    for typeName in TYPES:
        TypeSectID                  = RandomDict.get(typeName)
        numSongs                    = len(TypeSectID[SONG_LIST])            # Calcolo numero di Canzoni
        TypeSectID[TOTAL_SONGS]     = numSongs                 # save total number og Songs for this TYPE
        InxList                     = range(numSongs)                           # Crea range
        TypeSectID[SHUFFLED_LIST]   = InxList                 # save range-NO-shuffled to right location


    if OutputFile != None:
        outFileList = []
    else:
        outFileList = None

        # -------------------------------------------------------------
        # - Finita la ricerca dei Mandatory aggiustiamo alcune cose
        # - 1. Randomize index List
        # - 2. Azzeriamo il pointer della NEXT Song
        # -------------------------------------------------------------
    for typeName in TYPES:
        TypeSectID = RandomDict.get(typeName)
        TypeSectID[NEXT_SONG_POINTER] = 0
        random.seed()
        InxList    = TypeSectID[SHUFFLED_LIST]

        MyLogger.info("Shuffling the songs for %s" % (typeName))
        MyLogger.debug("-"*10 + ' Before Shuffle ' + "-"*90)
        MyLogger.debug(InxList)
        MyLogger.debug("-"*100)

        for xx in range(1,21):
            MyLogger.info("%s - Shuffling # %d" % (typeName, xx) )
            random.shuffle( InxList )                             # Crea range-shuffled

        TypeSectID[SHUFFLED_LIST] = InxList         # save range-shuffled to right location

        MyLogger.debug("-"*10 + ' After Shuffle ' + "-"*90)
        MyLogger.debug(TypeSectID[SHUFFLED_LIST])
        MyLogger.debug("-"*100)
        
        
        # --------------------------------------------
        # - SOLO per DEBUG
        # - Fa la lista delle canzoni valide
        # - Mi serve per verificare lo shuffle
        # --------------------------------------------
        xxxx = 9
        if xxxx == 1:
            MP3baseDir = globalARGs[MP3_BASE_DIR]
            for inx in range(len(TypeSectID[SHUFFLED_LIST])):
            
                songNO       = TypeSectID[SHUFFLED_LIST][inx]      # numero reale della canzone
                SongPTR      = TypeSectID[SONG_LIST][songNO]             # Canzone
                
                # SongPTR     = TypeSectID[SONG_LIST][inx]             # Canzone
                # offset      = -1
                typeName    = SongPTR[fldTYPE]
                authorName  = SongPTR[fldAUTHOR]
                albumName   = SongPTR[fldALBUM]
                songName    = SongPTR[fldSONGNAME]
                songSize    = int(SongPTR[fldSONGSIZE])
                filePath    = "%s\\%s\\%s\\%s\\%s.mp3" % (MP3baseDir, typeName, authorName, albumName, songName)
                MyLogger.info("[%6d]: %s" % (songNO, filePath))
    
    debugListDisplay(RandomDict)
            
        # ===========================================================================
        # - partiamo dal punteggio + alto.
        # ===========================================================================
    extractionOrder = RandomDict.get('Order Punteggi', 'firstMAX - restRANDOM')
    if  extractionOrder == 'firstMAX - restRANDOM':
        workingTYPES = TYPES[:]     # copia dei TYPES cu cui andiamo a lavorare per non toccare l'originale utile per il Display
        maxPunt = max(globalARGs[PUNTEGGI_LIST])
        Songs_Analyze(workingTYPES, RandomDict, outFileList, fPUNTEGGIO=maxPunt)
        if workingTYPES == []:
            MyLogger.info("No more TYPES available...[Last score evaluated:%s]" % (maxPunt))
        getRealDirStatus(RandomDict)                        # aggiorniamoci con la realtà della directory

        # ###################################
        choice = LnSys.getKeyboardInput("--------- Punteggio [%d] completato -------" % (maxPunt), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
        # ###################################


        # ===========================================================================
        # - Finita la ricerca dei Mandatory aggiustiamo alcune cose
        # - 1. Azzeriamo il pointer della NEXT Song
        # = 2. Passiamo in rassegna l'intera lista delle canzoni
        # - 3. le copiamo nella destinazione.
        # - 4. Se non riusciamo a raggiungere il valore massimo di bytes, proviamo
        # -    ad aumentare il numero massimo di canzoni per Autore
        # ===========================================================================
    MyLogger.info("Starting random extract process" )
    workingTYPES = TYPES[:]                             # copia dei TYPES cu cui andiamo a lavorare per non toccare l'originale utile per il Display
    while StatusSectID[LIMIT_REACHED] == False:
            
            # - Azzeriamo il pointer della next Song di tutti i types
        for typeName in workingTYPES:
            TypeSectID = RandomDict.get(typeName)
            TypeSectID[NEXT_SONG_POINTER] = 0

        debugListDisplay(RandomDict)

        # ###################################
        choice = LnSys.getKeyboardInput("--------- Pronti alla partenza -------", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
        # ###################################
        Songs_Analyze(workingTYPES, RandomDict, outFileList)
        if workingTYPES == []:
            MyLogger.info("No more TYPES available...[evaluating:%s]" % (globalARGs[PUNTEGGI_LIST]))
            StatusSectID[LIMIT_REACHED] = True
            
            
        # StatusSectID[STATUS_MAX_AUTHORS_SONGS] += 5   # Aumentiamo il numero di autori di due unità

    # ###################################
    choice = LnSys.getKeyboardInput("--------- Temporary DEBUG Exit -------", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################

    if OutputFile != None:
        LnFile.writeFile(OutputFile, outFileList, commentStr=True)
        pass

    debugListDisplay(RandomDict)

    return



# ==========================================================================
# - outFileList: contiene la lista dei file copiati per avere un report finale
# - songIndex:  = indice (nella TypeSectID[SHUFFLED_LIST]) della canzone da copiare
# ==========================================================================
def CopySongToDest(dict, typeName, songIndex, outFileList):
    retValue = (RCODE_OK, "?????")
    RndSectID  = globalARGs[PTR_RANDOM_SECTION]
    MP3baseDir = globalARGs[MP3_BASE_DIR]

        # STATUs varaiables
    StatusSectID        = dict.get(STATUS_HLQ)
    destDIR             = StatusSectID.getValue(STATUS_DEST_DIR)
    FillDISK            = StatusSectID.getValue(STATUS_FILL_DISK)
    # MaxSIZE             = StatusSectID.getValue(STATUS_MAX_BYTES)
    MaxSONGS            = StatusSectID.getValue(STATUS_MAX_SONGS)

        # TYPEs varaiables
    TypeSectID          = dict.get(typeName)
    songNO              = TypeSectID[SHUFFLED_LIST][songIndex]      # numero reale della canzone
    SongPTR             = TypeSectID[SONG_LIST][songNO]             # Canzone


    # offset              = -1
    typeName            = SongPTR[fldTYPE]
    authorName          = SongPTR[fldAUTHOR]
    albumName           = SongPTR[fldALBUM]
    songName            = SongPTR[fldSONGNAME]
    songSize            = int(SongPTR[fldSONGSIZE])

        # ---------------------------------------------------------------
        # - Calcolo del prefisso del nome canzone partendo dal nome autore
        # ---------------------------------------------------------------
    word = authorName.split(' ')
    Cognome = word[-1]
    Nome    = word[0]
    
    if   Nome.lower() == 'santo':   pass        # Santo & Jonny
    elif Nome.lower() == 'cugini':  pass        # Cugini di campagna
    elif Nome.lower() == 'le':      pass        # LE orme
    elif typeName.lower() == 'italiani':
        Cognome = word[0]
        Nome    = word[-1]
        
    if len(word) > 2:
        MiddleWords = ["E", "&", "di", "DI", "Di"]
        Middle = word[1]
        if word[1] in MiddleWords:
            prefixSongName = "%s %s %s-" % (Nome[0],Middle,Cognome)
        else:
            prefixSongName = "%s.%s.%s-" % (Nome[0],Middle[0],Cognome)
    elif len(word) == 2:
        prefixSongName = "%s.%s-" % (Nome[0],Cognome)
    else:
        prefixSongName = "%s-" % (authorName)

        # --------------------------------------------
        # - TEST del FREE Disk SPACE
        # - ed aggiornamento del valore nello Status
        # --------------------------------------------
        # E' stato inserito con un IF  altrimenti rallentava molto su USB drive
    if StatusSectID[STATUS_CURRENT_FREE_SPACE] < songSize+1000:
        StatusSectID[STATUS_CURRENT_FREE_SPACE] = LnFile.getDriveFreeSpace(destDIR, 'Bytes')
    StatusSectID[STATUS_CURRENT_FREE_SPACE] -= songSize
    MyLogger.debug("FreeSPACE:%d" % (StatusSectID[STATUS_CURRENT_FREE_SPACE]))


        # --------------------------------------------
        # - Creazione dei vari path dei file in/out
        # --------------------------------------------
    filePath    = "%s\\%s\\%s\\%s" % (MP3baseDir, typeName, authorName, albumName)
    fileName    = "%s\\%s" % (filePath, songName)
    fName       = "%s.mp3" % (songName)

    outTypeDIR   = "%s\\%s" % (destDIR, typeName)
    outAuthorDIR = "%s\\%s" % (outTypeDIR, authorName)
    
        

    TotalCopiedBytes = LnFile.getDirSize(destDIR)

        # -----------------------------------------
        # - Check del numero di Songs per Author
        # -----------------------------------------
    ExtractedAuthID = TypeSectID[EXTRACTED_AUTHORS]
    AuthorsSongs    = ExtractedAuthID.getValue(authorName, 0)
    sectID = globalARGs[PTR_RANDOM_SECTION]['MAX_AUTHORS_SONGS']
    DefaultAuthorSong = sectID['DEFAULT']
    MaxAuthorSong = sectID.get(authorName, DefaultAuthorSong)
    
    if  TotalCopiedBytes+songSize > StatusSectID[STATUS_MAX_BYTES]:
        StatusSectID[LIMIT_REACHED] = True
        return (RCODE_MAX_SIZE, "MAX_SIZE [%d] reached" % (StatusSectID[STATUS_MAX_BYTES]) )

    elif FillDISK == 'YES' and StatusSectID[STATUS_CURRENT_FREE_SPACE] < 0:   # include già la current songSize
        StatusSectID[LIMIT_REACHED] = True
        return (RCODE_NO_MORE_SPACE, "No more FreeSPACE [%d] is available" % (StatusSectID[STATUS_CURRENT_FREE_SPACE]))

    elif StatusSectID[STATUS_COPIED_SONGS] >= MaxSONGS:
        StatusSectID[LIMIT_REACHED] = True
        return (RCODE_MAX_SONG_NUMBER, "Max number of Songs [%d] have been reached" % (MaxSONGS))

    # elif AuthorsSongs >= StatusSectID[STATUS_MAX_AUTHORS_SONGS]:
    elif AuthorsSongs >= MaxAuthorSong:
        return (RCODE_MAX_AUTHOR_SONG_NUMBER, "[%s:%d] - Max song number [%d] per %s has been reached" % (typeName.upper(), TypeSectID[NEXT_SONG_POINTER], MaxAuthorSong, authorName))


            # ----------------------------------------------------------------------------
            # - Se il file esiste di già ....
            # ----------------------------------------------------------------------------
    if RndSectID.get('PrefixSong', False):
        destfName   = "%s%s" % (prefixSongName, fName)
    else:
        destfName   = fName

    outFname     = "%s\\%s" % (outAuthorDIR, destfName)
            
    if os.path.isfile(outFname):
        Msg0 = "Song: %s - already exists." % (outFname)

        currSize = os.path.getsize(outFname)

        if currSize == songSize:
            retValue = (RCODE_SKIP, "[%s] - The target filesize is the same as new. NOT replaced!" % (Msg0) )

        elif currSize > songSize:
            retValue = (RCODE_SKIP, "[%s] - The target filesize is greater then new. NOT replaced!" % (Msg0) )

        else:
            # rCode = LnFile.copyFiles(filePath, fName, outAuthorDIR, destfName)
            rCode = LnFile.copyMoveFile(fName, filePath, outAuthorDIR, dstFname=destfName)
            if rCode == 0:
                retValue = (RCODE_SKIP, "[%s] - File has been replaced" % (Msg0) )
            else:
                retValue = (RCODE_SKIP, "[%s] - ERROR replacing file" % (Msg0) )

    else:
        Msg0 = "Song: %s" % (outFname)
        # rCode = LnFile.copyFiles(filePath, fName, outAuthorDIR, destfName)
        rCode = LnFile.copyMoveFile(fName, filePath, outAuthorDIR, dstFname=destfName)
        if rCode == 0:
            retValue = (RCODE_OK, "[%s] - copied" % (Msg0) )
            if outFileList != None:
                outFileList.append(fileName + '.mp3')
        else:
            retValue = (RCODE_COPY_ERROR, "[%s] - ERROR copying file" % (Msg0) )



    return retValue

def debugListDisplay(RandomDict):
    StatusSectID = RandomDict.getValue(STATUS_HLQ)
    MyLogger.info("."*30)
    for varName, varValue in sorted(StatusSectID.items()):
        validTypes =  [types.IntType, types.StringType, types.FloatType, types.LongType, types.BooleanType]
        if type(varValue) in validTypes:
            MyLogger.info( "%-35s = %s" % (varName, varValue) )


    for typeName in TYPES:
        TypeSectID   = RandomDict.get(typeName)
        MyLogger.info("."*30)
        for varName, varValue in sorted(TypeSectID.items()):
            validTypes =  [types.IntType, types.StringType, types.FloatType, types.LongType, types.BooleanType]
            if type(varValue) in validTypes:
                MyLogger.info( "%-35s = %s" % (varName, varValue) )

    print

    # choice = LnSys.getKeybKeyboardInput("******* Vuoi continuare???", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)


# ====================================================================
# - Normalizzazione della percentuale a 100 nel caso non lo fosse
# ====================================================================
def RandomExtractNormalize(RandomDict, MAX_BYTES, Text=''):
    MyLogger.info("\n\n------------- %s" % (Text) )


        # -----------------------------------------------------
        # - Calcolo della Percentuale relativa alle entrate
        # -----------------------------------------------------
    TotalePercentuale = 0.0
    for typeName in TYPES:
        TypeSectID  = RandomDict.get(typeName)
        # if TypeSectID[PERCENT] > 0 and TypeSectID[BYTES_COPIED] < TypeSectID[BYTES_AVAILABLE]:
        if TypeSectID[PERCENT] > 0 :
            TotalePercentuale += TypeSectID[PERCENT]

        # -----------------------------------------------------
        # - Applicazione della Percentuale relativa
        # -----------------------------------------------------
    for typeName in TYPES:
        TypeSectID  = RandomDict.get(typeName)
        percent     = TypeSectID[PERCENT]
        if percent > 0:
            TypeSectID[AVAILABLE_SONGS] = True
            percent                     = (percent * 100) / TotalePercentuale
            TypeSectID[PERCENT]         = round(percent, 2)
            MAX_VAL                     = MAX_BYTES * (TypeSectID[PERCENT]/100)
            TypeSectID[BYTES_AVAILABLE] = int(round(MAX_VAL,0))   # Massimo numero di bytes per il singolo type
            TypeSectID[BYTES_COPIED]    = 0                         # bytes copiati per il singolo type
        else:
            TypeSectID[AVAILABLE_SONGS] = False
            TypeSectID[BYTES_AVAILABLE] = 0
            TypeSectID[BYTES_COPIED]    = 0                         # bytes copiati per il singolo type

        # ---------------------------------------------------
        # - Display delle percentuale
        # ---------------------------------------------------
    # debugListDisplay(RandomDict)

    return


# =======================================================
# - insertDirectory()
# - Insert a directory into MP3 dictionary
# =======================================================
def insertDirectory(dirName, dict=None, fDEBUG=False):
    MP3baseDir = globalARGs[MP3_BASE_DIR]

    if dict == None:
        dict = LnDict.SafeDict(name='Insert Dir' )

    albumName   = ''
    authorName  = ''
    typeName    = ''
    MyLogger.info("reading directory: [%s]" % (dirName))

    if dirName == '':
        MyLogger.info("skipping a null directory: [%s]" % (dirName))
        return dict


        # - Ritorna il path relativo
    (rCode, MP3List) = LnFile.dirListType1(dirName, pattern='*.mp3', what='FS')
    if rCode: choice = LnSys.getKeyboardInput("ERROR Reading directory %s (see LOG file)" % (dirName), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
        
    # MP3List = LnFile.dirList(dirName, includeFILES='*.mp3', what='FS', RETURN='INCL', returnPath='FULL')
    # if fDEBUG:
    MyLogger.debug('*'*40)
    for line in MP3List: MyLogger.debug(line)
    MyLogger.debug('*'*40)


    for file in MP3List:
            # - Ricostruisci nome completo
        MyLogger.debug("inserting file: [%s]" % (file))
        try:
                # eliminiamo la baseDir dal nome file
            baseDirLen = len(MP3baseDir) + 1
            (typeName, authorName, albumName, songName) = LnSys.splitUnicode(file[baseDirLen:], os.sep)
            # ###################################
            # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
            # ###################################

        except StandardError, why:
            Msg1 = "Il file [%s]\ncontiene piu' campi[%d] del previsto\nVerificare!!"  % (file, baseDirLen)
            LnSys.exit(10, Msg1, stackLevel=2)

        songName = os.path.splitext(songName)[0]
        songSize = os.path.getsize(file)

            # ----------------------------------------------------------------------------------------------
            # - Cerchiamo l'Album all'interno del DB.Dictionary
            # - Siccome il dictionary e' case sensitive nelle entrate, facciamo il controllo
            # - ignorando il case e rimpiazziamo sempre l'entrata con quella trovata sul disco.
            # ----------------------------------------------------------------------------------------------
        FOUND = False
        albumDict = dict.getSectionPointer(typeName+';'+authorName+';'+albumName, fldSep=';', create=False)
        if albumDict != None:
            for song, properties in albumDict.items():
                if song.upper() == songName.upper():
                    del albumDict[song]                         # REMOVE old entry
                    properties[attribSONGSIZE] = int(songSize)  # aggiorniamo solo il size della canzone
                    albumDict[songName] = properties            # ADD della canzone in modo da portarsi eventuali UPPER/LOWER case nuovi
                    FOUND = True                                # SKIP inserimento
                    break

            # --------------------------------------
            # - canzone non trovata, inseriamola
            # --------------------------------------
        if FOUND == False:
            MyLogger.info("adding New : [%10d] [%-20s] - [%-20s] %-20s - %s" % (songSize, typeName, authorName, albumName, songName))
            albumDict = dict.getSectionPointer(typeName+';'+authorName+';'+albumName, fldSep=';', create=True)
            newProperties = baseAttribValue[:]
            newProperties[attribSONGSIZE] = int(songSize)
            newProperties[attribPUNTEGGIO] = 0
            albumDict[songName] = newProperties


    return dict

# -------------------------------------------
# - Verifichiamo che non ci siano colonne vuote
# -------------------------------------------
def verifyColContent(attribCols):

    # baseAttribValue = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0']
    # print len(attribCols), attribCols
    for i in range(len(attribCols)-1):
        if attribCols[i] == '':
            attribCols[i] = u'.'
        # print attribCols[i]
        
    return attribCols

    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################

    
def ReadExcelCatalog():
    fDEBUG = False
    excelFileName = globalARGs[EXCEL_INPUT_FILE]
    mainSectID    = globalARGs[PTR_MAIN_SECTION]
    

    if not os.path.isfile(excelFileName):
        LnSys.exit(10, "File doesn't exists: [%s]" % (excelFileName), stackLevel=3)

    MyLogger.info("Reading excelFileName: [%s]."  % (excelFileName))
    prevAuth = '...'
    dict    = LnDict.SafeDict(name = ' MP3Dict ')
    wb      = xlrd.open_workbook(excelFileName)

    for sheet in wb.sheets():

        MyLogger.info('SheetName: %s' % (sheet.name))
        FldNames_ROW    =   mainSectID.get('FIELDS_NAME') -1                    # considerare che Excel parte da Row=0
        START_ROW       =   mainSectID.get('FIRST_SONG_ROW') -1                 # considerare che Excel parte da Row=0
        LAST_ROW        =   60                 # per DEBUG
        LAST_ROW        =   9999999
        startExcelCol = globalARGs[START_EXCEL_COLUMN].upper()   # Colonna di partenza dati
        for row in range(sheet.nrows):
            rowValue = LnExcel.getRow(sheet, row, wb, wantTupleDate=False)
            dummyCols = ord(startExcelCol) - ord('A')                # Eliminiamo le colonne vuote
            while dummyCols:
                del rowValue[0]
                dummyCols -= 1
                # print '^^^^ removing item', rowValue[0]
            MyLogger.debug("rowValue: [%s]" % (rowValue))
            
                # ------------------------------------------
                # - calcoliamo i nomi delle colonne
                # ------------------------------------------
            if row == FldNames_ROW:
                    # - Verifica che i campi siano corretti ed enumera gli stessi
                prepareExcelHeader(rowValue)
                continue

            elif row<START_ROW:
                continue

            elif row>LAST_ROW:
                MyLogger.warning("."*60)
                MyLogger.warning("MAX_ROWs has been reached.......")
                MyLogger.warning("."*60)
                break

            nCols     = sheet.ncols
            nCols     = len(rowValue)
            lastValidCOL = fldSONGSIZE+1
            if nCols > lastValidCOL:               # ultima colonna valida
                rowValue = rowValue[:lastValidCOL]
            elif nCols < lastValidCOL:               # NON PREVISTO
                LnSys.exit(11, "Il numero di colonne del file non può essere inferiore alle colonne preciste. [nCols:%d]<[fldSONGSIZE:%d]" % (nCols, fldSONGSIZE) )
            
            typeName    = rowValue[fldTYPE]
            authorName  = rowValue[fldAUTHOR]
            albumName   = rowValue[fldALBUM]
            songName    = rowValue[fldSONGNAME]

                 # riga vuota
            if typeName == '' or typeName == '#':
                MyLogger.debug("skipping row: [%s]" % (rowValue))
                continue
            
            if fDEBUG: print "^^^^^ %s/%s/%s/%s" % (typeName, authorName, albumName, songName), type(songName)
            if type(songName) == types.IntType:
               continue
            elif len(songName) < 2:
                continue

            if songName.find('_NO_MATCH_ON_DISK_') > 0:
                MyLogger.debug("Skipping file: [%s]" % (songName))
                continue

            if prevAuth != authorName:
                prevAuth = authorName
                MyLogger.info("reading author: [%s]" % (authorName) )

            restFields  = rowValue[fldSTART_ATTR:]
            restFields = verifyColContent(restFields)

            if len(songName) >= 2 and typeName != 'Titles':
                MP3InsertSong(dict, songName, authorName, albumName, typeName, restFields)
                if typeName == 'UNKNOWN':
                    xx=LnSys.getKeyboardInput("Vuoi continuare???", keyLIST='Y', exitKey='XQ')





    # dict.printDictionary(MaxDeepLevel=99, listAttributes=songAttrName)
    return dict

# =========================================================================
# - Si aspetta una lista dove oni riga è a sua volta una lista
# =========================================================================
def WriteCatalogToExcel(outFileName, dict):
    # fDEBUG = True
    fDEBUG = False

    if fDEBUG:
        MyLogger.debug('*'*40)
        dict.printDictionary()
        MyLogger.debug('*'*40)

        # --------------------------------------------
        # - Creazione del file di Output
        # --------------------------------------------
    WkBook = xlwt.Workbook()
    WkSheet = WkBook.add_sheet('MP3_Catalog', cell_overwrite_ok=True)

    (nLevels, linee) = dict.dictionaryToList(MaxDeepLevel=99, fPRINT=False, OutList='Full', Attrib=True, sortIt=True) # ritorna una lista di liste
    fDEBUG = False
    # fDEBUG = True
    if fDEBUG:
        MyLogger.debug('*'*40)
        for line in linee:
            MyLogger.debug(line)
        MyLogger.debug('*'*40)
    # LnSys.exit.exit(LnSys.EXIT_STACK, "--------------- TempoTemporaTemporary DEBUG Exit ---------------------")


    prevAlbumName=''
    prevAuthorName=''
    currRow=0
    startExcelCol = globalARGs[START_EXCEL_COLUMN].upper()   # Colonna di partenza dati
    
    for row in linee:
        try:
                # Assicurati che il SongSIZE sia INTEGER
            col = fldName.SONG_SIZE; row[col] = int(row[col])
            col = fldName.PUNTEGGIO; row[col] = int(row[col])
            # print '^^^^^^' , len(row), row
            # print '^^^^^^' , fldName.SONG_SIZE, row[fldName.SONG_SIZE-1], row[fldName.PUNTEGGIO-1]
        except:
            print "ERROR on line: (forse contiene qualche char invalido??"
            print "    %s" % (row)
            # ###################################
            choice = LnSys.getKeyboardInput("* ERRORE.... *", keyLIST='ENTER', exitKey='QX')
            # ###################################
        currRow += 1
        MyLogger.debug('writing row[%d]: %s' % (currRow, row))
        albumName   = row[fldALBUM]
        authorName  = row[fldAUTHOR]
        if authorName != prevAuthorName:
            prevAlbumName  = albumName
            prevAuthorName = authorName
            MyLogger.info("writing [%-40s]-[%s]" % (authorName, albumName) )

            
        excelRrow = WkSheet.row(currRow)    # pointer alla riga
            # Inseriamo le colonne vuote per allineare il foglio
        dummyCols = ord(startExcelCol) - ord('A')                
        while dummyCols:
            row.insert(0, '')               # inseriamo la colonna 0 - Vuota
            dummyCols -= 1
        col = 0
        for value in row:
            WkSheet.write(currRow, col, value)
            col += 1
            # WkSheet.write(currRow, col, "Ciao sono Loreto")
            # WkSheet.col(col).width = colsWidth
            # excelRrow.write(col, value, style)


    WkBook.save(outFileName)
    MyLogger.info("File: %s has been written!" % (outFileName))




# ======================================================
# = Inserisce una canzone nel Dictionary
# = authorName puo' essere anche un Integer (tipo 883)
# ======================================================
def MP3InsertSong(dict, songName, authorName='', albumName='', typeName='', rest=[], fPRINT=False):
    MP3baseDir  = globalARGs[MP3_BASE_DIR]

        # ---------------------------------------------------------------
        # - Pointer al current TypeName (Italiani, Stranieri, Bambini, ...)
        # ---------------------------------------------------------------
    if len(songName) < 2: return
    if authorName == '': authorName = 'UNKNOWN'
    if albumName  == '': albumName  = 'UNKNOWN'
    if typeName   == '': typeName   = 'UNKNOWN'


    authType = type(authorName)
    if isinstance(authorName, unicode):
        if authorName.startswith('Totale Autori'):
            return
        
        # ------------------------------------------
        # - Accertiamoci che SongSize sia INTEGER
        # - Accertiamoci che Punteggi sia INTEGER
        # ------------------------------------------
    rest[attribSONGSIZE]    = int(rest[attribSONGSIZE])
    rest[attribPUNTEGGIO]   = int(rest[attribPUNTEGGIO])

        # ---------------------------------------------------------------
        # - Aggiungiamo la canzone
        # ---------------------------------------------------------------
    newFile = None
    if typeName != 'Titles':
        FullSongPath = "%s\\%s\\%s\\%s\\%s.mp3" % (MP3baseDir, typeName, authorName, albumName, songName)
        MyLogger.debug("searching song: [%s]" % (FullSongPath))

        indent = 4
            # -----------------------------------------------------------------------------------
            # - Se il file non esiste pi? computer allora cerchiamo qualcosa di simile
            # -----------------------------------------------------------------------------------
        if not os.path.isfile(FullSongPath):

            MyLogger.debug("%s :NOT FOUND [%d] [%s]" % (indent*' ',rest[attribSONGSIZE], FullSongPath))
            authorPaths = "%s\\%s\\%s" % (MP3baseDir, typeName, authorName), "%s\\%s" % (MP3baseDir, typeName)

                # ---------------------------------------------
                # - Try to search the song into the disk path
                # ---------------------------------------------
            for authorPath in authorPaths:
                MyLogger.info("%s :Searching: [%s\\%s*]" % (indent*' ', authorPath, songName))

                (rCode, fileList) = LnFile.dirListType1(authorPath, pattern=songName + '*' , what='FS')
                if rCode: choice = LnSys.getKeyboardInput("ERROR Reading directory %s (see LOG file)" % (authorPath), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)

                if len(fileList) > 0:
                    break
            
            if len(fileList) == 0:              # non sono stati trovati file alternativi
                MyLogger.debug("%s :Non sono state trovate canzoni con il nome: %s" % (indent*' ', FullSongPath))
                songName = songName + '__NO_MATCH_ON_DISK___'

            else:
                MyLogger.debug("%s :cerchiamo un file con lo stesso size: [%s]" % (indent*' ', FullSongPath))
                chkKeys = 'K'
                outMsg = "    [%4s] [%4d] - %s  (NO MORE EXISTS)\n" % ('K', rest[attribSONGSIZE], FullSongPath)
                    
                    # ------------------------------------------------------------
                    # - Cerchiamo un file con lo stesso size (se esiste)
                    # ------------------------------------------------------------
                for i in range(len(fileList)):
                    size = os.path.getsize(fileList[i])
                    outMsg += "    [%4d] [%4d] - %s\n" % (i, size, fileList[i])
                    if size == rest[attribSONGSIZE]:
                        MyLogger.debug("%s :Found:     [%s]" % (indent*' ', fileList[i]))
                        newFile = fileList[i]
                        break
                    chkKeys = "%s%d" % (chkKeys, i)

                    # ------------------------------------------------------------
                    # - Un file con lo stesso size NON esiste.
                    # - Chiediamo a console per una scelta.
                    # ------------------------------------------------------------
                if newFile == None:
                    msg     = "%s :Sono state trovate le seguenti canzoni con lo stesso nome" % (indent*' ', )
                    msg     = msg + "Selezionare quella che desideri inserire"
                    MyLogger.info(outMsg)
                    choice=LnSys.getKeyboardInput(msg, keyLIST=chkKeys, exitKey='XQ', AnswerForDEBUG=None)
                    if choice.upper() != 'K':           # insert new song otherwise insert the current one
                        choice = int(choice)
                        newFile = fileList[choice]
        else:
            MyLogger.debug("%s :FOUND: [%s]" % (indent*' ', FullSongPath))
            # MyLogger.debug("%s :replacing song: [%10d] [%-20s] - [%-20s] %-20s - %s" % (indent*' ', rest[attribSONGSIZE], typeName, authorName, albumName, songName))

    if newFile == None: # inserisci l'entrata corrente nel DB
        # if songName = d:\MyData\MP3\Stranieri\Music from the ANDEs\Los Pantangoros\La Partida.mp3'
        # print '^^^', songName, rest
        # print '^^^', songName, rest[attribSONGSIZE], type(attribSONGSIZE),  type(rest[attribSONGSIZE]),  type(int(rest[attribSONGSIZE]))
        # if songName == 'La Partida':
            # ###################################
            # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
            # ###################################

            # pass
        MyLogger.debug("%s :updating with: [%10d] [%-20s] - [%-20s] %-20s - %s" % (indent*' ', rest[attribSONGSIZE], typeName, authorName, albumName, songName))
    else:               # la vecchia entrata viene rimpiazzata
            # - Eliminiamo la baseDir ed estraiamo i vari token
        # (Drive, Dir, typeName, authorName, albumName, songName) = newFile.split(os.sep)
        baseDirLen = len(MP3baseDir) + 1    # +1 per il '\' divisorio
        (typeName, authorName, albumName, songName) = newFile[baseDirLen:].split(os.sep)
        songName = os.path.splitext(songName)[0]
        rest[attribSONGSIZE] = os.path.getsize(newFile)
        MyLogger.debug("%s :adding New : [%10d] [%-20s] - [%-20s] %-20s - %s" % (indent*' ', rest[attribSONGSIZE], typeName, authorName, albumName, songName))

    currAlbumPtr = dict.getSectionPointer(typeName+';'+authorName+';'+albumName, fldSep=';', create=True)
    currAlbumPtr[songName] = rest



# =======================================================================================
# - Estrae tutte le canzoni che hanno una 'x' nei campi richiesti
# - Tutti queste canzoni verranno salvate in un file excel di output (if != None)
# - Se retType == LIST allora verrà ritornala una lista invece del DICT
# =======================================================================================
def extractSelected(dict, Punteggi=[], attribToExtract=[], attribToAvoid=[]):

    outDict = LnDict.SafeDict(name =' outDict ')
    # songAttrName = globalARGs[NOME_CALONNE_ATTRIBUTI]

    MyLogger.info("                     %s" % (Punteggi) )

    MyLogger.info("\n")
    # PunteggiLista = range(min(Punteggi), max(Punteggi)+1)
    
    for typeName in dict.keys():
        authorDict = dict.get(typeName)
        for authorName in authorDict.keys():
            albumDict = authorDict.get(authorName)
            for albumName in albumDict.keys():
                songDict = albumDict.get(albumName)
                
                for songName, val in songDict.items():
                    valore = val[attribPUNTEGGIO]
                    # if valore in Punteggi:
                    if valore >= min(Punteggi) and valore <= max(Punteggi):
                        currAlbumPtr = outDict.getSectionPointer(typeName+';'+authorName+';'+albumName, fldSep=';', create=True)
                        currAlbumPtr[songName] = val

    return outDict


def setMainVars(logClass=None):
    global LnLoggerCLASS

    if logClass: LnLoggerCLASS = logClass

    # import __builtin__
    # print __builtin__.foo
    # sys.exit()

    
    
#############################################################################################
# - M A I N
#############################################################################################
globalARGs=None
import pprint
userLogger = None
# import MP3Catalog_Funcs as LNfunc
def Main(callerName, args):
    global uLOG, userLoggerCLASS, CFG
    global globalARGs

        # =======================================
        # - get Input parameters
        # =======================================
    # (parser, options)   = LNfunc.ParseInput(callerName + '.cfg')
    (parser, options)   = ParseInput(callerName + '.cfg')
    fDEBUG              = options.debug 
    # Action              = options.action
    cfgFile             = options.cfgFileName
    # sectionName         = options.action + 'Section'

    if fDEBUG:
        LnSys.printObjectVars(options)
       
        # =======================================
        # - Initialize UserLOG
        # =======================================
    (uLOG, userLoggerCLASS) = initUserLog("Mp3Catalog_uLOG")
    uLOG.info("System Log: %s" % (LnLoggerCLASS.getLogName() ))

    
    globalARGs = LnDict.SafeDict(name="global Variables")

    LnSys.setBaseEnv(fDEBUG=True)
    fDEBUG = False

    if fDEBUG:
        LnLOG.changeLogLevel(LnLOG.logID, logging.DEBUG)
        LnSys.printObjectVars(options)

        # =======================================
        # - checking and Loading CONFIG file
        # =======================================
    # if not sectionName:
        # parser.print_help()
        # sys.exit()
        
    # CFG = LNfunc.loadConfigModule(cfgFile)    
    # pprint.pprint(CFG)
        # --------------------------------------------------------
        # - Lettura del file di configurazione
        # - Esci se le sezioni di interesse non esistono
        # --------------------------------------------------------
    configDB = LnSys.loadConfigModule(cfgFile, parser, fDEBUG=fDEBUG)
    # pprint.pprint(configDB)
    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST=['Ciao', "ENTER"], exitKey='QX', AnswerForDEBUG=None, fDEBUG=True)
    # ###################################
    try:
            # Le section sono quelle prelevate direttamente dal file di configurazione
        mainSectID                          = configDB.MainSection
        globalARGs[MP3_BASE_DIR]            = configDB.MP3baseDIR
        globalARGs[PTR_MAIN_SECTION]        = configDB.MainSection
        globalARGs[PTR_MERGE_SECTION]       = configDB.MergeSection
        globalARGs[PTR_EXTRACT_SECTION]     = configDB.ExtractSection
        globalARGs[PTR_RANDOM_SECTION]      = configDB.RandomSection
        globalARGs[NOME_CALONNE_ATTRIBUTI]  = mainSectID.get(NOME_CALONNE_ATTRIBUTI)
        globalARGs[NOME_CALONNE_PRIMARIE]   = mainSectID.get(NOME_CALONNE_PRIMARIE)
        globalARGs[START_EXCEL_COLUMN]      = mainSectID.get(START_EXCEL_COLUMN)
        globalARGs[INPUT_ARG_ACTION]        = mainSectID.get('ACTION').upper()
        # print '^^^^', globalARGs[NOME_CALONNE_PRIMARIE]
        # print '^^^^', globalARGs[START_EXCEL_COLUMN]

    except StandardError, why:
        LnSys.exit(97, "%s  %s" % (cfgFile, why) )

    LnLoggerCLASS.enableConsoleLogger(mainSectID.get('LOG_CONSOLE', logging.INFO))
    LnLoggerCLASS.enableRotateLogger(mainSectID.get('LOG_FILE', logging.INFO))




    # globalARGs[INPUT_ARG_ACTION] = options.action.upper()
    globalARGs.printDictionary()

    choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
    if globalARGs[INPUT_ARG_ACTION ] == 'MERGE':
        Mp3Merge()

    elif globalARGs[INPUT_ARG_ACTION ] == 'EXTRACT':
        extractedFile = Mp3Extract()

    elif globalARGs[INPUT_ARG_ACTION ] == 'RANDOM':
        extractedDict = Mp3Extract()
        RandomExtract(extractedDict)
    # ---------------
        choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
    # ---------------

    elif globalARGs[INPUT_ARG_ACTION ] == 'DISPLAY':
        MP3Catalog.Mp3Display(iniDB, dir2Scan=globalARGs[INPUT_ARG_INPDIR ], excelInputFile=globalARGs[EXCEL_OUTPUT_FILE])

    else:
        print globalARGs[INPUT_ARG_ACTION ]
        Msg1 = "Should NOT Occur.\n"
        LnSys.exit(10, Msg1, stackLevel=2)

    print "Process completed."
    sys.exit()

if __name__ == "__main__":
    # test01()
    sys.exit()