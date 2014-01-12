#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# ===============================================
# - Extracting SONG with valid attributes
# ===============================================
def Songs_Analyze(workingTYPES, RandomDict, outFileList, fPUNTEGGIO=-999):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

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



    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
