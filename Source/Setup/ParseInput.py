#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import os
import argparse
# mi serve per poi cercare i metodi dentro
this_mod = sys.modules[__name__]


#############################################################
# - parseInput()
#############################################################
def parseInput(gv, args, columnsName, programVersion=None):
    global C, songColumsName
    songColumsName = columnsName
    C = gv.Ln.Colors()
    if not programVersion: programVersion = gv.Prj.Version

    # songColumsName.SAMPLE = 'analizzata recomended loreto buona soft car vivace molto_vivace camera'

    positionalActionsDict  =  dict (
            # extract     = "filtra le canzoni e crea i file con le selezioni...",
            copySongs   = "copia le canzoni risultate dalla selezione nella directory di destinazione"
        )



        # se non ci sono parametri... forziamo l'help
    if len(sys.argv) == 1: sys.argv.append('-h')
    mainArgs   = prepareArgParse(positionalActionsDict, programVersion)
    InputPARAM = commonParsing(mainArgs.action)

    if InputPARAM.fTRACE: InputPARAM.fDEBUG = True

        # aggiungiamo manualmente valori alla struttura
    InputPARAM.action       = mainArgs.action

        # eliminiamo valori di include exclude non previsti
    print ()
    for item in reversed(InputPARAM.include):
        if item:
            if not item in songColumsName:
                C.printCyanH ('{0} - is not an INCLUDE valid argument'.format(item), tab=4)
                sys.exit()
        else:
            InputPARAM.include.remove(item)

    for item in reversed(InputPARAM.exclude):
        if item:
            if not item in songColumsName:
                C.printCyanH ('{0} - is not an EXCUDE valid argument'.format(item), tab=4)
                sys.exit()
        else:
            InputPARAM.exclude.remove(item)
    print ()





        # -----------------------------------------------------
        # - convert  InputPARAM (argparse.Namespace) in dict
        # -----------------------------------------------------
    myDict = {}
    for key, val in vars(InputPARAM).items():
        myDict[key] = val

            # -----------------------------------------
            # - Controlli
            # -----------------------------------------
    if InputPARAM.fDEBUG:
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        dictID = vars(InputPARAM)
        for key, val in sorted(dictID.items()):
                C.printCyan('{0:<20} : {1}'.format(key, val), tab = 8)

        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()


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

    mainArgs = myParser.parse_args(sys.argv[1:2])


    if not (mainArgs.action in positionalActionsDict.keys()):
        myParser.print_help()
        C.printYellow(".... Unrecognized action [{0}]. Valid actions are:".format(mainArgs.action), tab=8)
        for action in positionalActionsDict.keys():
            C.printYellow (action, tab=16)
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
    # _commonMultipleOptions(myParser)
    # _testOptions(myParser)

# def EXTRACT(myParser):
#     _commonOptions(myParser)
#     _executeOptions(myParser)
#     _debugOptions(myParser)
    # pass




# ---------------------------
# - _debugOptions
# ---------------------------
def _debugOptions(myParser):

    myParser.add_argument( "--check-source",
                            action="store_true",
                            dest="fCHECK_SOURCE",
                            default=False,
                            help=C.getYellow("""Verify that all the sources song are present.
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


    # --------------------------------------------------
    # - gruppi mutuamente esclusivi
    # --------------------------------------------------
    debugGroup = myParser.add_mutually_exclusive_group(required=False)  # True indica obbligatorietà di uno del gruppo

    debugGroup.add_argument( "-D", "--debug",
                            required=False,
                            action="store_true",
                            dest="fDEBUG",
                            default=False,
                            help=C.getYellow("""enter in DEBUG mode.
    [DEFAULT: False]
    """))

    debugGroup.add_argument( "-T", "--trace",
                            required=False,
                            action="store_true",
                            dest="fTRACE",
                            default=False,
                            help=C.getYellow("""enter in TRACE mode.
    [DEFAULT: False]
    """))

# ---------------------------
# - _copySongsOptions
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
# - _executeOptions
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
# - _songDirs
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
# - _commonOptions
# ---------------------------
def _commonOptions(myParser):
    # split della lista in gruppi da x elementi
    nElem = 5
    opts = ''
    composite_list = [songColumsName[x:x+nElem] for x in range(0, len(songColumsName),nElem)]
    for item in composite_list:
        opts += C.getYellowH(' '.join(item) + '\n        ')
    myParser.add_argument( "--include",
                            default=['analizzata'],
                            required=False,
                            # dest="multipleFlags",  # se omesso viene preso il nome lungo del parametro.
                            nargs='*',
                            help=C.getYellow("""inserire uno o piu argomenti della lista:

        {0}

        gli elementi vanno in AND. Ttutti i flag devono essere presenti per accettare la canzone.
    [DEFAULT: analizzata]
    """.format(opts)))

    myParser.add_argument( "--exclude",
                            default=[''],
                            required=False,
                            # dest="multipleFlags",  # se omesso viene preso il nome lungo del parametro.
                            nargs='*',
                            help=C.getYellow("""inserire uno o piu argomenti della lista:

        {0}

        gli elementi vanno in OR. Basta che uno sia presente che la canzone viene scartata
    [DEFAULT: '']
    """.format(opts)))


    myParser.add_argument( "--max-songs",
                            type=int,
                            default=0,
                            required=False,
                            dest="maxSongs",
                            help=C.getYellow("""Numero massimo di canzoni da processare... comodo per DEBUG
    [DEFAULT: 0 (all songs)]
    """))


###############################################
# - calculateBytes
###############################################
def calculateBytes(value):
    lastChar = value.strip().lower()[-1]

    if lastChar == 'm':
        bytes = int(value[:-1]) * 1000000
    elif lastChar == 'g':
        bytes = int(value[:-1]) * 1000000000
    elif lastChar == 'k':
        bytes = int(value[:-1]) * 1000
    else:
        bytes = int(value)

    return bytes
