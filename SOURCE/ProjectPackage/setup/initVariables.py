#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys, logging

class myClass():
    pass



def initVariables(gv):
    logger   = gv.LN.logger
    calledBy = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    gv.STATUS                       = myClass()               # lo aggangiamo come sotto-insieme del gv
    gv.STATUS.DIR_NOT_FOUND         = 'DIR NOT FOUND'
    gv.STATUS.DIR_ALREADY_EXISTS    = 'DIR ALREADY EXISTs'
    gv.STATUS.CONFIG_NOT_FOUND      = 'CONFIG NOT FOUND'
    gv.STATUS.CONFIG_FILE_ERROR     = 'CONFIGURATION File Error'
    gv.STATUS.CONFIG_OK             = 'CONFIGURATION OK'
    gv.STATUS.OK                    = 'OK'
    gv.STATUS.NOT_OK                = 'NOT OK'
    gv.STATUS.PROC_WAIT_TIMEOUT     = 'ERROR - Timeout occurs during Process WAITing'


    gv.RCODE                        = myClass()               # lo aggangiamo come sotto-insieme del gv
    gv.RCODE.shortStatus            = ""
    gv.RCODE.errMsg                 = ""
    gv.RCODE.statusMsg              = ""


    gv.INP_PARAM                    = myClass()                     # Dati passati come parametri
    gv.INP_PARAM.fDEBUG             = False
    gv.INP_PARAM.action             = "TEST"                        # TEST - GO - DRY-RUN
    gv.INP_PARAM.actionUPP          = gv.INP_PARAM.action.upper()
    gv.INP_PARAM.mainCfgFile        = None


    gv.INI                          = myClass()                     # Dati relativi alla configurazione del file.ini


    gv.LOG                          = myClass()
    gv.LOG.logDir          = None
    gv.LOG.fileName        = None
    gv.LOG.levelFile       = None
    gv.LOG.levelConsole    = None
    gv.LOG.loggerID        = None
    gv.LOG.nFiles          = 0
    gv.LOG.maxBytes        = 0
    gv.LOG.logger          = None



    # Specific Project Variables
    gv.CONFIG                       = myClass()                     # Dati relativi alla configurazione del file project.cfg
    gv.EXCEL                       = myClass()                     # Dati relativi alla configurazione del file project.cfg
    gv.MP3Dict                      = {}                            # Catalogo delle canzoni

    # ---------------------------------------------------------------------------
    # - variabili GLOBALI
    # ---------------------------------------------------------------------------
    actionARGS = {
        'display':          ['f:d:',    ['srcfile=', 'srcdir=']],               # d,f,      expect parameters
        'extract':          ['f:o:',    ['srcfile=', 'outfile=']],              # f,o,      expect parameters
        'merge':            ['f:d:o:',  ['srcfile=', 'srcdir=', 'outfile=']],   # f,d,o,    expect parameters
        'getrandom':        ['f:t:',    ['srcfile=', 'targetDir=']],            # f,t,      expect parameters
    }

    # gv.CFG                       = myClass()                # nomi variabili del file .CFG
    # gv.CONFIG.INPUT_ARG_ACTION        = 'ACTION'
    # EXCEL_INPUT_FILE        = 'Excel_INPUT FILE'
    # EXCEL_OUTPUT_FILE       = 'Excel_OUTPUT FILE'
    # DIRS_TO_SCAN            = 'Dirs To Scan'
    # gv.CONFIG.MP3_BASE_DIR            = 'mp3 base dir'

    # gv.CONFIG.PTR_MAIN_SECTION        = 'Ptr_Main_Section'
    # gv.CONFIG.PTR_MERGE_SECTION       = 'Ptr_Merge_Section'
    # gv.CONFIG.PTR_EXTRACT_SECTION     = 'Ptr_Extract_Section'
    # gv.CONFIG.PTR_RANDOM_SECTION      = 'Ptr_Random_Section'




    # TYPES                   = []
    # NAME                    = '01 NAME'
    # AVAILABLE_SONGS         = '02 Ci sono canzoni disponibili?'     # BOOL  - False = NON ci sono più canzoni per questo TYPE
    # NEXT_SONG_POINTER       = '03 Prossima canzone disponibile'     # INT  - Pointer (canzoni copiate) alla lista delle canzoni
    # TOTAL_SONGS             = '04 Canzoni Totali Disponibili'       # LONG  - Numero totali di canzoni del TYPE
    # COPIED_SONGS            = '06 Canzoni Copiate'                  # INT  -
    # PERCENT                 = '07 PERCENTUALE'                      # FLOAT  -
    # BYTES_AVAILABLE         = '08 Bytes disponibili'                # INT - Numero MAX di byte disponibile per ogni type
    # BYTES_COPIED            = '09 Bytes copiati'                    # INT - Numero MAX di byte copiati
    # SONG_LIST               = 'LISTA canzoni'                       # LIST - Nomi delle canzoni
    # EXTRACTED_AUTHORS       = 'LISTA Autori'                        # DICT - Serve per verificare il numero MAX di song per autore
    # SHUFFLED_LIST           = 'SHUFFLED'                            # LIST


    # STATUS_HLQ              = 'STATUS'
    # STATUS_COPIED_BYTES     = 'TOTAL_COPIED_BYTES'
    # STATUS_COPIED_SONGS     = 'TOTAL_COPIED_SONGS'
    # STATUS_FILL_DISK        = 'FILL_DISK'
    # STATUS_MAX_BYTES        = 'MAX_OUT_DIR_SIZE'
    # STATUS_MAX_SONGS        = 'MAX_SONGS'
    # STATUS_DEST_DIR         = 'Destination Directory'
    # LIMIT_REACHED           = 'Some limit has been reached'
    # STATUS_MAX_AUTHORS_SONGS = 'MAX_AUTHORS_SONGS'
    # STATUS_NO_MORE_SONGS    = 'NO MORE SONGS AVAILABLE'
    # STATUS_CURRENT_FREE_SPACE = 'Current Drive FreeSpace'

    # gv.CFG.NOME_CALONNE_PRIMARIE   = 'Nomi Colonne Primarie'
    # gv.CFG.NOME_CALONNE_ATTRIBUTI  = 'Nomi Colonne Attributi'
    # gv.CFG.START_EXCEL_COLUMN      = 'START EXCEL COLUMN'
    # EXTRACTION_TYPE         = 'Extraction Type'
    # PUNTEGGI_EXTRACTION_ORDER  = 'Extraction Order'
    # PUNTEGGI_LIST           = 'Lista Punteggi'


    # MP3baseDir, fldName, songAttr = '', '', ''
    # fldTYPE, fldAUTHOR, fldALBUM, fldSONGNAME, fldSONGSIZE = None, None, None, None, None
    # fldSTART_ATTR, attribSONGSIZE, attribPUNTEGGIO = None, None, None
    # songAttrName    = []
    # baseAttribValue = []

    # RCODE_OK                    = 0
    # RCODE_COPY_ERROR            = 1
    # RCODE_SKIP                  = 2
    # RCODE_NO_MORE_SPACE         = 3
    # RCODE_MAX_SONG_NUMBER       = 4
    # RCODE_MAX_SIZE              = 5
    # RCODE_MAX_AUTHOR_SONG_NUMBER  = 6





    logger.debug('exiting - [called by:%s]' % (calledBy(1)))

