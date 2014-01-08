#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os


# #############################################################
# = Estrae le canzoni dal dictionary oppure dalla inpList[]
# = Le canzoni devono rientrare nei criteri impostati nella ExtractSEction del file.cfg
# #############################################################
def extractSong(gv, inpList=None):
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


    minPunteggio = min(lPunteggioRange)
    maxPunteggio = max(lPunteggioRange)
    if inpList:
        outLines = []
        fld = gv.EXCEL.columnName
        for line in inpList:
               # if valore in Punteggi:
            valore = int(line[fld.PUNTEGGIO])
            if valore >= minPunteggio and valore <= maxPunteggio:
                outLines.append(line)

    else:
        fld = gv.EXCEL.songAttrName
        outDict = {}
        for typeName in gv.MP3Dict.keys():
            authorDICT = gv.MP3Dict.get(typeName)
            for authorName in authorDICT.keys():
                albumDICT = authorDICT.get(authorName)
                for albumName in albumDICT.keys():
                    songDICT = albumDICT.get(albumName)

                    for songName, val in songDICT.items():
                            # if valore in Punteggi:
                        valore = int(val[fld.PUNTEGGIO])
                        if valore >= minPunteggio and valore <= maxPunteggio:
                            currAlbumPtr = LN.dict.getDictPtr(gv, outDict, keyList=[typeName, authorName, albumName], fCREATE=True)
                            currAlbumPtr[songName] = val

        outLines = LN.dict.dictionaryToList(gv, outDict, MaxDeepLevel=99)


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return outLines
