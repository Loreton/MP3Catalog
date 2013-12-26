#!/ usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per la cercare di rendere leggibile un libro pdf
#           da cui è stato prelevato tutto il testo con copy/paste
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys

class myClass():
    def __dir__(self):  # forse non serve
        pass



################################################################################
# - M A I N
# - Prevede:
# -  1 - Impostazioni dei path per il corretto import dei moduli personali
# -  3 - Lettura del file di configurazione applicazione (per logFile)
# -  4 - Inizializzazione del logger
# -  2 - Controllo parametri di input per capire il file di config da utilizzare
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv, args):
    LN      = gv.LN
    Prj     = gv.Prj
    logger = LN.logger

    LN.dict.printDictionaryTree(gv, gv,  MaxDeepLevel=99, retCols='LTV', lTAB=' '*4, console=True)

