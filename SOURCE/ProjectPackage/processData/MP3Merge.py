#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# =======================================================================
# Mp3Merge()
# =======================================================================
def Mp3Merge(gv):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

    cfg = gv.CONFIG

        # -------------------------------------------------
        # - input output files
        # -------------------------------------------------
    cfg.DIRS_TO_SCAN        = cfg.MERGE_SECTION.get('dir to scan', '')



        # ------------------------------------------------------------------------
        # - Se le dir non sono passate come parametro cerchiamole nel file.ini
        # ------------------------------------------------------------------------
    if cfg.DIRS_TO_SCAN == '':
        for keyName, dirName in cfg.MERGE_SECTION.items():
            if keyName.startswith('dirToAdd.'):
                cfg.DIRS_TO_SCAN = "%s;%s" % (cfg.DIRS_TO_SCAN, dirName)

    if cfg.DIRS_TO_SCAN == '' or cfg.EXCEL_INPUT_FILE == '':
        usage("..... inpDir and inpFile are mandatory parameters")


        # --------------------------------------------------------------------
        # - Leggiamo il file Excel di Input (se richiesto) e creimao il DB
        # - Altrimenti lo creiamo nuovo
        # --------------------------------------------------------------------
    MP3Dict = ReadExcelCatalog()


    # MP3Dict.printDictionary()

        # --------------------------------------------------------------------
        # - Ora facciamo lo scanning delle dirs e le aggiungiamo al DB
        # --------------------------------------------------------------------
    for dirName in cfg.DIRS_TO_SCAN:
        dirName = dirName.strip()
        MyLogger.info("scanning folder: [%s]" % (dirName))
        MP3Dict = insertDirectory(dirName, MP3Dict, fDEBUG=True)

        # --------------------------------------------------------------------
        # - Se il file.out non è richiesto allora facciamo il display a video
        # - Altrimenti creiamo un nuovo foglio Excel
        # --------------------------------------------------------------------
    if cfg.EXCEL_OUTPUT_FILE == '':
        (nLevels, Mp3List) = MP3Dict.dictionaryToList( MaxDeepLevel=99, OutList='Normal', fPRINT=True)
        for linea in Mp3List:
            MyLogger.info(linea)
    else:
        WriteCatalogToExcel(cfg.EXCEL_OUTPUT_FILE, MP3Dict)
        MyLogger.info("\n\nfile [%s] has been created\n\n" % (cfg.EXCEL_OUTPUT_FILE))


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
