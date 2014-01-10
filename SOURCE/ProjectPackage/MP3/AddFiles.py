#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os


# #############################################################
# = Inserisce una canzone nel Dictionary
# = authorName puo' essere anche un Integer (tipo 883)
# #############################################################
def addFiles(gv):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))


    configID        = gv.CONFIG.MERGE_SECTION
    dir2Scan        = configID.get('dir to scan')
    MP3baseDir      = gv.CONFIG.MP3_BASE_DIR
    MP3baseDirLen   = len(MP3baseDir) + 1
    fld             = gv.EXCEL.columnName


        # --------------------------------------------------------------------
        # - Ora facciamo lo scanning delle dirs e le aggiungiamo al DB
        # --------------------------------------------------------------------
    for dirName in dir2Scan:
        dirName = dirName.strip()
        indent = 0
        searchPattern = '*.mp3'
        logger.info("%s :Searching: [%s\\%s]" % (indent*' ', dirName, searchPattern))
        print("%s :Searching: [%s\\%s]" % (indent*' ', dirName, searchPattern))

        (rCode, fileList) = LN.file.dirList(gv, dirName, pattern=searchPattern, what='FS', getFullPath=True)
        if rCode: choice = LN.sys.getKeyboardInput(gv, "ERROR Reading directory %s (see LOG file)" % (dirName), validKeys='ENTER', exitKey='XQ', deepLevel=3, fDEBUG=False)

        counter = 0
        nFiles = len(fileList)
        for fName in fileList:
            counter += 1
            if counter%100 == 0: print "     %6d/%6d file has been processed" % (counter, nFiles)
            indent = 4                                                 # per il display/log
            row = Prj.fmt.prepareRow(gv)
            logger.debug("adding file: [%s]" % (fName))

            try:
                    # Estrazione dei campi del nome file
                (row[fld.TYPE], row[fld.AUTHOR_NAME], row[fld.ALBUM_NAME], row[fld.SONG_NAME]) = LN.sys.splitUnicode(gv, fName[MP3baseDirLen:], os.sep)

            except StandardError, why:
                Msg1 = "Il file [%s]\ncontiene piu' campi del previsto\nVerificare!! [%s]"  % (fName[MP3baseDirLen:], why)
                Prj.exit(gv, 3001, Msg1)

            row[fld.SONG_NAME] = os.path.splitext(row[fld.SONG_NAME])[0]
            row[fld.SONG_SIZE] = os.path.getsize(fName)

            Prj.mp3.insertSong(gv, gv.MP3.Dict, row)
            if row[fld.TYPE] in 'UNKNOWN EMPTY':
                choice=LN.sys.getKeyboardInput(gv, "Vuoi continuare???", validKeys="Y", exitKey='XQ')


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
