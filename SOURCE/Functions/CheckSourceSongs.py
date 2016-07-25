#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys

def checkSourceSongs(gv, RECs):
    TAByel      = gv.Ln.cYELLOW + ' '*8
    TABerr      = gv.Ln.cERROR + ' '*8
    TABcyan     = gv.Ln.cCYAN + ' '*8
    TABgreen    = gv.Ln.cGREEN + ' '*8
    cYEL        = gv.Ln.cYELLOW
    cCYAN       = gv.Ln.cCYAN
    cGREEN      = gv.Ln.cGREEN
    cRESET      = gv.Ln.cRESET


    col = gv.Prj.enumCols(gv, RECs[0])
    nCols = len(col)

    NOTFOUND = []
    for index, song in enumerate(RECs[1:]):
        if len(song) != nCols: continue
        if index > 1000: break
        sourceSongName = os.path.join(  gv.INPUT_PARAM.sourceDIR,
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
        msg = 'The following songs are not found'
    else:
        msg = 'ALL the songs were found on source directory'

    print (msg)
    for index, song in enumerate(NOTFOUND):
        print ('{INX:04}{COLOR}"{FILE}"'.format(COLOR=TAByel, INX=index, FILE=song))
    print ()

