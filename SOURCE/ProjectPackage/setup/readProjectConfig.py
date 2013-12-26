#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os

class myClass():    pass

# #######################################################################
# # Lettura del file di configurazione
# #######################################################################
def readProjectConfig(gv, cfgFileName=None, sectionName=None, flowID=None):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))


        # ---------------------------------------------------------------------
        # - Leggiamo le variabili lette dalla Sezione MAIN
        # ---------------------------------------------------------------------

    if cfgFileName:
        # ----------------------------------------------------------------------
        # - Lettura del file di configurazione
        # - Leggiamo anche i valori considerati Mandatory
        # ----------------------------------------------------------------------
        (cfgMODULE, cfgDICT, cfgPATH, cfgFULLPATH) =  LN.dict.loadDictFile(gv, cfgFileName, moduleName=None, fDEBUG=False)
        if not hasattr(cfgMODULE, "Main"):
            Prj.exit(gv, 97, "Main{} section NOT present in %s file" % (cfgFileName) )

        gv.CONFIG.CONFIG_FILE_ID = cfgMODULE    # SAVE module pointer

            # --------------------------------------------------------
            # - Pointers delle sezioni di interesse
            # --------------------------------------------------------
        MainID = cfgMODULE.Main


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
