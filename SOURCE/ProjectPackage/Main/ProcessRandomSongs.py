#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################



# ############################################
# # Write RANDOM Songs
# ############################################
def processRandomSongs(gv, randomSongsLIST):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger

    print
    print
    print "%s # ############################################" % (' '*15)
    print "%s # # Write RANDOM Songs" % (' '*15)
    print "%s # ############################################" % (' '*15)
    print



    if gv.COPY.randomSONGS <= 0:
        logger.console(LN.cRED + "Non ci sono canzoni risultanti dalla selezione richiesta.")
        return

    LOOP = True
    while LOOP:
        (returnedERROR, gv.COPY.randomSONGS_written, gv.COPY.randomSONGS_remaining) = Prj.mp3.processSongs(gv, randomSongsLIST)
        print '\n'*2
        logger.console(LN.cGREEN + "Mandatory songs have been written..: %5d"   % (gv.COPY.randomSONGS_written))
        logger.console(LN.cGREEN + "Random    songs remaining..........: %5d"   % (gv.COPY.randomSONGS_remaining))

        if returnedERROR != '':
            Prj.main.printStatus(gv)
            Prj.exit(gv, 9999, returnedERROR)


            # prepariamoci ad uscire
        gv.COPY.IGNORE_CRITERIA = False
        LOOP                    = False

        if gv.COPY.randomSONGS_remaining:
            Prj.main.printStatus(gv)
            logger.console(LN.cYELLOW + "Ci sono ancora canzoni valide da copiare.")
            choice = LN.sys.getKeyboardInput(gv, LN.cYELLOW + "      - Vuoi copiarle comunque ignorando i criteri richiesti?", validKeys=['yes', 'no'], exitKey='XQ', deepLevel=3, fDEBUG=False)
            if choice.upper() == 'YES':
                gv.COPY.IGNORE_CRITERIA = True
                LOOP                    = True


