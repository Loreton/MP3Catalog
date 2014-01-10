#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os


# ############################################################################################
# = Estrae le canzoni dal dictionary oppure dalla inpList[]
# = Le canzoni devono rientrare nel punteggio impostato nella ExtractSEction del file.cfg
# = RETURN: LIST[] delle canzoni individuate.
# ############################################################################################
def extractSongs(gv, inpList=None):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))


    lPunteggioRange     =  gv.CONFIG.EXTRACT_SECTION['Punteggi']
    bRecomended         =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']


    minPunteggio = min(lPunteggioRange)
    maxPunteggio = max(lPunteggioRange)

    randomSONGS     = []
    mandatorySONGS  = []

        # - Estrazione da una LIST
    if inpList:
        nSongs = len(inpList)
        fld = gv.EXCEL.columnName
        for line in inpList:

            isRECOMENDED    = True if line[fld.RECOMENDED] != '.' else False
            valore          = int(line[fld.PUNTEGGIO])

            if bRecomended and isRECOMENDED:
                mandatorySONGS.append(line)

            elif (valore >= minPunteggio and valore <= maxPunteggio):
                randomSONGS.append(line)

            else:
                pass
                # print "skipped....", line


        # - Estrazione da un DICT
    else:
        nSongs = 0          # counter
        fld = gv.EXCEL.songAttrName
        for typeName in gv.MP3.Dict.keys():
            authorDICT = gv.MP3.Dict.get(typeName)
            for authorName in authorDICT.keys():
                albumDICT = authorDICT.get(authorName)
                for albumName in albumDICT.keys():
                    songDICT = albumDICT.get(albumName)

                    for songName, val in songDICT.items():
                        nSongs += 1
                        isRECOMENDED    = True if val[fld.RECOMENDED] != '.' else False
                        valore          = int(val[fld.PUNTEGGIO])

                        songLine = [typeName, authorName, albumName, songName]
                        songLine.extend(val)
                        if bRecomended and isRECOMENDED:
                            mandatorySONGS.append(songLine)

                        elif (valore >= minPunteggio and valore <= maxPunteggio):
                            randomSONGS.append(songLine)

                        else:
                            pass
                            # print "skipped...."

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))

    # print nSongs, len(mandatorySONGS), len(randomSONGS)
    return mandatorySONGS, randomSONGS
