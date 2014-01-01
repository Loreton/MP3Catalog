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
def insertSong(gv, myDict, songName, authorName='', albumName='', typeName='', rest=[], fPRINT=False):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    fld         = gv.EXCEL.columnName
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

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
    fld.SONG_SIZE    = int(fld.SONG_SIZE)
    fld.PUNTEGGIO    = int(fld.PUNTEGGIO)

        # ---------------------------------------------------------------
        # - Aggiungiamo la canzone
        # ---------------------------------------------------------------
    newFile = None
    if typeName != 'Titles':
        FullSongPath = "%s\\%s\\%s\\%s\\%s.mp3" % (gv.CONFIG.MP3_BASE_DIR, typeName, authorName, albumName, songName)
        logger.debug("searching song: [%s]" % (FullSongPath))

        indent = 4
            # -----------------------------------------------------------------------------------
            # - Se il file non esiste pi? computer allora cerchiamo qualcosa di simile
            # -----------------------------------------------------------------------------------
        if not os.path.isfile(FullSongPath):

            logger.debug("%s :NOT FOUND [%d] [%s]" % (indent*' ',fld.SONG_SIZE, FullSongPath))
            authorPaths = "%s\\%s\\%s" % (gv.CONFIG.MP3_BASE_DIR, typeName, authorName), "%s\\%s" % (gv.CONFIG.MP3_BASE_DIR, typeName)

                # ---------------------------------------------
                # - Try to search the song into the disk path
                # ---------------------------------------------
            for authorPath in authorPaths:
                logger.info("%s :Searching: [%s\\%s*]" % (indent*' ', authorPath, songName))

                (rCode, fileList) = LnFile.dirListType1(authorPath, pattern=songName + '*' , what='FS')
                # if rCode: choice = LnSys.getKeyboardInput("ERROR Reading directory %s (see LOG file)" % (authorPath), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
                if rCode: choice = LN.sys.getKeyboardInput(gv, "ERROR Reading directory %s (see LOG file)" % (authorPath), validKeys='ENTER', exitKey='XQ', deepLevel=3, fDEBUG=False)

                if len(fileList) > 0:
                    break

            if len(fileList) == 0:              # non sono stati trovati file alternativi
                logger.debug("%s :Non sono state trovate canzoni con il nome: %s" % (indent*' ', FullSongPath))
                songName = songName + '__NO_MATCH_ON_DISK___'

            else:
                logger.debug("%s :cerchiamo un file con lo stesso size: [%s]" % (indent*' ', FullSongPath))
                chkKeys = 'K'
                outMsg = "    [%4s] [%4d] - %s  (NO MORE EXISTS)\n" % ('K', fld.SONG_SIZE, FullSongPath)

                    # ------------------------------------------------------------
                    # - Cerchiamo un file con lo stesso size (se esiste)
                    # ------------------------------------------------------------
                for i in range(len(fileList)):
                    size = os.path.getsize(fileList[i])
                    outMsg += "    [%4d] [%4d] - %s\n" % (i, size, fileList[i])
                    if size == fld.SONG_SIZE:
                        logger.debug("%s :Found:     [%s]" % (indent*' ', fileList[i]))
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
                    logger.info(outMsg)
                    # choice=LN.sys.getKeyboardInput(msg, keyLIST=chkKeys, exitKey='XQ', AnswerForDEBUG=None)
                    choice=LN.sys.getKeyboardInput(gv, msg, validKeys=chkKeys, exitKey='XQ', deepLevel=3, fDEBUG=False)
                    if choice.upper() != 'K':           # insert new song otherwise insert the current one
                        choice = int(choice)
                        newFile = fileList[choice]
        else:
            logger.debug("%s :FOUND: [%s]" % (indent*' ', FullSongPath))
            # logger.debug("%s :replacing song: [%10d] [%-20s] - [%-20s] %-20s - %s" % (indent*' ', fld.SONG_SIZE, typeName, authorName, albumName, songName))

    if newFile == None: # inserisci l'entrata corrente nel DB
        # if songName = d:\MyData\MP3\Stranieri\Music from the ANDEs\Los Pantangoros\La Partida.mp3'
        # print '^^^', songName, rest
        # print '^^^', songName, fld.SONG_SIZE, type(attribSONGSIZE),  type(fld.SONG_SIZE),  type(int(fld.SONG_SIZE))
        # if songName == 'La Partida':
            # ###################################
            # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
            # ###################################

            # pass
        logger.debug("%s :updating with: [%10d] [%-20s] - [%-20s] %-20s - %s" % (indent*' ', fld.SONG_SIZE, typeName, authorName, albumName, songName))
    else:               # la vecchia entrata viene rimpiazzata
            # - Eliminiamo la baseDir ed estraiamo i vari token
        # (Drive, Dir, typeName, authorName, albumName, songName) = newFile.split(os.sep)
        baseDirLen = len(gv.CONFIG.MP3_BASE_DIR) + 1    # +1 per il '\' divisorio
        (typeName, authorName, albumName, songName) = newFile[baseDirLen:].split(os.sep)
        songName = os.path.splitext(songName)[0]
        fld.SONG_SIZE = os.path.getsize(newFile)
        logger.debug("%s :adding New : [%10d] [%-20s] - [%-20s] %-20s - %s" % (indent*' ', fld.SONG_SIZE, typeName, authorName, albumName, songName))

    currAlbumPtr = LN.dict.getDictPtr(gv, myDict, keyList=[typeName, authorName, albumName], fCREATE=True)
    currAlbumPtr[songName] = rest

    # ###################################
    # choice=LN.sys.getKeyboardInput(gv, "******* STOP Temporaneo *******", validKeys="ENTER", exitKey='XQ', deepLevel=3, fDEBUG=False)
    # ###################################


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
