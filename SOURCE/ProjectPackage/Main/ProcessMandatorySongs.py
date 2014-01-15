#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

# ############################################
# # Write MANDATORY Songs
# ############################################
def processMandatorySongs(gv, mandatorySongsLIST):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger

    print
    print
    print "%s # ############################################" % (' '*15)
    print "%s # # Write MANDATORY Songs" % (' '*15)
    print "%s # ############################################" % (' '*15)
    print

    bRecomended  =  gv.CONFIG.EXTRACT_SECTION['Recomended - Mandatory']
    if not bRecomended or gv.COPY.mandatorySONGS <= 0:
        return

    LOOP = True
    while LOOP:
        (returnedERROR, gv.COPY.mandatorySONGS_written, gv.COPY.mandatorySONGS_remaining) = Prj.mp3.processSongs(gv, mandatorySongsLIST)
        print '\n'*2
        logger.console(LN.cGREEN + "mandatory songs have been written.....:%5d" % (gv.COPY.mandatorySONGS_written))
        logger.console(LN.cGREEN + "mandatory songs remainings............:%5d" % (gv.COPY.mandatorySONGS_remaining))

        if returnedERROR != '':
            Prj.main.printStatus(gv)
            Prj.exit(gv, 9999, returnedERROR)

            # prepariamoci ad uscire
        gv.COPY.IGNORE_CRITERIA = False
        LOOP                    = False

        if gv.COPY.mandatorySONGS_remaining:
            Prj.main.printStatus(gv)
            logger.console(LN.cYELLOW + "Ci sono ancora canzoni Mandatory da scrivere.")
            choice = LN.sys.getKeyboardInput(gv, LN.cYELLOW + "      - Vuoi copiarle comunque ignorando i criteri richiesti?", validKeys=['yes', 'no'], exitKey='XQ', deepLevel=3, fDEBUG=False)
            if choice.upper() == 'YES':
                gv.COPY.IGNORE_CRITERIA = True
                LOOP                    = True



