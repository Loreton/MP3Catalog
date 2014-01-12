#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# ==========================================================================
# - outFileList: contiene la lista dei file copiati per avere un report finale
# - songIndex:  = indice (nella TypeSectID[SHUFFLED_LIST]) della canzone da copiare
# ==========================================================================
def CopySongToDest(dict, typeName, songIndex, outFileList):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

    retValue = (RCODE_OK, "?????")
    RndSectID  = globalARGs[PTR_RANDOM_SECTION]
    MP3baseDir = globalARGs[MP3_BASE_DIR]
    autoriParticolari = RndSectID['autoriParticolari']

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
    # PREFIXSONG = False
    # if PREFIXSONG:
    word = authorName.split(' ')
    Cognome = word[-1]
    Nome    = word[0]

    if   authorName in autoriParticolari:
        prefixSongName = autoriParticolari[authorName]

    elif   len(word) == 1:
        prefixSongName = "%s-" % (authorName)

    elif len(word) == 2:
        if typeName.lower() == 'italiani':
            (Cognome, Nome) = authorName.split(' ')
        else:
            (Nome, Cognome) = authorName.split(' ')
        prefixSongName = "%s.%s-" % (Nome[0],Cognome)

    elif len(word) == 3:
        if typeName.lower() == 'italiani':
            (Middle, Cognome, Nome) = authorName.split(' ')
        else:
            (Middle, Cognome, Nome) = authorName.split(' ')
        prefixSongName = "%s. %s %s-" % (Nome[0],Middle,Cognome)
    # else:
        # prefixSongName = ''

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

    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
