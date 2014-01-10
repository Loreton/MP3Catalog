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
def getAuthorName(gv, typeName, authorName):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))

    bPrefixSong         =  gv.CONFIG.EXTRACT_SECTION['PrefixSong']     # Mette <N.Cognome-> dell'autore prima del titolo della canzone All'interno del folder Type
    prefixStatic        =  gv.CONFIG.EXTRACT_SECTION['Prefissi particolari']



    token = authorName.split(' ')
    nTokens = len(token)
    lastTok  = token[-1].strip()
    firstTok = token[0].strip()

    # print typeName, authorName, lastTok, firstTok

    if authorName in prefixStatic:
        prefixSongName = prefixStatic[authorName]

    elif nTokens == 1:
        prefixSongName = "%s" % (lastTok)

    elif nTokens >= 2:
        if typeName.lower() == 'italiani':
            prefixSongName = "%s.%s" % (firstTok, lastTok[0])
        else:
            prefixSongName = "%s.%s" % (lastTok, firstTok[0])

    else:
        prefixSongName = authorName.strip()

    # print prefixSongName
    return prefixSongName