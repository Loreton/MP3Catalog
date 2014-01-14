#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os
import unicodedata, random


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


    percentREQ          = gv.CONFIG.EXTRACT_SECTION['FIELD_PERCENT_REQ_PERC']
    percentCALC         = gv.CONFIG.EXTRACT_SECTION['FIELD_PERCENT_CALC_PERC']
    percentMAXBYTES     = gv.CONFIG.EXTRACT_SECTION['FIELD_PERCENT_MAXBYTES']
    percentCOPIEDBYTES  = gv.CONFIG.EXTRACT_SECTION['FIELD_PERCENT_COPIEDBYTES']
    percentREAL         = gv.CONFIG.EXTRACT_SECTION['FIELD_PERCENT_REAL_PERC']


    destMP3Dir         =  gv.CONFIG.EXTRACT_SECTION['MP3 Destination Directory']
    sExtractOrder       =  gv.CONFIG.EXTRACT_SECTION['Extraction Order']
    # bPrefixSong         =  gv.CONFIG.EXTRACT_SECTION['PrefixSong']     # Mette <N.Cognome-> dell'autore prima del titolo della canzone All'interno del folder Type
    # bRecomended         =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
    # fillDISK            =  gv.CONFIG.EXTRACT_SECTION['FILL_DISK']


    fld = gv.EXCEL.columnName
    nSongs = 0
    writtenSongs = 0

    # -----------------------------------------------
    # - Shuffling
    # -----------------------------------------------
    # LN.file.writeListToFile(gv, destMP3Dir+os.sep+'1_beforeShuffle.txt', inpList, append=False)
    # for line in inpList: print line
    for xx in range(1,21):
        random.shuffle( inpList )                             # Crea range-shuffled
    # for line in inpList: print line
    # LN.file.writeFile(gv, destMP3Dir+os.sep+'2_afterShuffle.txt', inpList, append=False)

    for index, song in enumerate(inpList):
        nSongs += 1
        if song == '': continue

        # -------------------------------------------------------------------------------------------------------------
        # DEVO fare tutte le verifiche preliminari per capire se devo copiare o meno la canzone sulla destinazione
        # -------------------------------------------------------------------------------------------------------------
        typeName    = unicodedata.normalize('NFKD', song[fld.TYPE]).encode('ascii', 'ignore')
        authorName  = unicodedata.normalize('NFKD', song[fld.AUTHOR_NAME]).encode('ascii', 'ignore')
        songSize    = int(song[fld.SONG_SIZE])

        # yy = hasattr(gv.COPY.COPIED_BYTES, typeName) # non funziona nel dictionary
        if gv.COPY.COPIED_BYTES.get(typeName) == None:      gv.COPY.COPIED_BYTES[typeName]   = 0
        if gv.COPY.AUTHOR_SONGS.get(authorName) == None:    gv.COPY.AUTHOR_SONGS[authorName] = [False, 0] # Reached, numberSongs


        percentDICT    = gv.CONFIG.EXTRACT_SECTION['PERCENT']
        maxAuthorSongs = gv.CONFIG.EXTRACT_SECTION['MAX_AUTHORS_SONGS'].get(authorName, gv.CONFIG.EXTRACT_SECTION['MAX_AUTHORS_SONGS']['DEFAULT'])

        bytesMaxForType     = percentDICT[typeName][percentMAXBYTES]
        bytesCopiedForType  = percentDICT[typeName][percentCOPIEDBYTES]

            # ------------------------------------------------------------------------------
            # - TEST del FREE Disk SPACE
            # - E' stato inserito con un IF  altrimenti rallentava molto su USB drive
            # - Consideriamo uno spazio libero = SongSize + 5MB
            # ------------------------------------------------------------------------------
        if nSongs%100 == 0 or gv.COPY.driveFreeSpace==None:
            gv.COPY.driveFreeSpace = LN.file.driveSpace(gv, destMP3Dir, 'Bytes')
        if gv.CONFIG.EXTRACT_SECTION['FILL_DISK'] and gv.COPY.driveFreeSpace < (songSize+5*1024*1024):
            Prj.exit(gv, 4444,  "No more FreeSPACE [%d] is available on output drive." % (gv.COPY.driveFreeSpace))

            # ------------------------------------------------------------------------------
            # - TEST delle canzoni copiate per ogni Autore
            # - gv.COPY.AUTHOR_SONGS[authorName][0] - True indica che è stato raggiunto il massimo
            # - gv.COPY.AUTHOR_SONGS[authorName][1] - Numero di canzoni copiate
            # ------------------------------------------------------------------------------
        elif gv.COPY.AUTHOR_SONGS[authorName][0]: # E' già stato raggiunto il massimo?
            continue
        elif gv.COPY.AUTHOR_SONGS[authorName][1] >= maxAuthorSongs:
            gv.COPY.AUTHOR_SONGS[authorName][0] = True
            logger.console(LN.cRED + "MAX SONGs [%d] has been reached for Author:[%s]" % (gv.COPY.AUTHOR_SONGS[authorName][1], authorName))
            continue


            # ------------------------------------------------------------------------------
            # - TEST dei bytes copiati per ogni TYPE
            # ------------------------------------------------------------------------------
        elif bytesMaxForType < 1:
            continue

        elif bytesCopiedForType >= bytesMaxForType:
            percentDICT[typeName][percentMAXBYTES] = 0
            logger.console(LN.cRED + "MAX BYTES [%d] has been reached for TYPE=%s" % (bytesMaxForType, typeName))
            continue

            # ------------------------------------------------------------------------------
            # - Copiamo la canzone
            # ------------------------------------------------------------------------------
        else:
            rCode = Prj.mp3.copySongToDest(gv, song)
            if rCode:
                gv.COPY.COPIED_BYTES[typeName]              += songSize
                percentDICT[typeName][percentCOPIEDBYTES]   += songSize
                gv.COPY.AUTHOR_SONGS[authorName][1]         += 1
                gv.COPY.driveFreeSpace                      -= songSize
                writtenSongs                                += 1
                inpList[index]                              = ''



    # Compressione della LIST
    inpList = [item for item in inpList if item != '']
    # LN.file.writeFile(gv, destMP3Dir+os.sep+'3_completed.txt', inpList, append=False)
    # for line in inpList: print "AVANZI____: %-90s %5d %s" % (os.path.sep.join(line[:4]), int(line[4]), line[5])
    for line in inpList: print "AVANZI____: %-90s" % (os.path.sep.join(line[:4])), line[4], line[5]

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return writtenSongs, len(inpList)


