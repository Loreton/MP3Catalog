#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os
import ast


##############################################################
# - VALIDATE che tutte le entrate corrispondano ad un file
##############################################################
def Validate(gv, sourceDir, songDict, fldNames):
    logger  = gv.Ln.SetLogger(package=__name__)

        # -----------------------------------------------------------------------
        # - otteniamo una lista della struttura del dict dove ogni entry
        # - è una lista che contiene i token delle key della canzone
        # -----------------------------------------------------------------------
    keyList = songDict.KeyList()
    logger.info('andiamo a validare {0} records'.format(len(keyList)))
    """
        ['Bambini', 'Cartoni', 'The best of', 'Anna Dai Capelli Rossi']
        ['Bambini', 'Cartoni', 'The best of', 'Arale Avventura']
        ['Bambini', 'Cartoni', 'The best of', 'Arrivano I Superboys' ]
        ['Bambini', 'Cartoni', 'The best of', 'Astro Robot' ]
    """

    FLD = gv.Ln.LnEnum(fldNames, myDict=gv.Ln.LnDict)

        # -----------------------------------------------------------------------
        # - 1. verifichiamo che per la canzone esista il file.
        # - 2. Se non esiste mettiamo songSize=0 e ToBeDeleted=True
        # -     (per copiare gli attributi per poi cancellarle)
        # -----------------------------------------------------------------------
    songLIST = []  # conterrà le canzoni in formato listOfList
    filesToDelete = 0
    changes = 0
    SONGFLD = fldNames[FLD.SongSize]
    for songQualifiers in keyList:
        if songQualifiers == []: continue
        # - otteniamo il pointer alla canzone
        ptrSong = songDict.Ptr(songQualifiers)
        # - prepare newSongEntry
        mySong = songQualifiers[:]

        fileName = os.path.sep.join(songQualifiers)
        fileName = '{0}{1}{2}.mp3'.format(sourceDir, os.path.sep, fileName)

        if os.path.isfile(fileName):
            size = os.stat(fileName).st_size
            if not ptrSong[SONGFLD] == size:
                ptrSong[SONGFLD] = size
                changes += 1

        else:
            filesToDelete += 1
            # in modo che posso copiare gli attributi e poi cancellarle.
            msg = '     no more exists...{0}'.format(fileName)
            logger.debug(msg)
            print(msg)


        # ================================================
        # - Convertiamo il dict-record in una LIST
        # ================================================

            # - get song attributes values
        songAttr = ptrSong.GetValue(fPRINT=False)
        # print (songAttr)

        for attributeName, val in songAttr.items():
            mySong.append(val)
        # print (len(mySong), mySong)

        songLIST.append(mySong)

    logger.info('dovranno essere eliminati {0} records'.format(filesToDelete))
    return songLIST, changes