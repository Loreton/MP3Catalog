#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os
import ast


##############################################################
# - 1. Leggiamo la rootSourceDir
# - 2. Inseriamo ogni file nel dictionary
##############################################################
def Merge(gv, sourceDir, songDict, attributeNames ):
    logger  = gv.Ln.SetLogger(package=__name__)
    C      = gv.Ln.LnColor()

    changes = 0
        # ---------------------------------------
        # - lettura directory sorgente di MP3
        # ---------------------------------------
    listaFile = gv.Ln.DirList(sourceDir, patternLIST=['*.mp3'], onlyDir=False, maxDeep=99)
    if listaFile == []:
        gv.Ln.Exit(43, 'non sono stati trovati file nella directory indicata: {0}'.format(sourceDir))

    logger.info('sono stati individuati {0} file.mp3'.format(len(listaFile)))
        # ============================================
        # - inserimento...nuove canzoni
        # ============================================
    firstRelField = len(sourceDir.split(os.path.sep)) # numero del qualificatore subito dopo la sourceDir
    newEntryCount = 0
    ERRORS = 0
    for absName in listaFile:
        line            = absName.rsplit('.', 1)[0]                       # elimina extension
        relativeName    = line.split(os.path.sep)[firstRelField:]    # elimina rootDir
        if relativeName[0].startswith('@'): continue
        if not relativeName[0] in gv.ini.MAIN.songType: continue   # la dir non rientra tra quelle previste

            # --------------------------------------------------
            # - inserimento canzone
            # - Se non contiene gli attributi vuol dire che
            # - è stata appena creata, inseriamo gli attributi
            # --------------------------------------------------
        ptr = songDict.Ptr(relativeName, create=True)
        if not attributeNames[0] in ptr:
            newEntryCount += 1
            msg = '     new entry...: flds:[{0:02}] - {1}'.format( len(relativeName), relativeName)
            logger.debug(msg)
            # display dei primi campi della canzone con
            # evidenza di eventuali errori
            C.printYellow('new entry...:', tab=12, end='')
            if not len(relativeName) == firstRelField:
                C.printYellowH(' flds:[{0:02} of {1:02}]'.format(len(relativeName),firstRelField ), end='')
                ERRORS = 1
            else:
                C.printYellow(' flds:[{0:02} of {1:02}]'.format(len(relativeName),firstRelField ), end='')
            C.printYellow(' - {0}'.format(relativeName))


            # msg = " numero campi diversi???? - Verifica..."

            # if not len(relativeName) == firstRelField:
            #     msg = " numero campi diversi???? - Verifica..."
            #     C.printMagentaH(msg, tab=12)
            #     ERRORS = 1

                # su ogni canzone mettiamo i vari attributi di default
            for attributeName in attributeNames:
                ptr[attributeName] = '_'
            changes += 1
                # - campi integer
            # ptr['Song Size'] = 0

    if ERRORS:
        changes = 0
        msg = " correggere prima gli errori..."
        C.printRedH(msg, tab=12)

    logger.info('sono stati individuati {0} new entry'.format(newEntryCount))
    return changes