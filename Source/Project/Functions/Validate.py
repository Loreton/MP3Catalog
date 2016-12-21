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
def Validate(gv, sourceDir, songDict ):
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

        # -----------------------------------------------------------------------
        # - 1. verifichiamo che per la canzone esista il file.
        # - 2. Se non esiste mettiamo songSize=0 e ToBeDeleted=True
        # -     (per copiare gli attributi per poi cancellarle)
        # -----------------------------------------------------------------------
    songLIST = []  # conterrà le canzoni in formato listOfList
    filesToDelete = 0
    for songQualifiers in keyList:
        if songQualifiers == []: continue
        # - otteniamo il pointer alla canzone
        ptrSong = songDict.Ptr(songQualifiers)
        # - prepare newSongEntry
        mySong = songQualifiers[:]
        SONGNAME_FLD = 3

        fileName = os.path.sep.join(songQualifiers)
        fileName = '{0}{1}{2}.mp3'.format(sourceDir, os.path.sep, fileName)


        if os.path.isfile(fileName):
            size = os.stat(fileName).st_size
            ptrSong['Song Size'] = size

        else:
            # suffix = '_TO_BE_DELETED'
            # if not songQualifiers[SONGNAME_FLD].endswith(suffix):
            #     mySong[SONGNAME_FLD] = songQualifiers[SONGNAME_FLD] + suffix
            filesToDelete += 1
            # in modo che posso copiare gli attributi e poi cancellarle.
            msg = '     no more exists...{0}'.format(fileName)
            logger.debug(msg)
            print(msg)

            # msg = '     renamed to...{0}'.format(mySong)
            # logger.debug(msg)
            # print(msg)


        # ================================================
        # - Convertiamo il dict-record in una LIST
        # ================================================

            # - get song attributes values
        songAttr = ptrSong.GetValue(fPRINT=False)

        for attributeName, val in songAttr.items():
            mySong.append(val)

        songLIST.append(mySong)

    logger.info('dovranno essere eliminati {0} records'.format(filesToDelete))
    return songLIST