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
    bPrefixSong         =  gv.CONFIG.EXTRACT_SECTION['PrefixSong']     # Mette <N.Cognome-> dell'autore prima del titolo della canzone All'interno del folder Type
    bRecomended         =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
    fillDISK            =  gv.CONFIG.EXTRACT_SECTION['FILL_DISK']


    fld = gv.EXCEL.columnName

    nSongs = 0
    for song in inpList:
        nSongs += 1

        # -------------------------------------------------------------------------------------------------------------
        # DEVO fare tutte le verifiche preliminari per capire se devo copiare o meno la canzone sulla destinazione
        # -------------------------------------------------------------------------------------------------------------
        typeName    = song[fld.TYPE]
        authorName  = song[fld.AUTHOR_NAME]
        # albumName   = song[fld.ALBUM_NAME]
        # songName    = song[fld.SONG_NAME]
        songSize    = song[fld.SONG_SIZE]

        # fileSize                    = os.path.getsize(sourceFullPathName)
        # gv.MP3.TYPE.BYTES[typeName] = LN.file.getFolderSize(destFilePath)

        driveFreeSpace              = gv.MP3.driveFreeSpace



        # --------------------------------------------
        # - TEST del FREE Disk SPACE
        # - Lo facciamo a fronte di
        # --------------------------------------------
        # E' stato inserito con un IF  altrimenti rallentava molto su USB drive
        if nSongs%100 == 0: gv.MP3.driveFreeSpace = LN.file.driveFreeSpace(destFilePath, 'Bytes')

        if gv.CONFIG.EXTRACT_SECTION['FILL_DISK'] and gv.MP3.driveFreeSpace < (songSize+1000):
            Prj.exit(gv, 4444,  "No more FreeSPACE [%d] is available" % (gv.MP3.driveFreeSpace))


        if gv.MP3.TYPE.BYTES[typeName] > gv.CONFIG.EXTRACT_SECTION['PERCENT'][typeName]:
            print "MAX_SIZE [%d] reached for TYPE=" % (gv.MP3.TYPE.BYTES[typeName], typeName)


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    # return outLines
