#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys



def copySongs(gv, RECs):
    TAByel      = gv.Ln.cYELLOW + ' '*8
    TABerr      = gv.Ln.cERROR + ' '*8
    TABcyan     = gv.Ln.cCYAN + ' '*8
    cYEL        = gv.Ln.cYELLOW
    cCYAN       = gv.Ln.cCYAN
    cGREEN      = gv.Ln.cGREEN
    cRESET      = gv.Ln.cRESET


    col = gv.Prj.enumCols(gv, RECs[0])
    nCols = len(col)

    # gv.INPUT_PARAM.printDict(gv)
    # sourceDir   = gv.INPUT_PARAM.sourceDIR
    # destDir     = gv.INPUT_PARAM.destDIR
    NOTFOUND = []
    for index, song in enumerate(RECs[1:]):
        if len(song) != nCols: continue
        if index > 1000: break


        # sourceSongName = '{BASEDIR}/{}'.format()
        sourceSongNameDisplay = os.path.join(song[col.AuthorName], song[col.SongName] + '.mp3')

        # sourceSongName = os.path.join(  gv.INPUT_PARAM.sourceDIR, sourceSongNameRel)

        sourceSongName = os.path.join(  gv.INPUT_PARAM.sourceDIR,
                                    song[col.Type],
                                    song[col.AuthorName],
                                    song[col.AlbumName],
                                    song[col.SongName] + '.mp3')

        destSongName = os.path.join(  gv.INPUT_PARAM.destDIR,
                                        song[col.AuthorName],
                                        song[col.SongName] + '.mp3')

        MAXLEN=40
        print (cGREEN + 'song: {FILE:<{LEN}}'.format(LEN=MAXLEN,FILE=sourceSongNameDisplay[-MAXLEN:]), end=' ')
        if os.path.isfile(sourceSongName):
            print(TABcyan + '--> {FILE:<{LEN}}'.format(LEN=MAXLEN,FILE=destSongName[-MAXLEN:]), end=' ')
            # print(TABcyan + '...copying', end=' ')
            pass
            print(TAByel + '...copyied')
        else:
            print (TABerr + ' - not FOUND'.format(FILE=sourceSongName))
            NOTFOUND.append(sourceSongName)


