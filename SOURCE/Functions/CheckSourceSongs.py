#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys

def checkSourceSongs(gv, RECs):
    logger = gv.Ln.setLogger(package=__name__, CONSOLE=gv.INPUT_PARAM.LogCONSOLE)
    color  = gv.Ln.Colors()

    col = gv.Prj.enumCols(gv, RECs[0])
    nCols = len(col)
    logger.info('numero colonne trovate: {0}'.format(nCols))

    NOTFOUND = []
    # logger.info('numero record : {0}'.format(len(RECs[1:])))

    for index, song in enumerate(RECs[1:]):
        if len(song) != nCols: continue
        if gv.INPUT_PARAM.maxSongs and index > gv.INPUT_PARAM.maxSongs: break
        sourceSongName = os.path.join(gv.INPUT_PARAM.sourceDIR,
                                    song[col.Type],
                                    song[col.AuthorName],
                                    song[col.AlbumName],
                                    song[col.SongName] + '.mp3')

        sourceSongName = sourceSongName.replace('Rondó', 'Rondò')
        if not os.path.isfile(sourceSongName):
            NOTFOUND.append(sourceSongName)

    # The following songs are not found
    print ()
    if NOTFOUND:
        nSongs = len(NOTFOUND)
        msg = color.RED08 + 'The following songs [{nSONGS}] are not found in the source directory'.format(nSONGS=nSongs)
    else:
        nSongs = index -1
        msg = color.YELLOW08 + 'ALL the songs [{nSONGS}] were found in the source directory'.format(nSONGS=nSongs)

    print (msg)
    for index, song in enumerate(NOTFOUND):
        print ('{COLOR1}{INX:04} - {COLOR2}"{FILE}"'.format(COLOR2=color.YELLOW, COLOR1=color.RED, INX=index+1, FILE=song))
    print ()

