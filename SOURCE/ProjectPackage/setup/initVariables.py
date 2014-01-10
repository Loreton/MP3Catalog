#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys, logging

class myClass():    pass



def initVariables(gv):
    # logger   = gv.LN.logger
    # calledBy = gv.LN.sys.calledBy
    # logger.debug('entered - [called by:%s]' % (calledBy(1)))

    gv.STATUS                       = myClass()               # lo aggangiamo come sotto-insieme del gv
    gv.STATUS.DIR_NOT_FOUND         = 'DIR NOT FOUND'
    gv.STATUS.DIR_ALREADY_EXISTS    = 'DIR ALREADY EXISTs'
    gv.STATUS.CONFIG_NOT_FOUND      = 'CONFIG NOT FOUND'
    gv.STATUS.CONFIG_FILE_ERROR     = 'CONFIGURATION File Error'
    gv.STATUS.CONFIG_OK             = 'CONFIGURATION OK'
    gv.STATUS.OK                    = 'OK'
    gv.STATUS.NOT_OK                = 'NOT OK'
    gv.STATUS.PROC_WAIT_TIMEOUT     = 'ERROR - Timeout occurs during Process WAITing'


    gv.RCODE                        = myClass()               # lo aggangiamo come sotto-insieme del gv
    gv.RCODE.shortStatus            = ""
    gv.RCODE.errMsg                 = ""
    gv.RCODE.statusMsg              = ""


    gv.INP_PARAM                    = myClass()                     # Dati passati come parametri
    gv.INP_PARAM.fDEBUG             = False
    gv.INP_PARAM.action             = "TEST"                        # TEST - GO - DRY-RUN
    gv.INP_PARAM.actionUPP          = gv.INP_PARAM.action.upper()
    gv.INP_PARAM.mainCfgFile        = None


    gv.INI                          = myClass()                     # Dati relativi alla configurazione del file.ini


    gv.LOG                          = myClass()
    gv.LOG.logDir          = None
    gv.LOG.fileName        = None
    gv.LOG.levelFile       = None
    gv.LOG.levelConsole    = None
    gv.LOG.loggerID        = None
    gv.LOG.nFiles          = 0
    gv.LOG.maxBytes        = 0
    gv.LOG.logger          = None



    # Specific Project Variables
    gv.CONFIG                       = myClass()                     # Dati relativi alla configurazione del file project.cfg

    gv.EXCEL                        = myClass()                     # Dati relativi alla configurazione del file project.cfg
    gv.EXCEL.ROWS                   = []                            # Righe del foglio Excel

    gv.MP3                          = myClass()                     # Base per il Catalogo
    gv.MP3.Dict                     = {}                          # Catalogo delle canzoni
    gv.MP3.randomSONGS              = []                               # Catalogo delle canzoni estratte
    gv.MP3.mandatorySONGS           = []                               # Catalogo delle canzoni estratte di tipo Recomended/Mandatory

    gv.MP3.TYPE                     = myClass()
    gv.MP3.TYPE.BYTES               = {}                            # bytes copiati per tipologia di canzoni (ITALIANI, STRANIERI, ...)



    # logger.debug('exiting - [called by:%s]' % (calledBy(1)))

