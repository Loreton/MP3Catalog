#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os
import unicodedata


# ############################################################################################
# = Copia le canzoni con il FLAG di Mandatory
# = RETURN: LIST[] delle canzoni rimaste.
# ############################################################################################
def processSongs(gv, inpList=[]):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))

    configID            = gv.CONFIG.EXTRACT_SECTION
    MP3baseDir          = gv.CONFIG.MP3_BASE_DIR
    MP3baseDirLen       = len(MP3baseDir) + 1

    destMP3Dir         =  gv.CONFIG.EXTRACT_SECTION['MP3 Destination Directory']
    sExtractOrder       =  gv.CONFIG.EXTRACT_SECTION['Extraction Order']
    bPrefixSong         =  gv.CONFIG.EXTRACT_SECTION['PrefixSong']     # Mette <N.Cognome-> dell'autore prima del titolo della canzone All'interno del folder Type
    bRecomended         =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
    fillDISK            =  gv.CONFIG.EXTRACT_SECTION['FILL_DISK']


    fld = gv.EXCEL.columnName
    nSongs = 0
    writtenSongs = 0
    for index, song in enumerate(inpList):
        nSongs += 1
        if song == '': continue

        # -------------------------------------------------------------------------------------------------------------
        # DEVO fare tutte le verifiche preliminari per capire se devo copiare o meno la canzone sulla destinazione
        # -------------------------------------------------------------------------------------------------------------
        typeName    = unicodedata.normalize('NFKD', song[fld.TYPE]).encode('ascii', 'ignore')
        authorName  = unicodedata.normalize('NFKD', song[fld.AUTHOR_NAME]).encode('ascii', 'ignore')
        songSize    = int(song[fld.SONG_SIZE])

        # (typeName, authorName, albumName, songName) = LnSys.splitUnicode(file[baseDirLen:], os.sep)
        if not hasattr(gv.MP3.COPIED_BYTES, typeName):      gv.MP3.COPIED_BYTES[typeName]   = 0
        if not hasattr(gv.MP3.AUTHOR_SONGS, authorName):    gv.MP3.AUTHOR_SONGS[authorName] = 0
        # try:
        # except UnicodeEncodeError, why:
        #     print song
        #     print why
        #     sys.exit()

        maxAuthorSongs = gv.CONFIG.EXTRACT_SECTION['MAX_AUTHORS_SONGS'].get(authorName, gv.CONFIG.EXTRACT_SECTION['MAX_AUTHORS_SONGS']['DEFAULT'])

        bytesMaxForType     = gv.CONFIG.EXTRACT_SECTION['PERCENT'][typeName][2]
        bytesCopiedForType  = gv.CONFIG.EXTRACT_SECTION['PERCENT'][typeName][3]

            # ------------------------------------------------------------------------------
            # - TEST del FREE Disk SPACE
            # - E' stato inserito con un IF  altrimenti rallentava molto su USB drive
            # - Consideriamo uno spazio libero = SongSize + 5MB
            # ------------------------------------------------------------------------------
        if nSongs%100 == 0 or gv.MP3.driveFreeSpace==None: gv.MP3.driveFreeSpace = LN.file.driveSpace(gv, destMP3Dir, 'Bytes')
        if gv.CONFIG.EXTRACT_SECTION['FILL_DISK'] and gv.MP3.driveFreeSpace < (songSize+5*1024*1024):
            Prj.exit(gv, 4444,  "No more FreeSPACE [%d] is available on output drive." % (gv.MP3.driveFreeSpace))




            # ------------------------------------------------------------------------------
            # - TEST delle canzoni copiate per ogni Autore
            # ------------------------------------------------------------------------------
        elif gv.MP3.AUTHOR_SONGS[authorName] > maxAuthorSongs:
            print "MAX SONGs [%d] has been reached for Author=" % (gv.MP3.AUTHOR_SONGS[authorName], authorName)
            continue


            # ------------------------------------------------------------------------------
            # - TEST dei numero di bytes da copiare
            # ------------------------------------------------------------------------------
        if bytesMaxForType < 1:
            continue

            # ------------------------------------------------------------------------------
            # - TEST dei bytes copiati per ogni TYPE
            # ------------------------------------------------------------------------------
        # elif gv.MP3.COPIED_BYTES[typeName] > gv.CONFIG.EXTRACT_SECTION['PERCENT'][typeName][2]:
        elif bytesCopiedForType > bytesMaxForType:
            print "MAX BYTES [%d] has been reached for TYPE=%s" % (bytesMaxForType, typeName)

            # ------------------------------------------------------------------------------
            # - Copiamo la canzone
            # ------------------------------------------------------------------------------
        else:
            rCode = Prj.mp3.copySongToDest(gv, song)
            if rCode:
                gv.MP3.COPIED_BYTES[typeName]                       += songSize
                gv.CONFIG.EXTRACT_SECTION['PERCENT'][typeName][3]   += songSize
                gv.MP3.AUTHOR_SONGS[authorName]                     += 1
                gv.MP3.driveFreeSpace                               -= songSize
                writtenSongs                                        += 1


        inpList[index] = ''

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return writtenSongs


