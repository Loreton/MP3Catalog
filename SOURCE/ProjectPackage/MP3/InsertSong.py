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
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

    fld         = gv.EXCEL.columnName
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
    if typeName != 'Titles':
        FullSongPath = "%s\\%s\\%s\\%s\\%s.mp3" % (gv.CONFIG.MP3_BASE_DIR, typeName, authorName, albumName, songName)
        logger.debug("searching song: [%s]" % (FullSongPath))

        indent = 4

            # -----------------------------------------------------------------------------------
            # - Se il file non esiste piu' sul filesystem allora cerchiamo qualcosa di simile
            # -----------------------------------------------------------------------------------
        if not os.path.isfile(FullSongPath):
            logger.debug("%s :NOT FOUND [%d] [%s]" % (indent*' ',rowValue[fld.SONG_SIZE], FullSongPath))
                # partendo dal type
            authorPaths = ["%s\\%s\\%s" % (gv.CONFIG.MP3_BASE_DIR, typeName, authorName), "%s\\%s" % (gv.CONFIG.MP3_BASE_DIR, typeName)]
                # partendo dall'autore
            authorPaths = ["%s\\%s\\%s" % (gv.CONFIG.MP3_BASE_DIR, typeName, authorName)]

                # ---------------------------------------------
                # - Try to search the song into the disk path
                # ---------------------------------------------
            for authorPath in authorPaths:
                searchPattern = songName + '.mp3'
                logger.info("%s :Searching: [%s\\%s\\]" % (indent*' ', authorPath, searchPattern))

                (rCode, fileList) = LN.file.dirList(gv, authorPath, pattern=searchPattern, what='FS', getFullPath=True)
                if rCode:
                    choice = LN.sys.getKeyboardInput(gv, "ERROR Reading directory %s (see LOG file)" % (authorPath), validKeys='ENTER', exitKey='XQ', deepLevel=3, fDEBUG=False)

                if len(fileList) > 0:
                    break

            if len(fileList) == 0:              # non sono stati trovati file alternativi
                logger.debug("%s :Non sono state trovate canzoni con il nome: %s" % (indent*' ', FullSongPath))
                songName = songName + '__NO_MATCH_ON_DISK___'

            elif len(fileList) == 1:              # e' stato trovato un solo file alternativo
                msg1 = "%s -Canzone.........: %s" % (indent*' ', FullSongPath)
                msg2 = "%s -sostituita con..: %s" % (indent*' ', fileList[0])
                logger.debug("%s La canzone:%s e' stata sostituita da:%s" % (indent*' ', FullSongPath, fileList[0]))
                print msg1
                print msg2
                newFile = fileList[0]

            else:
                logger.debug("%s :cerchiamo un file con lo stesso size: [%s]" % (indent*' ', FullSongPath))
                chkKeys = 'K'
                outMsg = "    [%4s] [%4d] - %s  (NO MORE EXISTS)\n" % ('K', rowValue[fld.SONG_SIZE], FullSongPath)

                    # ------------------------------------------------------------
                    # - Cerchiamo un file con lo stesso size (se esiste)
                    # ------------------------------------------------------------
                for i in range(len(fileList)):
                    size = os.path.getsize(fileList[i])
                    outMsg += "    [%4d] [%4d] - %s\n" % (i, size, fileList[i])
                    if size == rowValue[fld.SONG_SIZE]:
                        logger.debug("%s :Found:     [%s]" % (indent*' ', fileList[i]))
                        newFile = fileList[i]
                        break
                    chkKeys = "%s%d" % (chkKeys, i)

                    # ------------------------------------------------------------
                    # - Un file con lo stesso size NON è stato trovato.
                    # - Chiediamo a console per una scelta.
                    # ------------------------------------------------------------
                if newFile == None:
                    msg     = "%s :Sono state trovate le canzoni sopra con lo stesso nome" % (indent*' ')
                    msg     = msg + '\n' + outMsg
                    msg     = msg + "\nSelezionare quella che desideri inserire:"
                    logger.info(msg)
                    choice=LN.sys.getKeyboardInput(gv, msg, validKeys=chkKeys, exitKey='XQ', deepLevel=3, fDEBUG=False)
                    if choice.upper() != 'K':           # insert new song otherwise insert the current one
                        choice = int(choice)
                        newFile = fileList[choice]
        else:
            logger.debug("%s :FOUND: [%s]" % (indent*' ', FullSongPath))

    if newFile == None: # inserisci l'entrata corrente nel DB
        logger.debug("%s :updating with: [%10d] [%-20s] - [%-20s] %-20s - %s" % (indent*' ', rowValue[fld.SONG_SIZE], typeName, authorName, albumName, songName))
    else:               # la vecchia entrata viene rimpiazzata
            # - Eliminiamo la baseDir ed estraiamo i vari token
        # (Drive, Dir, typeName, authorName, albumName, songName) = newFile.split(os.sep)
        baseDirLen = len(gv.CONFIG.MP3_BASE_DIR) + 1    # +1 per il '\' divisorio
        (typeName, authorName, albumName, songName) = newFile[baseDirLen:].split(os.sep)
        songName = os.path.splitext(songName)[0]
        rowValue[fld.SONG_SIZE] = os.path.getsize(newFile)
        logger.debug("%s :adding New : [%10d] [%-20s] - [%-20s] %-20s - %s" % (indent*' ', rowValue[fld.SONG_SIZE], typeName, authorName, albumName, songName))

    currAlbumPtr = LN.dict.getDictPtr(gv, myDict, keyList=[typeName, authorName, albumName], fCREATE=True)
    currAlbumPtr[songName] = rowValue[gv.EXCEL.startAttrIndex:]

    # ###################################
    # choice=LN.sys.getKeyboardInput(gv, "******* STOP Temporaneo *******", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
    # ###################################


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
