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


    sourceMP3Dir          = gv.CONFIG.MP3_BASE_DIR
    destMP3Dir           =  gv.CONFIG.EXTRACT_SECTION['MP3 Destination Directory']
    bPrefixSong         =  gv.CONFIG.EXTRACT_SECTION['PrefixSong']     # Mette <N.Cognome-> dell'autore prima del titolo della canzone All'interno del folder Type



    fld = gv.EXCEL.columnName
    typeName    = song[fld.TYPE]
    authorName  = song[fld.AUTHOR_NAME]
    albumName   = song[fld.ALBUM_NAME]
    songName    = song[fld.SONG_NAME]
    songSize    = song[fld.SONG_SIZE]

        # --------------------------------------------
        # - Verifica dell'esistenza del file di input
        # --------------------------------------------
    sourceFilePath  = os.sep.join([sourceMP3Dir, typeName, authorName, albumName])
    sourceFileName  = songName + '.mp3'
    sourceFullPathName  = os.sep.join([sourceFilePath, sourceFileName])

    if not os.path.isfile(sourceFullPathName):
        print "File NOT FOUND: %s" % (sourceFullPathName)
        return False

        # --------------------------------------------
        # - Creazione dei vari path in/out
        # --------------------------------------------
    if bPrefixSong:
        authorPrefix  = Prj.mp3.getAuthorName(gv, song[fld.TYPE], song[fld.AUTHOR_NAME])
        destFilePath  = os.sep.join([destMP3Dir, typeName])
        destFileName  = "%s-%s.mp3" % (authorPrefix, songName)
    else:
        destFilePath  = os.sep.join([destMP3Dir, typeName, authorName, albumName])
        destFileName  = "%s.mp3" % (songName)

    destFullPathName = os.sep.join([destFilePath, destFileName])
    print "\ncopying file:"
    print "     %s" % (sourceFullPathName)
    print "     %s" % (destFullPathName)

    rCode = LN.file.copyFile(gv, srcPATH=sourceFilePath, dstPATH=destFilePath, srcFile=sourceFileName,  dstFile=destFileName, createDir=True, exitOnError=True)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))

    return rCode








