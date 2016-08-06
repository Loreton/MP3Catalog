#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# Version 0.01 08/04/2010:  Starting
# ####################################################################################################################
import os, sys


# ###########################################################################
# * Gestione input da Keyboard.
# * 29-08-2010 - Rimosso LnSys dalla chiamata alla LnSys.exit()
# * 12-02-2012 - Cambiato keys in keyLIST
# * 12-03-2013 - Cambiato keyLIST in validKeys
# * 01-01-2014 - modificato il validKeysLIST.
# ###########################################################################
def getKeyboardInput(gv, msg, validKeys='ENTER', exitKey='X', deepLevel=1, keySep="|", fDEBUG=False):
    logger = gv.Ln.setLogger(package=__name__)


    exitKeyUPP = exitKey.upper()

    if keySep in validKeys:
        validKeyLIST = validKeys.split(keySep)
    else:
        validKeyLIST = validKeys

    if keySep in exitKeyUPP:
        exitKeyLIST = exitKeyUPP.split(keySep)
    else:
        exitKeyLIST = exitKeyUPP

    print()
    if " Temporanea" in msg: fDEBUG=True
    if fDEBUG:
        print("exitKeyLIST....:", exitKeyLIST)
        print("validKeyLIST...:", validKeyLIST)
        caller = "%s" % (calledBy(deepLevel))
        msg = "<{CALLER}> - [{MSG} - ({VALKEY})] ({EXITKEY} to exit) ==> ".format(CALLER=caller, MSG=msg, VALKEY=validKeys, EXITKEY=exitKey)
    else:
        msg = "%s [%s] - (%s to exit) ==> " % (msg, validKeys, exitKey)

    try:
        while True:
            choice      = input(msg).strip()
            choiceUPP   = choice.upper()
            if fDEBUG: print("choice: [%s]" % (choice))

            if choice == '':
                if "ENTER" in validKeys:
                    return ''
                else:
                    print('\n... please enter something\n')

            elif choiceUPP in exitKeyLIST:
                gv.Ln.exit(gv, 9998, "Exiting on user request new.", printStack=True)

            elif choice in validKeyLIST:
                break

            else:
                print('\n... try again\n')

    except Exception as why:
        gv.Ln.exit(gv, 8, "Error running program [{ME}]\n\n ....{WHY}\n".format(ME=sys.argv[0], WHY=why) )


    return choice


