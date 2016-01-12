#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys; sys.dont_write_bytecode = True

    # gv.LN.dict.printDictionaryTree(gv, percentList, header="percentList [{0}]".format(calledBy(0)), console=True, fEXIT=True, retCols='TV', lTAB=' '*4, listInLine=2)

######################################
# - normalize():
# percdm = dm([('Natale', 0), ('Bambini', 0), ('Italiani', 71), ('Stranieri', 20), ('Themes', 0), ('Classica', 0), ('Popolari', 5), ('Country', 10), ('Chitarra', 5)])
# perced = ed([('Natale', 0), ('Bambini', 0), ('Italiani', 71), ('Stranieri', 20), ('Themes', 0), ('Classica', 0), ('Popolari', 5), ('Country', 10), ('Chitarra', 5)])
# ###############################################################

def PercentNormalization(gv, percentList):
    logger   = gv.LN.setLogger(gv, __name__, LnConsole=True)
    calledBy = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))

    logger.info("{0} - {1}".format(type(percentList), percentList))

        # convertiamo la list in DICT
    # percentDict = gv.LN.listToDotMap(gv, percentList, fieldsInRow=2)
    # percentDict = gv.LN.listToEDict(gv, percentList, fieldsInRow=2)
    # percentDict = gv.LN.LnDotMap(percentList)

    percentDict = gv.LN.LnEasyDict(percentList)

    print (percentDict.Italiani)
    print (percentDict['Italiani'])
    print (percentDict)

    for key  in percentDict.keys():
        print (key)
        # totPercent += int(val)


    totPercent = 0
    logger.info("totPercent {0}".format(totPercent))

    '''



    if totPercent != 100:
        print ()
        print ("Totale percentuali [{0}]".format(totPercent))
        print ("Verra' fatta la normalizzazione a 100")
        print ()


    newTotal = 0
    for key, reqPercent in percentList.percent.items():
            #  Allineamento a 100 delle percentuali   [ x : 70 = 100 : TotalPercent ]
        calcPercent = (reqPercent * 100.0)/totPercent
        calcPercentFloat = '{0:.2F}'.format( calcPercent)
        newTotal += float(calcPercent)


            #  calcolo del size corrispondente alla percentuale [ x : MAX_OUT_DIR_SIZE = perc : 100 ]
            # L'entry della LIST cambia: KEY = %req, %calcolata, %maxBytes, copiedBytes, %reale
        maxBytes = int((calcPercent * percentList.maxOutDirSize) / 100)
        percentList.percent[key.strip('\n')] = [reqPercent, calcPercentFloat, maxBytes, 0, 0]

            # Creazione di entrate/enum che verranno utilizzate dal programma per conoscere i vari field
        percentList.FIELD_PERCENT_REQ_PERC           = 0
        percentList.FIELD_PERCENT_CALC_PERC          = 1
        percentList.FIELD_PERCENT_MAXBYTES           = 2
        percentList.FIELD_PERCENT_COPIEDBYTES        = 3
        percentList.FIELD_PERCENT_REAL_PERC          = 4


    '''
