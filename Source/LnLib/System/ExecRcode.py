#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
#
#!/usr/bin/python -O
# -O Optimize e non scrive il __debug__
#
# ####################################################################################################################
import sys, subprocess

from ..LnCommon.LnLogger import SetLogger
# from ..LnCommon.LnColor  import LnColor
# from ..LnCommon.Exit     import Exit

##########################################################
# - timeout     solo dalla Versione 3.3
# - extraParam  conterrà magari parametri con blank in mezzo
##########################################################
def ExecRcode(command, timeout=5, EXECUTE=True, shell=False):
    logger = SetLogger(package=__name__)


    if isinstance(command, list):
        cmdLIST = command

    elif isinstance(command, str):
        cmdLIST = [x.strip() for x in command.split()]

    if shell:
        cmdLIST = ' '.join(cmdLIST)                      # Join command

    logger.debug('[dry-run: {DRYRUN}] - executing command "{0}"'.format(command, DRYRUN=not EXECUTE))

    if EXECUTE:
        logger.info(' EXEC:    {0}'.format(' '.join(cmdLIST)))
        try:
            rCode = subprocess.call( cmdLIST, shell=shell, timeout=timeout)  # ritorna <class 'bytes'>

                # output = output.decode('utf-8')                         # converti in STRing
        except subprocess.TimeoutExpired as why:
            msg = str(why)
            logger.error(msg)
            rCode = 9

    else:
        logger.info(' DRY-RUN: {0}'.format(command))
        rCode = 0

    if rCode:
        logger.error('rcode: {0}'.format(rCode))

    return rCode

    '''  ALTRO metodo
    with open(os.devnull, "wb") as limbo:
        outputult  = subprocess.Popen(cmdLIST, stdout=limbo, stderr=limbo).wait()

    '''
