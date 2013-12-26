#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys
import  textwrap
import optparse


def mainUsage(exit=True): # senza gv altrimenti non funziona usage per la --version
    LN = gv.LN

    print LN.cCYAN + textwrap.dedent("""\
          Usage: %s ACTION JBossInstanceNAME [-d|--debug] [-f|--file=deployFile]

        --------------- ACTION - You may indicate: ----------------
        -v --version -  Display version level
        -c --config  -  configuration file containing the flows to be executed
        -d --debug   -  start debug trace
        -a --action  -  STEP      to just display rSync command to be executed
                        DRY-RUN   run rSync command in DRY-RUN mode
                        GO        run rSync command

        Example: -c HomeBackup.cfg -s Portit_DiscoL -a step

         """ % (gv.scriptName) )


    if exit: sys.exit()




# ######################################################################################
# # ParseInput()
# ######################################################################################
def parseInput(gVars):
    global parser, gv
    gv = gVars
    usage = "\n\nUsage: %prog -C cfgFile -D Debug"

    parser = optparse.OptionParser(usage, version="ProjectName Version 0.01 - 2013-10-30") # --version
    cfgFile = None


    parser.add_option( "-a", "--action",
                       type="string",
                       dest="ACTION",
                       default='TEST',
                       help="You may indicate the ACTION with the -a option. Default is: [light]")



    group = optparse.OptionGroup(parser,
                        "\n --------------- Optional parameters----------------",
                        "Use these options to set debug or other values.")

    group.add_option( "-c", "--cfgFile",
                       type="string",
                       dest="CFGFILENAME",
                       default=cfgFile,
                       help="You may indicate a cfgFile with the -c option. Default is one of the following (in the order): [%s]" % (cfgFile))


    group.add_option( "-D", "--debug",
                       action="store_true",
                       dest="DEBUG",
                       default=False,
                       help="You may indicate a debug status with the -d option. Default is: [False]")

    parser.add_option_group(group)


    (options, args) = parser.parse_args()

    validActions =  ["GO", "TEST"]
    if options.ACTION:
        actionUPP = options.ACTION.upper()
        if not actionUPP in validActions:
            mainUsage()
    else:
        mainUsage()

    gv.args = options



