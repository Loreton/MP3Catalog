#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys; sys.dont_write_bytecode = True

# ###############################################################
# - calcola():
# ###############################################################
def ReadIniData(gv):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy

    logger.info('entered - [called by:{0}]'.format(calledBy(1)))
    try:
        SectID = gv.INI.configParser['EXTRACT']
        gv.extract.MP3DestDir           = SectID['MP3 Destination Directory']
        gv.extract.Mandatory            = SectID['Recomended - Mandatory']
        gv.extract.prefixSong           = SectID['PrefixSong']


        gv.extract.maxSongs             = int(SectID['MAX_SONGS'])
        gv.extract.maxOutDirSize        = int(SectID['MAX_OUT_DIR_SIZE'])
        gv.extract.fillDisk             = SectID['FILL_DISK']

        # print ('..........................'); sys.exit()
        appo                            = SectID['Punteggi']
        gv.extract.punteggi             = [int(x.strip('\n').strip()) for x in appo.split(',') if x]



        appo = SectID['PERCENT']
        '''
            # dentro una LIST
        gv.extract.percent              = [x.strip('\n').strip() for x in appo.split(',') if x]
        '''
            # dentro un DICT
        gv.extract.percent = {}
        for item in appo.split(','):
            if item:
                key, val = item.split(':')
                gv.extract.percent[key.strip('\n')] = int(val)

        appo = SectID['MAX_AUTHORS_SONGS']
        gv.extract.maxSongPerAuthor = {}
        for item in appo.split(','):
            if item:
                key, val = item.split(':')
                gv.extract.maxSongPerAuthor[key.strip('\n')] = int(val)



        appo = SectID['Prefissi particolari']
        gv.extract.aliases = {}
        for item in appo.split(','):
            if item:
                key, val = item.split(':')
                gv.extract.aliases[key.strip('\n')] = val


        # gv.LN.dict.printDictionaryTree(gv, gv.extract, header="Section: [extract] [{0}]".format(calledBy(0), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2))

    except Exception as why:
        msg = "ERROR: {0} nel file.ini".format(str(why))
        gv.LN.sys.exit(gv, 1001, "ERROR: {0} nel file.ini".format(str(why)))


    return gv.extract


