#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys

def copySongs(gv, RECs):
    logger = gv.Ln.setLogger(package=__name__, CONSOLE=gv.INPUT_PARAM.LogCONSOLE)
    C = gv.Ln.Colors()

    col = gv.Prj.enumCols(gv, RECs[0])
    nCols = len(col)

    # gv.copySong = gv.Ln.LnDict(_dynamic=True)
    # gv.INPUT_PARAM.printDict(gv)
    # sourceDir   = gv.INPUT_PARAM.sourceDIR
    # destDir     = gv.INPUT_PARAM.destDIR
    gv.copySong = gv.Ln.LnDict()
    gv.copySong.currDirNo   = 0
    gv.copySong.nAvailDirs  = gv.INPUT_PARAM.numDirs    # counter per tenere conto delle dir non ancora riempite
    '''
        gv.copySong['dir01'].totSize    = 1
        gv.copySong['dir01'].nSongs     = 1
        gv.copySong.currDirNo           = 1
        gv.copySong.nAvailDirs          = 1
    '''

    NOTFOUND = []


    for index, song in enumerate(RECs[1:]):
        if gv.copySong.nAvailDirs < 1:
            print ('Abbiamo raggiunto il limite per tutte le directories.')
            break

        if len(song) != nCols: continue
        if gv.INPUT_PARAM.maxSongs and index > gv.INPUT_PARAM.maxSongs: break

        songSize = int(song[col.SongSize].replace('bytes', '').replace('.', ''))


        # sourceSongNameDisplay = os.path.join(song[col.AuthorName], song[col.SongName] + '.mp3')


        sourceSongName = os.path.join(  gv.INPUT_PARAM.sourceDIR,
                                    song[col.Type],
                                    song[col.AuthorName],
                                    song[col.AlbumName],
                                    song[col.SongName] + '.mp3')


        DISPLAY_LEN=50
        print (C.GREEN04 + '{FILE:<{LEN}}'.format(LEN=DISPLAY_LEN,FILE=sourceSongName[-DISPLAY_LEN:]), end=' ')

            # ---------------------------------
            # - se la canzone sorgente esiste....
            # ---------------------------------
        if os.path.isfile(sourceSongName):
            gv.copySong.currDirNo += 1
            if gv.copySong.currDirNo > gv.INPUT_PARAM.numDirs:
                    gv.copySong.currDirNo = 1

                # - identifichiamo il numero della dir di dest....
            DirTree = 'dir-{0:02}'.format(gv.copySong.currDirNo)
            if not DirTree in gv.copySong:
                gv.copySong[DirTree] = gv.Ln.LnDict()
                gv.copySong[DirTree].nSongs  = 0
                gv.copySong[DirTree].totSize = 0

                # - Verifichiamo di non aver raggiunto il MAXBYTES
                # - per la spewcifica dir
            destDir = gv.INPUT_PARAM.destDIR + '-{0:02}'.format(gv.copySong.currDirNo)
            if gv.copySong[DirTree].totSize + songSize > gv.INPUT_PARAM.maxBytes:
                print(C.YELLOW04 + '...skipped, songSize:{0:,}'.format(songSize))
                print ()
                print(C.CYAN04 + """maxByte limit has been reached: {LIMIT:,}
                    for the directory: {DIR}
                    """.format(LIMIT=gv.copySong[DirTree].totSize, DIR=destDir))
                gv.copySong.nAvailDirs      -= 1
                continue

                # - prepariamo il nome del file di dest.
            destSongName = os.path.join(  gv.INPUT_PARAM.destDIR + '-{0:02}'.format(gv.copySong.currDirNo),
                                          song[col.AuthorName],
                                          song[col.SongName] + '.mp3')


                # - copiamo la canzone... se non esiste
            '''
             .........
            '''

                # - aggiorniamo i contatori
            gv.copySong[DirTree].nSongs  += 1

            gv.copySong[DirTree].totSize += songSize



            print(C.CYAN04 + '--> {FILE:<{LEN}}'.format(LEN=DISPLAY_LEN,FILE=destSongName[:DISPLAY_LEN]), end=' ')
            print(C.YELLOW04 + '...copyied')


        else:
            print (C.ERROR04 + ' - not FOUND'.format(FILE=sourceSongName))
            NOTFOUND.append(sourceSongName)



    gv.copySong.printDict(gv)
    sys.exit()

