#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


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
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))
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



    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
