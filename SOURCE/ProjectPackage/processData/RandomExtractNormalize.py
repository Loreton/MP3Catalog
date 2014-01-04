#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types

# ====================================================================
# - Normalizzazione della percentuale a 100 nel caso non lo fosse
# ====================================================================
def RandomExtractNormalize(RandomDict, MAX_BYTES, Text=''):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))
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


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
