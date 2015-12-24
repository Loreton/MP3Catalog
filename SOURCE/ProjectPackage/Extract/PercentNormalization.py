#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys; sys.dont_write_bytecode = True

# ###############################################################
# - calcola():
# ###############################################################
def PercentNormalization(gv, extractINI):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy

    logger.info('entered - [called by:{0}]'.format(calledBy(1)))

    totPercent = 0
    for key, val in extractINI.percent.items():
        totPercent += int(val)

    if totPercent != 100:
        print ()
        print ("Totale percentuali [{0}]".format(totPercent))
        print ("Verra' fatta la normalizzazione a 100")
        print ()


    newTotal = 0
    for key, reqPercent in extractINI.percent.items():
            #  Allineamento a 100 delle percentuali   [ x : 70 = 100 : TotalPercent ]
        calcPercent = (reqPercent * 100.0)/totPercent
        calcPercentFloat = '{0:.2F}'.format( calcPercent)
        newTotal += float(calcPercent)


            #  calcolo del size corrispondente alla percentuale [ x : MAX_OUT_DIR_SIZE = perc : 100 ]
            # L'entry della LIST cambia: KEY = %req, %calcolata, %maxBytes, copiedBytes, %reale
        maxBytes = int((calcPercent * extractINI.maxOutDirSize) / 100)
        extractINI.percent[key.strip('\n')] = [reqPercent, calcPercentFloat, maxBytes, 0, 0]

            # Creazione di entrate/enum che verranno utilizzate dal programma per conoscere i vari field
        extractINI.FIELD_PERCENT_REQ_PERC           = 0
        extractINI.FIELD_PERCENT_CALC_PERC          = 1
        extractINI.FIELD_PERCENT_MAXBYTES           = 2
        extractINI.FIELD_PERCENT_COPIEDBYTES        = 3
        extractINI.FIELD_PERCENT_REAL_PERC          = 4


    # gv.LN.dict.printDictionaryTree(gv, extractINI, header="Section: [extract] [{0}]".format(calledBy(0), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2))
