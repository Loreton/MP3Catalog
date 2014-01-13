#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os

class myClass():    pass

# #######################################################################
# # Lettura del file di configurazione
# #######################################################################
def readProjectConfig(gv, cfgFileName=None):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))


    if not cfgFileName:
        Prj.exit(gv, 97, "Missing configFile %s" % (cfgFileName) )

    # ----------------------------------------------------------------------
    # - Lettura del file di configurazione
    # - Leggiamo anche i valori considerati Mandatory
    # ----------------------------------------------------------------------
    (cfgMODULE, cfgDICT, cfgPATH, cfgFULLPATH) =  LN.dict.loadDictFile(gv, cfgFileName, moduleName=None, fDEBUG=False)


    gv.CONFIG.FILE_MODULE   = cfgMODULE    # SAVE module pointer
    gv.CONFIG.FILE_DICT     = cfgDICT       # SAVE module pointer

        # --------------------------------------------------------
        # - Pointers delle sezioni di interesse
        # --------------------------------------------------------
    # configDB = cfgMODULE.MainSection
    configDB = cfgMODULE

    try:
            # ----------------------------------------------------------
            # Prendiamo i pointer delle section.
            # Li prendiamo qi solo per essere certi che ci siano.
            # In caso di errori non proseguaimo.
            # ----------------------------------------------------------
        gv.CONFIG.MP3_BASE_DIR              = configDB.MP3baseDIR
        gv.CONFIG.MAIN_SECTION              = configDB.MainSection
        gv.CONFIG.MERGE_SECTION             = configDB.MergeSection
        gv.CONFIG.EXTRACT_SECTION           = configDB.ExtractSection
        # gv.CONFIG.RANDOM_SECTION            = configDB.RandomSection

        mainSectID                          = configDB.MainSection
        gv.CONFIG.NOMI_COLONNE_ATTRIBUTI    = mainSectID.get('Nomi Colonne Attributi')
        gv.CONFIG.NOMI_COLONNE_PRIMARIE     = mainSectID.get('Nomi Colonne Primarie')

        gv.CONFIG.START_EXCEL_COLUMN        = mainSectID.get('START EXCEL COLUMN')          # Prima colonna valida
        gv.CONFIG.COLUMNS_NAME_ROW          = mainSectID.get('COLUMNS NAME ROW')-1            # riga che contiene i nomi delle colonne (considerare che Excel parte da Row=0)
        gv.CONFIG.FIRST_SONG_ROW            = mainSectID.get('FIRST SONG ROW')-1              # riga dove iniziano i dati (considerare che Excel parte da Row=0)
        gv.CONFIG.LAST_SONG_ROW             = mainSectID.get('LAST SONG ROW')               # riga dove finiscono i dati

        gv.CONFIG.ACTION                    = mainSectID.get('ACTION').upper()

        gv.CONFIG.EXCEL_INPUT_FILE          = mainSectID.get("excelInputFile",  '')
        gv.CONFIG.EXCEL_OUTPUT_FILE         = mainSectID.get("excelOutputFile", '')

        logger.info('Configuration file:%s has been read]' % (cfgFileName) )

    except StandardError, why:
        Prj.exit(gv, 2001, "%s  %s" % (cfgFileName, why) )


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return gv.CONFIG.FILE_DICT