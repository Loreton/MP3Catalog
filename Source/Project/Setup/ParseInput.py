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
def parseInput(gVars, args, columnsName, programVersion=None):
    global LnColor, songColumsName, gv
    gv = gVars
    songColumsName = columnsName
    LnColor = gv.Ln.LnColor()
    if not programVersion: programVersion = 'unknown'

    positionalActionsDict  =  dict (
            # extract     = "filtra le canzoni e crea i file con le selezioni...",
            copySongs   = "copia le canzoni risultate dalla selezione nella directory di destinazione",
            ExcelExport = "esporta il file excel, definito nel file di conf,  in formato CSV",
            merge       = "legge la directory ed inserisce/modifica le canzoni esistenti"
        )



        # se non ci sono parametri... forziamo l'help
    if len(sys.argv) == 1: sys.argv.append('-h')
    mainArgs   = prepareArgParse(positionalActionsDict, programVersion)
    InputPARAM = commonParsing(mainArgs.songAction)

    if InputPARAM.LogMODULE:
        InputPARAM.LogACTIVE = True

    if InputPARAM.LogCONSOLE:
        InputPARAM.LogACTIVE = True

        # aggiungiamo manualmente valori alla struttura
    InputPARAM.songAction       = mainArgs.songAction

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
        LnColor.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        dictID = vars(InputPARAM)
        for key, val in sorted(dictID.items()):
            TYPE = '(' + str(type(val)).split("'")[1] + ')'
            LnColor.printCyan('{0:<20} : {1:<6} - {2}'.format(key, TYPE, val), tab = 8)


        LnColor.printYellow('.'*10 + __name__ + '.'*10, tab=4)
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
        Immettere uno dei seguenti valori/comandi/action:
        (con il parametro -h se si desidera lo specifico help)
                {CMDLIST}\n""".format(CMDLIST=totalCMDLIST)

    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description=LnColor.getYellow(description),
        usage='',                                               # non voglio lo usage
        epilog=LnColor.getYellow(mainHelp),
        conflict_handler='resolve',
    )


    myParser.add_argument('--version',
                            action='version',
                            version='{PROG} Version: {VER}'.format(PROG='JBossCMK', VER=programVersion))
                            # version='%(prog)s {VER}'.format(VER=programVersion))



    myParser.add_argument('songAction', help='JBoss Version directory')



    mainArgs = myParser.parse_args(sys.argv[1:2])

    if not (mainArgs.songAction in positionalActionsDict.keys()):
        myParser.print_help()
        LnColor.printYellow(".... Unrecognized value [{0}]. Valid values are:".format(mainArgs.songAction), tab=8)
        for positionalParm in positionalActionsDict.keys():
            LnColor.printYellow (positionalParm, tab=16)
        exit(1)

    return mainArgs


###################################################
# - commonParsing
###################################################
def commonParsing(positionalParm, DESCR='CIAO DESCR'):
    usageMsg = "\n          {COLOR}   {ACTION} {COLRESET}[options]".format(COLOR=LnColor.YEL, ACTION=positionalParm, COLRESET=LnColor.RESET)
    myParser = argparse.ArgumentParser( description=positionalParm + ' Command',
                                        add_help=True, usage=usageMsg,
                                        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        # formatter_class=argparse.RawDescriptionHelpFormatter,
                                        )



        # use dispatch pattern to invoke method with same name
        # ritorna un nameSpace
    if hasattr(this_mod, positionalParm.upper()):
        getattr(this_mod, positionalParm.upper())(myParser)
    else:
        LnColor.printCyan ('[{0}] - Command not yet implemented!'.format(positionalParm))
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
    '''
        se aspetta  parametri obbligatori...
        ... if len(sys.argv[1:]) == 1: sys.argv.append('-h')
    '''
    _executeOptions(myParser)
    _debugOptions(myParser)
    _commonOptions(myParser)
    _copySongsOptions(myParser)
    _songDirs(myParser)
    _excelExport(myParser)

# ---------------------------
# - A C T I O N s
# ---------------------------
def EXCELEXPORT(myParser):
    '''
        se aspetta  parametri obbligatori...
        ... if len(sys.argv[1:]) == 1: sys.argv.append('-h')
    '''
    _excelExport(myParser)
    _debugOptions(myParser)


# ---------------------------
# - A C T I O N s
# ---------------------------
def MERGE(myParser):
    '''
        se aspetta  parametri obbligatori...
        ... if len(sys.argv[1:]) == 1: sys.argv.append('-h')
    '''
    _songDirs(myParser)
    _debugOptions(myParser)





# ---------------------------
# - _debugOptions
# ---------------------------
def _debugOptions(myParser):

    logGroup = myParser.add_mutually_exclusive_group(required=False)  # True indica obbligatorietà di uno del gruppo
    logGroup.add_argument( "--log",
                            required=False,
                            action="store_true",
                            dest="LogACTIVE",
                            default=False,
                            help=LnColor.getYellow("""attivazione del logger.
    [DEFAULT: False]
    """))

        # log debug su console
    logGroup.add_argument( "--log-console",
                            required=False,
                            dest="LogCONSOLE",
                            action="store_true",
                            # choices=['info', 'debug'],
                            default=False,
                            help=LnColor.getYellow("""attivazione log sulla console.
    """))

        # log debug su specifica funzione
    myParser.add_argument( "--log-function",
                            required=False,
                            dest="LogMODULE",
                            default=False,
                            help=LnColor.getYellow("""attivazione log sul una singola funcName o stringa di essa.
    Possono essere anche porzioni di funcName separate da ',' Es: pippo,uto,ciao
    """))



    myParser.add_argument( "-D", "--debug",
                            required=False,
                            action="store_true",
                            dest="fDEBUG",
                            default=False,
                            help=LnColor.getYellow("""enter in DEBUG mode..
    [DEFAULT: None]
    """))

    myParser.add_argument( "--elapsed",
                            required=False,
                            action="store_true",
                            dest="fELAPSED",
                            default=False,
                            help=LnColor.getYellow("""display del tempo necessario al processo..
    [DEFAULT: False]
    """))


    myParser.add_argument( "--check-source",
                            action="store_true",
                            dest="fCHECK_SOURCE",
                            default=False,
                            help=LnColor.getYellow("""Verify that all the sources song are present.
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
                            help=LnColor.getYellow("""Numero massimo di bytes che deve avere l'output
    Es.: 10m | 10G | 10K | 2549878
    [DEFAULT: 0 (no limits)]
    """))


    myParser.add_argument( "--num-out-dirs",
                            type=int,
                            default=1,
                            required=False,
                            dest="numDirs",
                            help=LnColor.getYellow("""Numero di directory da creare.
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
                            help=LnColor.getYellow("""Execute commands.
    [DEFAULT: False, run in DRY-RUN mode]
    """))

# ---------------------------
# - _songDirs
# ---------------------------
def _songDirs(myParser):
    mandatory = LnColor.getYellowH('MANDATORY')
    mandatory = ''
    myParser.add_argument( "-s", "--source-dir",
                            type=str,
                            required=False,
                            default=gv.ini.MAIN.sourceDIR,
                            dest="sourceDIR",
                            metavar="directory sorgente",
                            help=mandatory + LnColor.getYellow( """ - Nome della directory da cui prelevare le canzoni ...
    [DEFAULT: {0}]
    """.format(gv.ini.MAIN.sourceDIR)))

    myParser.add_argument( "-d", "--dest-dir",
                            type=str,
                            required=False,
                            default=gv.ini.MAIN.destDIR,
                            dest="destDIR",
                            metavar="directory di destinazione",
                            help=mandatory + LnColor.getYellow(""" - Nome della directory dove copiare le canzoni selezionate ...
    [DEFAULT: {0}]
    """.format(gv.ini.MAIN.destDIR)))



# ---------------------------
# - _excelExport
# ---------------------------
def _excelExport(myParser):
    mandatory = ''
    # mandatory = LnColor.getYellowH('MANDATORY')

    myParser.add_argument( "-f", "--input-file",
                            type=str,
                            required=False,
                            dest="excelFile",
                            metavar="Excel filename",
                            default=None,
                            help=mandatory + LnColor.getYellow( """ - Nome del file Excel di cui fare l'export.
    Il file di output avrà lo stesso fullPath ma con estenzione .csv
    DEFAULT: come definito nel file config.ini [EXCEL]-->EXCEL_File
    """))




# ---------------------------
# - _commonOptions
# ---------------------------
def _commonOptions(myParser):
    # split della lista in gruppi da x elementi
    nElem = 5
    opts = ''
    # - per ragioni di display delle colonne,
    # - creiamo una lista di liste dove ognuna è una riga
    composite_list = [songColumsName[x:x+nElem] for x in range(0, len(songColumsName),nElem)]
    for item in composite_list:
        opts += LnColor.getYellowH(','.join(item) + ',\n        ')

    defaultInclude = ['Analizzata']
    defaultInclude = [x.strip() for x in gv.ini.MAIN.include.split(',')]
    myParser.add_argument( "--include",
                            type=checkInclude,

                            # dest="multipleFlags",  # se omesso viene preso il nome lungo del parametro.

                            # ------------------------------------------------------------
                            # - il parametro choice mi visualizza le possibili scelte
                            # - ma visto che sono troppe le visualizzo nella
                            # - variabile opts ed elimino il parametro.
                            # - Il controllo lo faccio io manualmente con il type=.
                            # ------------------------------------------------------------
                            # choices=songColumsName,

                            default=defaultInclude,
                            required=False,

                            nargs='*',
                            help=LnColor.getYellow("""inserire uno o piu argomenti della lista:

        {OPT}

        gli elementi vanno in AND. Ttutti i flag devono essere presenti per accettare la canzone.
    [DEFAULT: {DEFAULT}]

    La sintassi dell'include:
        --include Loreto Lenta   --> CORRETTA
        --include=Loreto,Lenta   --> ERRATA
    """.format(DEFAULT=defaultInclude, OPT=opts)))




    defaultExclude = ['Undefined' ,'Avoidit','Confusionaria']
    defaultExclude = [x.strip() for x in gv.ini.MAIN.exclude.split(',')]
    myParser.add_argument( "--exclude",
                            type=checkExclude,
                            # ------------------------------------------------------------
                            # - il parametro choice mi visualizza le possibili scelte
                            # - ma visto che sono troppe le visualizzo nella
                            # - variabile opts ed elimino il parametro.
                            # - Il controllo lo faccio io manualmente con il type=.
                            # ------------------------------------------------------------
                            # choices=songColumsName,

                            # dest="multipleFlags",  # se omesso viene preso il nome lungo del parametro.
                            default=defaultExclude,
                            required=False,
                            nargs='+',
                            help=LnColor.getYellow("""inserire uno o piu argomenti della lista:

        {OPT}

        gli elementi vanno in OR. Basta che uno sia presente che la canzone viene scartata
    [DEFAULT: {DEFAULT}]

    La sintassi dell'exclude:
        --exclude Loreto Lenta   --> CORRETTA
        --exclude=Loreto,Lenta   --> ERRATA

    """.format(DEFAULT=defaultExclude, OPT=opts)))


    myParser.add_argument( "--max-songs",
                            type=int,
                            default=0,
                            required=False,
                            dest="maxSongs",
                            help=LnColor.getYellow("""Numero massimo di canzoni da processare... comodo per DEBUG
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

###############################################
# - checkInclude
###############################################
def checkInclude(value):
    if not value in songColumsName:
        LnColor.printRedH ('{0} - is not an INCLUDE valid argument'.format(value), tab=4)
        sys.exit()

    return value

###############################################
# - checkExclude
###############################################
def checkExclude(value):
    if not value in songColumsName:
        LnColor.printCyanH ('{0} - is not an EXCLUDE valid argument'.format(value), tab=4)
        sys.exit()

    return value
