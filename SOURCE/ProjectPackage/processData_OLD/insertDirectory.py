#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types

# =======================================================
# - insertDirectory()
# - Insert a directory into MP3 dictionary
# =======================================================
def insertDirectory(dirName, dict=None, fDEBUG=False):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))


    MP3baseDir = globalARGs[MP3_BASE_DIR]

    if dict == None:
        dict = LnDict.SafeDict(name='Insert Dir' )

    albumName   = ''
    authorName  = ''
    typeName    = ''
    MyLogger.info("reading directory: [%s]" % (dirName))

    if dirName == '':
        MyLogger.info("skipping a null directory: [%s]" % (dirName))
        return dict


        # - Ritorna il path relativo
    (rCode, MP3List) = LnFile.dirListType1(dirName, pattern='*.mp3', what='FS')
    if rCode: choice = LnSys.getKeyboardInput("ERROR Reading directory %s (see LOG file)" % (dirName), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)

    # MP3List = LnFile.dirList(dirName, includeFILES='*.mp3', what='FS', RETURN='INCL', returnPath='FULL')
    # if fDEBUG:
    MyLogger.debug('*'*40)
    for line in MP3List: MyLogger.debug(line)
    MyLogger.debug('*'*40)


    for file in MP3List:
            # - Ricostruisci nome completo
        MyLogger.debug("inserting file: [%s]" % (file))
        try:
                # eliminiamo la baseDir dal nome file
            baseDirLen = len(MP3baseDir) + 1
            (typeName, authorName, albumName, songName) = LnSys.splitUnicode(file[baseDirLen:], os.sep)
            # ###################################
            # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
            # ###################################

        except StandardError, why:
            Msg1 = "Il file [%s]\ncontiene piu' campi[%d] del previsto\nVerificare!!"  % (file, baseDirLen)
            LnSys.exit(10, Msg1, stackLevel=2)

        songName = os.path.splitext(songName)[0]
        songSize = os.path.getsize(file)

            # ----------------------------------------------------------------------------------------------
            # - Cerchiamo l'Album all'interno del DB.Dictionary
            # - Siccome il dictionary e' case sensitive nelle entrate, facciamo il controllo
            # - ignorando il case e rimpiazziamo sempre l'entrata con quella trovata sul disco.
            # ----------------------------------------------------------------------------------------------
        FOUND = False
        albumDict = dict.getSectionPointer(typeName+';'+authorName+';'+albumName, fldSep=';', create=False)
        if albumDict != None:
            for song, properties in albumDict.items():
                if song.upper() == songName.upper():
                    del albumDict[song]                         # REMOVE old entry
                    properties[attribSONGSIZE] = int(songSize)  # aggiorniamo solo il size della canzone
                    albumDict[songName] = properties            # ADD della canzone in modo da portarsi eventuali UPPER/LOWER case nuovi
                    FOUND = True                                # SKIP inserimento
                    break

            # --------------------------------------
            # - canzone non trovata, inseriamola
            # --------------------------------------
        if FOUND == False:
            MyLogger.info("adding New : [%10d] [%-20s] - [%-20s] %-20s - %s" % (songSize, typeName, authorName, albumName, songName))
            albumDict = dict.getSectionPointer(typeName+';'+authorName+';'+albumName, fldSep=';', create=True)
            newProperties = baseAttribValue[:]
            newProperties[attribSONGSIZE] = int(songSize)
            newProperties[attribPUNTEGGIO] = 0
            albumDict[songName] = newProperties


    return dict


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
