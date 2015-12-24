#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope: Lettura di un file nel formato INI
#        Ricerca all'interno la sezione [UseridSection] che contiene userID e Password.
#        Se la password non è presente oppure è in chiaro la cripta e riscrive il file.
# ######################################################################################

import configparser
import logging

fullPackageName = __name__.split('.')
baseLoggerName  = ('.'.join(fullPackageName[-2:]))

# ######################################################
# # https://docs.python.org/3/library/configparser.html
def checkUserID(gv, iniFileName):
# ######################################################
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = logging.getLogger(baseLoggerName)
    calledBy    = gv.LN.sys.calledBy
    Crypt       = gv.LN.crypt.XorCryptString
    deCrypt     = gv.LN.crypt.XorDeCryptString

    logger.debug('entered - [called by:{0}]'.format(calledBy(1)))

        # Lettura del file
    configID = gv.LN.file.readIniFile(iniFileName, gVars=gv)
    gv.LN.dict.printDictionaryTree(gv, configID, header="Main variables [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, listInLine=2, console=False, exit=False)

    gv.JBossMon.UserID    = None
    gv.JBossMon.Password  = None

    UseridSection = 'USER_ID'
    encPrefix = ':dedocnE-NL:'[::-1]   # Reverse pe mascherarlo
    if configID.has_section(UseridSection):
        uSection = configID[UseridSection]
        userID    = uSection.get('userid', None)
        password  = uSection.get('password', '')
        encPassw = None

        logger.info('UserID: %s' % (userID))

        if userID:
            REWRITE_FILE = False
            if password.startswith(encPrefix):             # è già codificata
                encPassw = password[len(encPrefix):]

            elif password == '':             # vuoto
                clearPassword = input('Please enter a password for userid [%s]: ' % (userID) )
                encPassw = Crypt(clearPassword, userID)
                REWRITE_FILE = True

            else:                               # c'è un valore ma non cripted
                clearPassword = password
                encPassw = Crypt(clearPassword, userID)
                REWRITE_FILE = True

            if REWRITE_FILE:
                uSection['password'] = encPrefix + encPassw
                logger.info('Userid: %s:  - Crypted Password: [%s]' % (userID, encPassw))
                logger.info('rewriting file: %s' % (iniFileName))
                gv.LN.file.writeIniFile(gv, configID, iniFileName)

            gv.JBossMon.UserID    = userID
            gv.JBossMon.Password  = encPassw



    else:
        logger.warning('No section [%s] found on file: %s' % (UseridSection, iniFileName))

    logger.debug('exiting - [called by:{0}]'.format(calledBy(1)))

    return configID


