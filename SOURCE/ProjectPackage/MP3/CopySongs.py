#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os


# ############################################################################################
# = Copia le canzoni con il FLAG di Mandatory
# = RETURN: LIST[] delle canzoni rimaste.
# ############################################################################################
def copySongs(gv, inpList=[]):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))

    configID            = gv.CONFIG.EXTRACT_SECTION
    MP3baseDir          = gv.CONFIG.MP3_BASE_DIR
    MP3baseDirLen       = len(MP3baseDir) + 1

    sMP3DestDir         =  gv.CONFIG.EXTRACT_SECTION['MP3 Destination Directory']
    sExtractOrder       =  gv.CONFIG.EXTRACT_SECTION['Extraction Order']
    lPunteggioRange     =  gv.CONFIG.EXTRACT_SECTION['Punteggi']
    bPrefixSong         =  gv.CONFIG.EXTRACT_SECTION['PrefixSong']     # Mette <N.Cognome-> dell'autore prima del titolo della canzone All'interno del folder Type
    bRecomended         =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
    prefixStatic        =  gv.CONFIG.EXTRACT_SECTION['Prefissi particolari']


    fld = gv.EXCEL.columnName


    for song in inpList:
        typeName    = song[fld.TYPE]
        authorName  = song[fld.AUTHOR_NAME]
        albumName   = song[fld.ALBUM_NAME]
        songName    = song[fld.SONG_NAME]

        if bPrefixSong:
            authorPrefix = Prj.mp3.getAuthorName(gv, song[fld.TYPE], song[fld.AUTHOR_NAME])
            fName = "%s-%s" % (authorPrefix, songName)
            filePath    = os.sep.join([MP3baseDir, typeName, fName])
        else:
            filePath    = os.sep.join([MP3baseDir, typeName, authorName, albumName, songName])


            # --------------------------------------------
            # - Creazione dei vari path dei file in/out
            # --------------------------------------------
        print filePath
        # fileName    = "%s\\%s" % (filePath, songName)
        # fName       = "%s.mp3" % (songName)

        # outTypeDIR   = "%s\\%s" % (destDIR, typeName)
        # outAuthorDIR = "%s\\%s" % (outTypeDIR, authorName)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    # return outLines
