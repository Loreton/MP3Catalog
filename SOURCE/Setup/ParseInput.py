#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys; sys.dont_write_bytecode = True
import os
import argparse
# mi serve per poi cercare i metodi dentro
this_mod = sys.modules[__name__]

#############################################################
# - parseInput()
#############################################################
def parseInput(gv, args, programVersion=None):
    global TAByel, TABerr, TABcyan, cYEL, cCYAN, cRESET
    if not programVersion: programVersion = gv.Prj.Version

    # global gv;  gv = GlobalVars
    TAByel      = gv.Ln.cYELLOW + ' '*8
    TABerr      = gv.Ln.cERROR + ' '*8
    TABcyan     = gv.Ln.cCYAN + ' '*8
    cYEL        = gv.Ln.cYELLOW
    cCYAN       = gv.Ln.cCYAN
    cRESET      = gv.Ln.cRESET

    positionalActionsDict  =  dict (
            filter      = "filtra le canzoni e crea i file con le selezioni...",
            extract     = "le canzoni risultate 'extracted' le copia sulla dir di destinazione"
        )



        # se non ci sono parametri... forziamo l'help
    if len(sys.argv) == 1: sys.argv.append('-h')
    mainArgs   = prepareArgParse(positionalActionsDict, programVersion)
    InputPARAM = commonParsing(mainArgs.action)

        # aggiungiamo manualmente valori alla struttura
    InputPARAM.action       = mainArgs.action



            # -----------------------------------------
            # - Controlli
            # -----------------------------------------
    if InputPARAM.fDEBUG:
        print ('\n', InputPARAM, '\n')
        dictID = vars(InputPARAM)
        print()
        print('     ---- {0} - INPUT Parameters ---'.format(InputPARAM.action))
        print()
        for key, val in dictID.items():
                print('         {0:<20} : {1}'.format(key, val))
        print()
        print('     ---- {0} - INPUT Parameters ---'.format(InputPARAM.action))
        print()
        # sys.exit()



        # -----------------------------------------------------
        # - convert  InputPARAM (argparse.Namespace) in dict
        # -----------------------------------------------------
    myDict = {}
    for key, val in vars(InputPARAM).items():
        myDict[key] = val

    return myDict



#############################################################
# - prepareArgParse()
#############################################################
def prepareArgParse(positionalActionsDict, programVersion):
    mainHelp    = "default help"
    description = "MP3Catalog"

    # print (len(positionalActionsDict))
    # print (positionalActionsDict.keys())

    # if len(positionalActionsDict) > 0:
    totalCMDLIST = '\n'
    for key, val in sorted(positionalActionsDict.items()):
        totalCMDLIST += '          * {0:<12} : {1}\n'.format(key, val)
    totalCMDLIST += '\n '

    mainHelp="""
        Immettere uno dei seguenti comandi/action:
        (con il parametro -h se si desidera lo specifico help)
                {CMDLIST}\n""".format(CMDLIST=totalCMDLIST)

    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description=cYEL+description+cRESET,
        usage='',                                               # non voglio lo usage
        epilog=cYEL+mainHelp+cRESET,
        conflict_handler='resolve',
    )


    myParser.add_argument('--version',
                            action='version',
                            version='%(prog)s {VER}'.format(VER=programVersion))

    myParser.add_argument('action', help='Command/Action to run')

    # print ('11111', sys.argv[1:2])
    mainArgs = myParser.parse_args(sys.argv[1:2])
    # print ('22222', mainArgs.action)

        # - Positional Parameter ....
    # if len(positionalActionsDict):

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail

    if not (mainArgs.action in positionalActionsDict.keys()):
        myParser.print_help()
        print ("""{COLOR}.... Unrecognized action [{PARAM}]. Valid actions are:""".format(COLOR=TAByel,PARAM=mainArgs.action))
        for action in positionalActionsDict.keys():
            print ('        ', TABcyan+action)
        print (cRESET)
        exit(1)

    return mainArgs


###################################################
# - commonParsing
###################################################
def commonParsing(actionName, DESCR='CIAO DESCR'):
    usageMsg = "\n          {COLOR}   {ACTION} {COLRESET}[options]".format(COLOR=cYEL, ACTION=actionName, COLRESET=cRESET)
    myParser = argparse.ArgumentParser( description=actionName + ' Command',
                                        add_help=True, usage=usageMsg,
                                        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        # formatter_class=argparse.RawDescriptionHelpFormatter,
                                        )



    _commonOptions(myParser)

    # --------------------------------------------------
    # - forzare l'help solo se sappiamo che il comando
    # - richiede ulteriori parametri altrimenti
    # - il programma non va avanti.
    # --------------------------------------------------
    # if len(sys.argv[2:]) == 0: sys.argv.append('-h')



        # use dispatch pattern to invoke method with same name
        # ritorna un nameSpace
    if hasattr(this_mod, actionName.upper()):
        getattr(this_mod, actionName.upper())(myParser)
    else:
        print (TABcyan+ '[{0}] - Command not yet implemented!'.format(actionName))
        sys.exit(1)


        # ------------------------------------------------
        # - skip first/action parameter
        # ------------------------------------------------
    args = myParser.parse_args(sys.argv[2:])

    return args



# ---------------------------
# - A C T I O N s
# ---------------------------
def EXTRACT(myParser):
    if len(sys.argv[1:]) == 1: sys.argv.append('-h')
    _songDirs(myParser)
    _executeOptions(myParser)
    # _ddnsOptions(myParser)

def FILTER(myParser):
    _executeOptions(myParser)
    # pass





# ---------------------------
# - EXECUTE
# ---------------------------
def _executeOptions(myParser):
    myParser.add_argument( "-go", "--go",
                            action="store_true",
                            dest="fEXECUTE",
                            default=False,
                            help=cYEL+"""Execute commands.
    [DEFAULT: False, run in DRY-RUN mode]
    """+cRESET)

# ---------------------------
# - DDNS
# ---------------------------
def _songDirs(myParser):
    myParser.add_argument( "-s", "--source-dir",
                            type=str,
                            required=True,
                            dest="sourceDIR",
                            help=cYEL+"""Nome della directory da cui prelevare le canzoni ...
    """+cRESET)

    myParser.add_argument( "-d", "--dest-dir",
                            type=str,
                            required=True,
                            dest="destDIR",
                            help=cYEL+"""Nome della directory dove copiare le canzoni selezionate ...
    """+cRESET)

    myParser.add_argument( "-1", "--one-dir-x-author",
                            action="store_true",
                            required=False,
                            default=False,
                            dest="oneDirPerAuthor",
                            help=cYEL+"""viene creata una directory per autore (quindi senza le dir di Album)
    [DEFAULT: False]
    """+cRESET)





# ---------------------------
# - COMMON
# ---------------------------
def _commonOptions(myParser):
    myParser.add_argument( "-D", "--debug",
                            required=False,
                            action="store_true",
                            dest="fDEBUG",
                            default=False,
                            help=cYEL+"""enter in DEBUG mode.
    [DEFAULT: False]
    """+cRESET)

        # log debug su console
    myParser.add_argument( "-dc", "--dconsole",
                            required=False,
                            action="store_true",
                            dest="LogCONSOLE",
                            default=False,
                            help=cYEL+"""display log to console.
    [DEFAULT: False]
    """+cRESET)


