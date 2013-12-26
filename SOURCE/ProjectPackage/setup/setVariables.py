#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys, logging

class myClass():
    pass

def setVariables(gv):
    logger   = gv.LN.logger
    calledBy = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    # PRJStatus    = myClass()
    gv.PRJStatus = myClass()               # lo aggangiamo come sotto-insieme del gv

    PRJStatus = gv.PRJStatus               # lo aggangiamo come sotto-insieme del gv

    PRJStatus.DIR_NOT_FOUND       = 'DIR NOT FOUND'
    PRJStatus.DIR_ALREADY_EXISTS  = 'DIR ALREADY EXISTs'
    PRJStatus.CONFIG_NOT_FOUND    = 'CONFIG NOT FOUND'
    PRJStatus.CONFIG_FILE_ERROR   = 'CONFIGURATION File Error'
    PRJStatus.CONFIG_OK           = 'CONFIGURATION OK'
    PRJStatus.INSTALLED           = 'INSTALLED'
    PRJStatus.NO_AUTO_STOP        = 'NO AUTO-STOP'
    PRJStatus.NO_AUTO_START       = 'NO AUTO-START'
    PRJStatus.ALREADY_STOPPED     = 'ALREADY STOPPED'
    PRJStatus.ALREADY_RUNNING     = 'ALREADY RUNNING'
    PRJStatus.STOPPING            = 'STOPPING'
    PRJStatus.NOT_RUNNING         = 'NOT RUNNING'
    PRJStatus.RUNNING             = 'RUNNING'
    PRJStatus.UNSTABLE            = 'Unrecognized Status - UNSTABLE'
    PRJStatus.OK                  = 'OK'
    PRJStatus.NOT_OK              = 'NOT OK'
    PRJStatus.PROC_WAIT_TIMEOUT   = 'ERROR - Timeout occurs during Process WAITing'

    # gv.Vars                     = myClass()  # variabili globali

    logger.info('exiting - [called by:%s]' % (calledBy(1)))
