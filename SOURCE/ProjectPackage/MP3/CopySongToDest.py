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
def copySongToDest(gv, song):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))



    typeName    = song[fld.TYPE]
    authorName  = song[fld.AUTHOR_NAME]
    albumName   = song[fld.ALBUM_NAME]
    songName    = song[fld.SONG_NAME]
    songSize    = song[fld.SONG_SIZE]


        # --------------------------------------------
        # - Verifica dell'esistenza del file di input
        # --------------------------------------------
    sourceFullPathName  = os.sep.join([MP3baseDir, typeName, songName])
    if not os.file.isfile(sourceFullPathName):
        print "File NOT FOUND: %s" % (sourceFullPathName)

        # --------------------------------------------
        # - Creazione dei vari path in/out
        # --------------------------------------------
    if bPrefixSong:
        authorPrefix  = Prj.mp3.getAuthorName(gv, song[fld.TYPE], song[fld.AUTHOR_NAME])
        destFilePath  = os.sep.join([sMP3DestDir, typeName])
        destFileName  = "%s-%s.mp3" % (authorPrefix, songName)
    else:
        destFilePath  = os.sep.join([MP3baseDir, typeName, authorName, albumName])
        destFileName  = "%s.mp3" % (songName)


    gv.MP3.TYPE.BYTES[typeName] = LN.file.getFolderSize(destFilePath)
    gv.MP3.TYPE.BYTES[typeName] += songSize












    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    # return outLines
