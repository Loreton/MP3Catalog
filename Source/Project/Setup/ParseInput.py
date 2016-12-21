#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import os
import argparse
import collections
# mi serve per poi cercare i metodi dentro
this_mod = sys.modules[__name__]


#############################################################
# - parseInput()
#############################################################
def ParseInput(gVars, args, columnsName, programVersion=None):
    global LnColor, songColumsName, gv
    gv = gVars
    songColumsName = columnsName
    LnColor = gv.Ln.LnColor()
    if not programVersion: programVersion = 'unknown'

     # definizioni per mantenere insalterato l'ordine
    positionalActionsDict  =  {
        'excel': {
            'export'    : "esporta il file excel, definito nel file di conf,  in formato CSV"
            },
        'sqlite': {
            'export'    : "esporta il DB, in formato CSV",
            'import'    : "import del file csv passato come parametro",
            'merge'     : "legge la directory ed inserisce/modifica le canzoni esistenti",
            'copySongs' : "copia le canzoni risultate dalla selezione nella directory di destinazione",
            }
    }



        # se non ci sono parametri... forziamo l'help
    if len(sys.argv) == 1: sys.argv.append('-h')

    mainArgs   = prepareArgParse(positionalActionsDict, programVersion)
    InputPARAM = commonParsing(mainArgs.mainCommand)

    InputPARAM.mainCommand    = mainArgs.mainCommand
    InputPARAM.actionCommand = '.'.join(mainArgs.mainCommand)

    if InputPARAM.LogMODULE:
        InputPARAM.LogACTIVE = True

    if InputPARAM.LogCONSOLE:
        InputPARAM.LogACTIVE = True

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

    totalCMDLIST = []
    for key, val in positionalActionsDict.items():
        totalCMDLIST.append('\n')
        totalCMDLIST.append('      * {0}'.format(key))
        if isinstance(val, dict):
            for key1, val1 in val.items():
                totalCMDLIST.append('          {0:<30} : {1}'.format(key1, val1))
    cmdLIST = '\n'.join(totalCMDLIST)

    mainHelp="""
        Immettere uno dei seguenti valori/comandi/action:
        (con il parametro -h se si desidera lo specifico help)
                {CMDLIST}\n""".format(CMDLIST=cmdLIST)

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


        # -------------------------------------------------------
        # - con nargs viene tornata una lista con nArgs
        # - deve prendere il comando primario e poi il sottocomando
        # -------------------------------------------------------
    # -- mantenimao separati
    # myParser.add_argument('mainCommand',   metavar='mainCommand',   type=str, nargs=1)
    # myParser.add_argument('actionCommand', metavar='actionCommand', type=str, nargs=1)

    # .... oppure uniti.
    # myParser.add_argument('mainCommand',   metavar='mainCommand',   type=checkMainCommand, nargs=1)
    myParser.add_argument('mainCommand', metavar='mainCommand', type=str, nargs=2)

        # ----------------------------------------------------------
        # - lanciamo il parse dei parametri subito dopo quelli posizionali
        # ----------------------------------------------------------
    posizARGS = 2
    mainArgs = myParser.parse_args(sys.argv[1:posizARGS+1])
    mainCommand  = mainArgs.mainCommand[0]
    songsCommand = mainArgs.mainCommand[1]
    # print (type(mainArgs.mainCommand), mainArgs.mainCommand)

    # checkMainCommand(myParser, mainArgs.mainCommand[0], positionalActionsDict)
    # checkActionCommand(myParser, mainArgs.mainCommand[0], positionalActionsDict)

    if not (mainCommand in positionalActionsDict.keys()):
        myParser.print_help()
        LnColor.printYellow(".... Unrecognized value [{0}]. Valid values are:".format(mainCommand), tab=8)
        for positionalParm in positionalActionsDict.keys():
            LnColor.printYellow (positionalParm, tab=16)
        exit(1)

    return mainArgs


###################################################
# - commonParsing
###################################################
def commonParsing(positionalParm, DESCR='CIAO DESCR'):
    mainCommand, songsCommand = positionalParm
    usageMsg = "\n          {COLOR}   {ACTION} {COLRESET}[options]".format(COLOR=LnColor.YEL, ACTION=mainCommand, COLRESET=LnColor.RESET)
    myParser = argparse.ArgumentParser( description='{0} Command'.format(mainCommand),
                                        add_help=True, usage=usageMsg,
                                        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        # formatter_class=argparse.RawDescriptionHelpFormatter,
                                        )



        # use dispatch pattern to invoke method with same name
        # ritorna un nameSpace
    funcToCall = '_'.join(positionalParm)  # non so se conviene
    if hasattr(this_mod,  mainCommand.upper()):
        getattr(this_mod, mainCommand.upper())(myParser, songsCommand)
    else:
        LnColor.printCyan ('[{0}] - Command not yet implemented!'.format(mainCommand))
        sys.exit(1)


        # ------------------------------------------------
        # - skip first/action parameter
        # ------------------------------------------------
    args = myParser.parse_args(sys.argv[len(positionalParm)+1:])
    # print (args.compareWithSource)

    return args




# ---------------------------
# - A C T I O N s
# ---------------------------
def EXCEL(myParser, action):
    if len(sys.argv[2:]) == 1: sys.argv.append('-h')
    from . import ParseInput_Excel as excel

    excel.SetGlobals(LnColor)

    if action == 'export':
        excel.ExportToCSV(myParser)

    _debugOptions(myParser)

# ---------------------------
# - A C T I O N s
# ---------------------------
def SQLITE(myParser, action):
    from . import ParseInput_SQLite as sqlite

    sqlite.SetGlobals(LnColor)

    if action == 'import':
        if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        sqlite.ImportCSV(myParser)

    elif action == 'export':
        if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        sqlite.ExportCSV(myParser)

    elif action == 'merge':
        if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        sqlite.SourceDir(myParser)

    else:
        print('''
            Action: {0} per sqlite non prevista.
            valori previsti sono:
            '''.format(action)
            )
        sys.exit()

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



