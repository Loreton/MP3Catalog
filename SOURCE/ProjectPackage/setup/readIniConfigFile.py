#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per la gestione start/stop di un'istanza di JBoss EAP 6.x
#                                               by Loreto Notarantonio 2013, February
# Comando per eseguire uno script all'interno di uno ZIP file:
#        SET PYTHONPATH=JBossStart_LNf.zip python -m JBossStart [parameters]
#     oppure creare un file che si chiama __main__.py e lanciare il comando:
#        python JBossStart_LNf.zip [parameters]
# ######################################################################################

import os, sys
import platform
OpSys        = platform.system()


# NON HO ancora il LOG ATTIVO

class myClass():
    pass



# ##########################################################
# # readIniFile
# # return:
# #     log.xx tutti i valori relativi al file di LOG
# #     pkg.xx il path del package LN_Package
# ##########################################################
def readIniConfigFile(gv, iniFileName):
    Prj         = gv.Prj
    LN          = gv.LN
    # logger      = gv.LN.logger          #  Ancora non lo abbiamo
    calledBy    = gv.LN.sys.calledBy

    import getpass, ConfigParser

    OpSys   = platform.system()
    tempDir = os.getenv('TEMP', 'c:\\temp') if OpSys == 'Windows' else os.getenv('tmp', '/tmp')

        # con l'utente come suffix per evitare eventuali conflitti
    outFname    = os.path.join(tempDir, 'LnTemp_%s.ini' % (getpass.getuser()))


        # -----------------------------------------
        # - copiamo file.ini to temp.ini
        # - facendo lo strip delle righe
        # - per evitare che il parser dia errore
        # -----------------------------------------
    finp = open(iniFileName,"r")
    fout = open(outFname, "wb")
    for line in finp:
        line = line.strip()
        fout.write(line + '\n')

    finp.close()
    fout.close()

    config = ConfigParser.ConfigParser()
    config.read(outFname)


    # Otteniamo il nome del file di Log e relativi livelli di debug
    log  = myClass()
    iniMAIN = myClass()

    try:
        # iniMAIN.JBossURLs   = config.get('MAIN', 'JBossURLs').split(',')

        log.logDir          = config.get('LOG', 'logDir')

        log.fileName        = config.get('LOG', 'logFileName')
        log.levelFile       = config.get('LOG', 'LogLEVEL_file')
        log.levelConsole    = config.get('LOG', 'LogLEVEL_console')
        log.loggerID        = config.get('LOG', 'loggerID')
        log.maxBytes        = config.getint('LOG', 'maxBytes')
        log.nFiles          = config.getint('LOG', 'nFiles')

        savedPath = os.getcwd()
        os.chdir(log.logDir)
        os.chdir(savedPath)

    except (ConfigParser.Error), why:
        Prj.exit(gv, 1, "ERROR reading %s file - %s" % (iniFileName, str(why) ) )

    except (StandardError, IOError), why:
        Prj.exit(gv, 2, str(why))

        # Creazione nome del log file con l'utente come suffix per evitare conflitti
    (fname, fext) = os.path.splitext(log.fileName)
    log.fileName  = "%s_%s%s" % (fname, getpass.getuser(), fext)

    gv.INI_LOG  = log
    gv.INI_MAIN = iniMAIN

    return log, config

