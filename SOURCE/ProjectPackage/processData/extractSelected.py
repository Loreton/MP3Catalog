#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# =======================================================================
# sample()
# =======================================================================
def sample():
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

# =======================================================================================
# - Estrae tutte le canzoni che hanno una 'x' nei campi richiesti
# - Tutti queste canzoni verranno salvate in un file excel di output (if != None)
# - Se retType == LIST allora verrà ritornala una lista invece del DICT
# =======================================================================================
def extractSelected(dict, Punteggi=[], attribToExtract=[], attribToAvoid=[]):

    outDict = LnDict.SafeDict(name =' outDict ')
    # songAttrName = globalARGs[NOME_CALONNE_ATTRIBUTI]

    MyLogger.info("                     %s" % (Punteggi) )

    MyLogger.info("\n")
    # PunteggiLista = range(min(Punteggi), max(Punteggi)+1)

    for typeName in dict.keys():
        authorDict = dict.get(typeName)
        for authorName in authorDict.keys():
            albumDict = authorDict.get(authorName)
            for albumName in albumDict.keys():
                songDict = albumDict.get(albumName)

                for songName, val in songDict.items():
                    valore = val[attribPUNTEGGIO]
                    # if valore in Punteggi:
                    if valore >= min(Punteggi) and valore <= max(Punteggi):
                        currAlbumPtr = outDict.getSectionPointer(typeName+';'+authorName+';'+albumName, fldSep=';', create=True)
                        currAlbumPtr[songName] = val

    return outDict


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
