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
    logger = gv.Ln.SetLogger(package=__name__)
    c = gv.Ln.LnColor()

    col = gv.Prj.enumCols(gv, RECs[0])
    nCols = len(col)

    copySong                 = gv.Ln.LnDict()
    copySong.currDirNo       = 0
    copySong.nAvailDirs      = gv.INPUT_PARAM.numDirs    # counter per tenere conto delle dir non ancora riempite
    copySong.dirLIMIT        = gv.INPUT_PARAM.maxBytes
    copySong.totalSongs      = len(RECs[1:])
    copySong.remainingSongs  = copySong.totalSongs

    NOTFOUND    = []; copySong.NOTFOUND = NOTFOUND
    copiedSongs = []


    DISPLAY_LEN=55
    for index, song in enumerate(RECs[1:]):
        if copySong.nAvailDirs < 1:
            print ('Abbiamo raggiunto il limite per tutte le directories.')
            break

        if len(song) != nCols: continue
        if gv.INPUT_PARAM.maxSongs and index > gv.INPUT_PARAM.maxSongs: break
        type(song[col.SongSize])

        if isinstance(song[col.SongSize], int):
            recSongSize = song[col.SongSize]
        elif isinstance(song[col.SongSize], str):
            recSongSize = int(song[col.SongSize].replace('bytes', '').replace('.', ''))

        sourceSongName = os.path.join(
                                    gv.INPUT_PARAM.MP3SourceDir,
                                    song[col.Type],
                                    song[col.AuthorName],
                                    song[col.AlbumName],
                                    song[col.SongName].strip() + '.mp3')

        sourceRootDirLen=len(gv.INPUT_PARAM.MP3SourceDir + song[col.Type]) +1
        c.printGreen ('{FILE:<{LEN}}'.format(FILE=sourceSongName[sourceRootDirLen:sourceRootDirLen+DISPLAY_LEN:], LEN=DISPLAY_LEN), end='', tab=4)

            # ---------------------------------
            # - se la canzone sorgente esiste....
            # ---------------------------------
        if os.path.isfile(sourceSongName):
            realSongSize = os.path.getsize(sourceSongName)      # in bytes
            copySong.currDirNo += 1
            if copySong.currDirNo > gv.INPUT_PARAM.numDirs:
                    copySong.currDirNo = 1

                # - identifichiamo il numero della dir di dest....
            DirTree = 'dir-{0:02}'.format(copySong.currDirNo)
            if not DirTree in copySong:
                copySong[DirTree] = gv.Ln.LnDict()
                copySong[DirTree].nSongs  = 0
                copySong[DirTree].totSize = 0
                copySong[DirTree].full = False

                # - Se la dir è piena salta
            if copySong[DirTree].full == True: continue


                # - se MAXBYTES > LIMIT lock directory
            destDir = gv.INPUT_PARAM.destDIR + '-{0:02}'.format(copySong.currDirNo)
            if copySong.dirLIMIT > 0:
                if copySong[DirTree].totSize + realSongSize > copySong.dirLIMIT:

                    c.printCyanH("""--> {DIR} - maxByte limit reached: {CURSIZE:,} of {LIMIT:,}""".format(
                                    LIMIT=copySong.dirLIMIT,
                                    CURSIZE=copySong[DirTree].totSize,
                                    DIR=destDir),
                                    tab=4)

                    c.printYellow('...skipped, songSize: {0:,}'.format(realSongSize), tab=60)
                    copySong[DirTree].full = True
                    copySong.nAvailDirs      -= 1
                    continue

                # - prepariamo il nome del file di dest.
            destSongName = os.path.join(  gv.INPUT_PARAM.destDIR, '{0:02}'.format(copySong.currDirNo),
                                          song[col.AuthorName],
                                          song[col.SongName].strip() + '.mp3')


            destRootDirLen=len(gv.INPUT_PARAM.destDIR)
            c.printCyan('--> {FILE:<{LEN}}'.format(FILE=destSongName[destRootDirLen:destRootDirLen+DISPLAY_LEN], LEN=DISPLAY_LEN), end=' ', tab=4)

                # - copiamo la canzone... se non esiste
            isCopied = copia(gv, sourceSongName, destSongName)


                # - aggiorniamo i contatori
            if isCopied:
                copySong[DirTree].nSongs  += 1
                copySong.remainingSongs   -= 1
                copySong[DirTree].totSize += realSongSize


        else:
            c.printERROR(' - not FOUND'.format(FILE=sourceSongName), tab=4)
            NOTFOUND.append(sourceSongName)

    return copySong



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


