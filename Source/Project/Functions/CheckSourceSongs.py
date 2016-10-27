#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys

def checkSourceSongs(gv, RECs):
    logger = gv.Ln.setLogger(gv, package=__name__)
    color  = gv.Ln.Colors()

    print (len(RECs))
    print (len(RECs[1:]))
    col = gv.Prj.enumCols(gv, RECs[0])
    nCols = len(col)
    logger.info('numero colonne trovate: {0}'.format(nCols))

    NOTFOUND = []
    FOUND = []


    for index, song in enumerate(RECs[1:]):
        if gv.INPUT_PARAM.maxSongs and index > gv.INPUT_PARAM.maxSongs: break
        sourceSongName = os.path.join(gv.INPUT_PARAM.sourceDIR,
                                    song[col.Type],
                                    song[col.AuthorName],
                                    song[col.AlbumName],
                                    song[col.SongName] + '.mp3')

        if os.path.isfile(sourceSongName):
            FOUND.append(sourceSongName)
        else:
            NOTFOUND.append(sourceSongName)

    print ()
    if NOTFOUND:
        nSongs = len(NOTFOUND)
        msg = color.getRedH('The following songs [{nSONGS}] are not found in the source directory'.format(nSONGS=nSongs), tab=8)
    else:
        nSongs = len(FOUND)
        msg = color.getYellow('ALL the songs [{nSONGS}] were found in the source directory'.format(nSONGS=nSongs), tab=8)

    print (msg)
    for index, song in enumerate(NOTFOUND):
        print ('{COLOR1}{INX:04} - {COLOR2}"{FILE}"'.format(COLOR2=color.YELLOW, COLOR1=color.RED, INX=index+1, FILE=song))
    print ()

