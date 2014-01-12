#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os
import types


# #############################################################
# = Inserisce una canzone nel Dictionary
# = authorName puo' essere anche un Integer (tipo 883)
# #############################################################
def insertSong(gv, myDict, rowValue=[]):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('Entered - [called by:%s]' % (calledBy(1))) # non metterlo ad info


    fld         = gv.EXCEL.columnName
    songAttrib  = gv.EXCEL.songAttrName
    typeName    = rowValue[fld.TYPE]
    authorName  = rowValue[fld.AUTHOR_NAME]
    albumName   = rowValue[fld.ALBUM_NAME]
    songName    = rowValue[fld.SONG_NAME]


        # ---------------------------------------------------------------
        # - Pointer al current TypeName (Italiani, Stranieri, Bambini, ...)
        # ---------------------------------------------------------------
    authType = type(authorName)
    if isinstance(authorName, unicode):
        if authorName.startswith('Totale Autori'):
            return

        # ------------------------------------------
        # - Accertiamoci che SongSize sia INTEGER
        # - Accertiamoci che Punteggi sia INTEGER
        # ------------------------------------------
    rowValue[fld.SONG_SIZE]    = int(rowValue[fld.SONG_SIZE])
    rowValue[fld.PUNTEGGIO]    = int(rowValue[fld.PUNTEGGIO])

        # ---------------------------------------------------------------
        # - Aggiungiamo la canzone
        # ---------------------------------------------------------------
    newFile = None
    INDENT = 4*' '
    if typeName != 'Titles':
        FullSongPath = "%s\\%s\\%s\\%s\\%s.mp3" % (gv.CONFIG.MP3_BASE_DIR, typeName, authorName, albumName, songName)
        logger.debug("searching song: [%s]" % (FullSongPath))


            # -----------------------------------------------------------------------------------
            # - Se il file non esiste piu' sul filesystem allora cerchiamo qualcosa di simile
            # -----------------------------------------------------------------------------------
        if not os.path.isfile(FullSongPath):
            logger.debug("%15s: NOT FOUND [%d] [%s]" % (INDENT,rowValue[fld.SONG_SIZE], FullSongPath))
                # partendo dall'autore e dal type
            authorPaths = ["%s\\%s\\%s" % (gv.CONFIG.MP3_BASE_DIR, typeName, authorName), "%s\\%s" % (gv.CONFIG.MP3_BASE_DIR, typeName)]
                # partendo dall'autore
            authorPaths = ["%s\\%s\\%s" % (gv.CONFIG.MP3_BASE_DIR, typeName, authorName)]

                # ---------------------------------------------
                # - Try to search the song into the disk path
                # ---------------------------------------------
            for authorPath in authorPaths:
                searchPattern = songName + '.mp3'
                logger.info("%15s: [%s\\%s]" % ("Searching", authorPath, searchPattern))

                (rCode, fileList) = LN.file.dirList(gv, authorPath, pattern=searchPattern, what='FS', getFullPath=True)
                if rCode:
                    choice = LN.sys.getKeyboardInput(gv, "ERROR Reading directory %s (see LOG file)" % (authorPath), validKeys='ENTER', exitKey='XQ', deepLevel=3, fDEBUG=False)

                if len(fileList) > 0:
                    break

            if len(fileList) == 0:              # non sono stati trovati file alternativi
                logger.debug("%15s: Non sono state trovate canzoni con il nome: %s" % (INDENT, FullSongPath))
                songName = songName + '__NO_MATCH_ON_DISK___'

            elif len(fileList) == 1:              # e' stato trovato un solo file alternativo
                msg1 = "%15s: -Canzone.........: %s" % (INDENT, FullSongPath)
                msg2 = "%15s: -sostituita con..: %s" % (INDENT, fileList[0])
                logger.debug("%15s: La canzone:%s e' stata sostituita da:%s" % (INDENT, FullSongPath, fileList[0]))
                print msg1
                print msg2
                newFile = fileList[0]

            else:                               # sono stati trovati diversi file alternativi
                logger.debug("%15s: cerchiamo un file con lo stesso size: [%s]" % (INDENT, FullSongPath))
                chkKeys = 'K'
                outMsg = "    [%4s] [%4d] - %s  (NO MORE EXISTS)\n" % ('K', rowValue[fld.SONG_SIZE], FullSongPath)

                    # ------------------------------------------------------------
                    # - Cerchiamo un file con lo stesso size (se esiste)
                    # ------------------------------------------------------------
                for i in range(len(fileList)):
                    size = os.path.getsize(fileList[i])
                    outMsg += "    [%4d] [%4d] - %s\n" % (i, size, fileList[i])
                    if size == rowValue[fld.SONG_SIZE]:
                        logger.debug("%15s: Found:     [%s]" % (INDENT, fileList[i]))
                        newFile = fileList[i]
                        break
                    chkKeys = "%s%d" % (chkKeys, i)

                    # ------------------------------------------------------------
                    # - Un file con lo stesso size NON è stato trovato.
                    # - Chiediamo a console per una scelta.
                    # ------------------------------------------------------------
                if newFile == None:
                    msg     = "%15s: :Sono state trovate le canzoni sopra con lo stesso nome" % (INDENT)
                    msg     = msg + '\n' + outMsg
                    msg     = msg + "\nSelezionare quella che desideri inserire:"
                    logger.info(msg)
                    choice=LN.sys.getKeyboardInput(gv, msg, validKeys=chkKeys, exitKey='XQ', deepLevel=3, fDEBUG=False)
                    if choice.upper() != 'K':           # insert new song otherwise insert the current one
                        choice = int(choice)
                        newFile = fileList[choice]
        else:
            logger.debug("         FOUND: [%s]" % (FullSongPath))

    if newFile:
            # - Eliminiamo la baseDir ed estraiamo i vari token
        baseDirLen = len(gv.CONFIG.MP3_BASE_DIR) + 1    # +1 per il '\' divisorio
        (typeName, authorName, albumName, songName) = newFile[baseDirLen:].split(os.sep)
        songName = os.path.splitext(songName)[0]
        rowValue[fld.SONG_SIZE] = os.path.getsize(newFile)
        logger.debug("%15s: [%10d] [%-20s] - [%-20s] %-20s - %s" % ("adding New", rowValue[fld.SONG_SIZE], typeName, authorName, albumName, songName))

    else:               # la vecchia entrata viene rimpiazzata
        logger.debug("%15s: [%10d] [%-20s] - [%-20s] %-20s - %s" % ("updating with", rowValue[fld.SONG_SIZE], typeName, authorName, albumName, songName))





        # ---------------------------------
        # - Aggiornamento del DB
        # ---------------------------------
    currAlbumPtr = LN.dict.getDictPtr(gv, myDict, keyList=[typeName, authorName, albumName], fCREATE=True)
    ptrSong = currAlbumPtr.get(songName)
    if ptrSong:     # esiste ... modifichiamo solo il size (magari è uguale)
        ptrSong[songAttrib.SONG_SIZE] = rowValue[fld.SONG_SIZE]
    else:           # creiamo la canzone
        currAlbumPtr[songName] = rowValue[gv.EXCEL.startAttrIndex:]

        # ---------------------------------
        # - Aggiornamento delle Rows Excel - NON VA BENE
        # ---------------------------------
    # songLine = [typeName, authorName, albumName, songName]
    # songLine.extend(rowValue[gv.EXCEL.startAttrIndex:])
    # gv.EXCEL.ROWS.append(songLine)


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
