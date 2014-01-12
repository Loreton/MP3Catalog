#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# ==============================================================================================================
# - Look for SONG with  attribute
# -     TypeSectID[SHUFFLED_LIST]       lista (numero) delle canzoni
# -     TypeSectID[SONG_LIST]           lista con in nomi delle canzoni
# -     TypeSectID[COPIED_SONGS]        counter delle canzoni copiate (escluse le Mandatory)
# -     TypeSectID[NEXT_SONG_POINTER]   pointer allo TypeSectID[SHUFFLED_LIST] dell'ultima canzone cercata
# ==============================================================================================================
def Songs_GetNext(dict, typeName, fPUNTEGGIO=-999):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

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


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
