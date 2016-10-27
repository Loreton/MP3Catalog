#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import shutil

def copySongs(gv, RECs):
    global c, copiedSongs
    logger = gv.Ln.setLogger(gv, package=__name__)
    c = gv.Ln.Colors()

    col = gv.Prj.enumCols(gv, RECs[0])
    nCols = len(col)

    gv.copySong                 = gv.Ln.LnDict()
    gv.copySong.currDirNo       = 0
    gv.copySong.nAvailDirs      = gv.INPUT_PARAM.numDirs    # counter per tenere conto delle dir non ancora riempite
    gv.copySong.dirLIMIT        = gv.INPUT_PARAM.maxBytes
    gv.copySong.totalSongs      = len(RECs[1:])
    gv.copySong.remainingSongs  = gv.copySong.totalSongs

    '''
        gv.copySong['dir01'].totSize    = 1
        gv.copySong['dir01'].nSongs     = 1
        gv.copySong.currDirNo           = 1
        gv.copySong.nAvailDirs          = 1
    '''

    NOTFOUND = []
    copiedSongs = []


    DISPLAY_LEN=50
    for index, song in enumerate(RECs[1:]):
        if gv.copySong.nAvailDirs < 1:
            print ('Abbiamo raggiunto il limite per tutte le directories.')

            break

        if len(song) != nCols: continue
        if gv.INPUT_PARAM.maxSongs and index > gv.INPUT_PARAM.maxSongs: break

        recSongSize = int(song[col.SongSize].replace('bytes', '').replace('.', ''))

        sourceSongName = os.path.join(  gv.INPUT_PARAM.sourceDIR,
                                    song[col.Type],
                                    song[col.AuthorName],
                                    song[col.AlbumName],
                                    song[col.SongName] + '.mp3')


        c.printGreen ('{FILE:<{LEN}}'.format(LEN=DISPLAY_LEN,FILE=sourceSongName[-DISPLAY_LEN:]), end='', tab=4)

            # ---------------------------------
            # - se la canzone sorgente esiste....
            # ---------------------------------
        if os.path.isfile(sourceSongName):
            realSongSize = os.path.getsize(sourceSongName)      # in bytes
            gv.copySong.currDirNo += 1
            if gv.copySong.currDirNo > gv.INPUT_PARAM.numDirs:
                    gv.copySong.currDirNo = 1

                # - identifichiamo il numero della dir di dest....
            DirTree = 'dir-{0:02}'.format(gv.copySong.currDirNo)
            if not DirTree in gv.copySong:
                gv.copySong[DirTree] = gv.Ln.LnDict()
                gv.copySong[DirTree].nSongs  = 0
                gv.copySong[DirTree].totSize = 0
                gv.copySong[DirTree].ready = True

                # - Se la dir è piena salta
            if gv.copySong[DirTree].ready == False: continue

                # - se MAXBYTES > LIMIT lock directory
            destDir = gv.INPUT_PARAM.destDIR + '-{0:02}'.format(gv.copySong.currDirNo)
            if gv.copySong.dirLIMIT > 0:
                if gv.copySong[DirTree].totSize + realSongSize > gv.copySong.dirLIMIT:

                    c.printCyanH("""--> {DIR} - maxByte limit reached: {CURSIZE:,} of {LIMIT:,}""".format(
                                    LIMIT=gv.copySong.dirLIMIT,
                                    CURSIZE=gv.copySong[DirTree].totSize,
                                    DIR=destDir),
                                    tab=4)

                    c.printYellow('...skipped, songSize: {0:,}'.format(realSongSize), tab=60)
                    gv.copySong[DirTree].ready = False
                    gv.copySong.nAvailDirs      -= 1
                    continue

                # - prepariamo il nome del file di dest.
            destSongName = os.path.join(  gv.INPUT_PARAM.destDIR, '{0:02}'.format(gv.copySong.currDirNo),
                                          song[col.AuthorName],
                                          song[col.SongName] + '.mp3')


                # - copiamo la canzone... se non esiste


            c.printCyan('--> {FILE:<{LEN}}'.format(LEN=DISPLAY_LEN,FILE=destSongName[:DISPLAY_LEN]), end=' ', tab=4)
            isCopied = copia(gv, sourceSongName, destSongName)


                # - aggiorniamo i contatori
            if isCopied:
                gv.copySong[DirTree].nSongs  += 1
                gv.copySong.remainingSongs   -= 1
                gv.copySong[DirTree].totSize += realSongSize


        else:
            c.printERROR(' - not FOUND'.format(FILE=sourceSongName), tab=4)
            NOTFOUND.append(sourceSongName)





def copia(gv, sourceSongName, destSongName):
    isCopied = False
    if gv.INPUT_PARAM.fEXECUTE:
        destdir = os.path.dirname(destSongName)
        if not os.path.exists(destdir): os.makedirs(destdir)

        action = c.getYellow('...copyied', tab=4)

        if os.path.isfile(destSongName):
            gv.songList.duplicate.append(sourceSongName)
            sourceSongSize = os.path.getsize(sourceSongName)
            destSongSize = os.path.getsize(destSongName)
            # - check songSize
            if sourceSongSize == destSongSize:
                c.printRedH('...skipped - same size', tab=4)
                return isCopied

            # - proviamo a fare il rename
            fname = destSongName.split('.mp3')[0]
            FOUND = True
            counter = 0
            while FOUND==True:
                counter += 1
                destSongName = '{FNAME}-{COUNTER:03}.mp3'.format(FNAME=fname, COUNTER=counter)
                FOUND = os.path.isfile(destSongName)
            action = c.getRedH('...renamed - {COUNTER:03}'.format(COUNTER=counter), tab=4)


        try:
            shutil.copyfile(sourceSongName, destSongName)

        except (IOError, os.error) as why:
            msg = "Can't COPY [{0}] to [{1}]: {3}".format(sourceSongName, destSongName, str(why))
            print (msg)
            sys.exit()


        print (action)
        copiedSongs.append(destSongName)
        isCopied = True
        return isCopied

    else:   # siamo in dry-run mode
        if destSongName in copiedSongs:
            c.printRedH('...duplicate', tab=4)
            gv.songList.duplicate.append(sourceSongName)
            return False

        else:
            copiedSongs.append(destSongName)
            c.printYellow('...will be copied', tab=4)
            return True


