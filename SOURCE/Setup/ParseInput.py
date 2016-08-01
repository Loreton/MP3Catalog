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
    global C
    C = gv.Ln.Colors()
    if not programVersion: programVersion = gv.Prj.Version


    positionalActionsDict  =  dict (
            # extract     = "filtra le canzoni e crea i file con le selezioni...",
            copySongs   = "le canzoni risultate 'validSongs' le copia sulla dir di destinazione"
        )



        # se non ci sono parametri... forziamo l'help
    if len(sys.argv) == 1: sys.argv.append('-h')
    mainArgs   = prepareArgParse(positionalActionsDict, programVersion)
    InputPARAM = commonParsing(mainArgs.action)


        # aggiungiamo manualmente valori alla struttura
    InputPARAM.action       = mainArgs.action

    if InputPARAM.defaultFlags:
        InputPARAM.Recomended = True
        InputPARAM.Loreto     = True
        InputPARAM.Buona      = True



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
        description=C.getYellow(description),
        usage='',                                               # non voglio lo usage
        epilog=C.getYellow(mainHelp),
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
        C.printYellow(".... Unrecognized action [{0}]. Valid actions are:".format(mainArgs.action), tab=8)
        for action in positionalActionsDict.keys():
            C.printYellow (action, tab=16)
        # print (C.RESET)
        exit(1)

    return mainArgs


###################################################
# - commonParsing
###################################################
def commonParsing(actionName, DESCR='CIAO DESCR'):
    usageMsg = "\n          {COLOR}   {ACTION} {COLRESET}[options]".format(COLOR=C.YEL, ACTION=actionName, COLRESET=C.RESET)
    myParser = argparse.ArgumentParser( description=actionName + ' Command',
                                        add_help=True, usage=usageMsg,
                                        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        # formatter_class=argparse.RawDescriptionHelpFormatter,
                                        )





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
        C.printCyan ('[{0}] - Command not yet implemented!'.format(actionName))
        sys.exit(1)


        # ------------------------------------------------
        # - skip first/action parameter
        # ------------------------------------------------
    args = myParser.parse_args(sys.argv[2:])

    return args



# ---------------------------
# - A C T I O N s
# ---------------------------
def COPYSONGS(myParser):
    if len(sys.argv[1:]) == 1: sys.argv.append('-h')
    _songDirs(myParser)
    _executeOptions(myParser)
    _copySongsOptions(myParser)
    _commonOptions(myParser)
    _debugOptions(myParser)
    # _testOptions(myParser)

# def EXTRACT(myParser):
#     _commonOptions(myParser)
#     _executeOptions(myParser)
#     _debugOptions(myParser)
    # pass




# ---------------------------
# - COPYSONGS
# ---------------------------
def _debugOptions(myParser):

    myParser.add_argument( "--check-source",
                            action="store_true",
                            dest="fCHECK_SOURCE",
                            default=False,
                            help=C.getYellow("""Verify that all the sources song are present.
    [DEFAULT: False]
    """))

    myParser.add_argument( "-D", "--debug",
                            required=False,
                            action="store_true",
                            dest="fDEBUG",
                            default=False,
                            help=C.getYellow("""enter in DEBUG mode.
    [DEFAULT: False]
    """))

        # log debug su console
    myParser.add_argument( "-dc", "--dconsole",
                            required=False,
                            action="store_true",
                            dest="LogCONSOLE",
                            default=False,
                            help=C.getYellow("""display log to console.
    [DEFAULT: False]
    """))
# ---------------------------
# - COPYSONGS
# ---------------------------
def _copySongsOptions(myParser):
    myParser.add_argument( "--max-output-bytes",
                            type=calculateBytes,
                            default='0',
                            required=False,
                            dest="maxBytes",
                            help=C.getYellow("""Numero massimo di bytes che deve avere l'output
    Es.: 10m | 10G | 10K | 2549878
    [DEFAULT: 0 (no limits)]
    """))
    #                         help=C.getYellow("""Numero massimo di bytes che deve avere l'output
    # [DEFAULT: 0 (no limits)]
    # """))

    myParser.add_argument( "--num-out-dirs",
                            type=int,
                            default=1,
                            required=False,
                            dest="numDirs",
                            help=C.getYellow("""Numero di directory da creare.
    Verranno create tante subDirs sotto la dest-dir con un size <= --max-output-bytes.
    [DEFAULT: 1]
    """))


# ---------------------------
# - EXECUTE
# ---------------------------
def _executeOptions(myParser):
    myParser.add_argument( "--go",
                            action="store_true",
                            dest="fEXECUTE",
                            default=False,
                            help=C.getYellow("""Execute commands.
    [DEFAULT: False, run in DRY-RUN mode]
    """))

# ---------------------------
# - Directrory
# ---------------------------
def _songDirs(myParser):
    mandatory = C.getYellowH('MANDATORY')
    myParser.add_argument( "-s", "--source-dir",
                            type=str,
                            required=True,
                            dest="sourceDIR",
                            metavar="directory sorgente",
                            help=mandatory + C.getYellow( """ - Nome della directory da cui prelevare le canzoni ...
    """))

    myParser.add_argument( "-d", "--dest-dir",
                            type=str,
                            required=True,
                            dest="destDIR",
                            metavar="directory di destinazione",
                            help=mandatory + C.getYellow(""" - Nome della directory dove copiare le canzoni selezionate ...
    """))

    myParser.add_argument( "-1", "--one-dir-x-author",
                            action="store_true",
                            required=False,
                            default=False,
                            dest="oneDirPerAuthor",
                            help=C.getYellow("""viene creata una directory per autore (quindi senza le dir di Album)
    [DEFAULT: False]
    """))





# ---------------------------
# - COMMON
# ---------------------------
def _commonOptions(myParser):

    myParser.add_argument( "-a",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="defaultFlags",
                            help=C.getYellow("""include i seguenti flags:
        --recomended    = True
        --loreto        = True
        --buona         = True
    [DEFAULT: False]
    """))

    myParser.add_argument( "--max-songs",
                            type=int,
                            default=0,
                            required=False,
                            dest="maxSongs",
                            help=C.getYellow("""Numero massimo di canzoni da processare... comodo per DEBUG
    [DEFAULT: 0 (all songs)]
    """))

    myParser.add_argument( "--no-analysed",
                            action="store_false",
                            default=True,
                            required=False,
                            dest="Analizzata",
                            help=C.getYellow("""Indica che le canzoni da filtrare NON abbiano il flag di analysed.
    [DEFAULT: True]
    """))

    myParser.add_argument( "--recomended",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="Recomended",
                            help=C.getYellow("""Indica che le canzoni da filtrare abbiano il flag di recomended.
    [DEFAULT: False]
    """))

    myParser.add_argument( "--loreto",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="Loreto",
                            help=C.getYellow("""Indica che le canzoni da filtrare abbiano il flag di loreto.
    [DEFAULT: False]
    """))

    myParser.add_argument( "--buona",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="Buona",
                            help=C.getYellow("""Indica che le canzoni da filtrare abbiano il flag di Buona.
    [DEFAULT: False]
    """))

    myParser.add_argument( "--vivace",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="Vivace",
                            help=C.getYellow("""Indica che le canzoni da filtrare abbiano il flag di vivace.
    [DEFAULT: False]
    """))

    myParser.add_argument( "--molto-vivace",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="MoltoViv",
                            help=C.getYellow("""Indica che le canzoni da filtrare abbiano il flag di molto-vivace.
    [DEFAULT: False]
    """))

    myParser.add_argument( "--car",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="Car",
                            help=C.getYellow("""Indica che le canzoni da filtrare abbiano il flag di car.
    [DEFAULT: False]
    """))

    myParser.add_argument( "--soft",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="Soft",
                            help=C.getYellow("""Indica che le canzoni da filtrare abbiano il flag di Soft.
    [DEFAULT: False]
    """))

    myParser.add_argument( "--camera",
                            action="store_true",
                            default=False,
                            required=False,
                            dest="Camera",
                            help=C.getYellow("""Indica che le canzoni da filtrare abbiano il flag di camera.
    [DEFAULT: False]
    """))







###############################################
# -
###############################################
def calculateBytes(value):
    # print (len(value), value)
    # if value == '0':
    #     value = '9'*24
    lastChar = value.strip().lower()[-1]
    if lastChar == 'm':
        bytes = int(value[:-1]) * 1000000
    elif lastChar == 'g':
        bytes = int(value[:-1]) * 1000000000
    elif lastChar == 'k':
        bytes = int(value[:-1]) * 1000
    else:
        bytes = int(value)

    print ('.............BYTES', bytes)
    return bytes
