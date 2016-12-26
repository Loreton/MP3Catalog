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
def ParseInput(gVars, args, programVersion=None):
    global C,  gv
    gv = gVars

    C = gv.Ln.LnColor()
    if not programVersion: programVersion = 'unknown'

     # definizioni per mantenere insalterato l'ordine
    positionalActionsDict  =  {
        'edit': {
            'conf'    : "edit configuration file"
            },
        'excel': {
            'export'    : "esporta il file excel, definito nel file di conf,  in formato CSV"
            },
        'sqlite': {
            'export'    : "export in base alla stringa passata oppure inserita nel file di conigurazione, in formato CSV",
            'fullexport': "export dell'intera tabella, in formato CSV",
            'backup'    : "export dell'intera tabella, in formato CSV e backap del .db e.csv",
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
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        dictID = vars(InputPARAM)
        for key, val in sorted(dictID.items()):
            TYPE = '(' + str(type(val)).split("'")[1] + ')'
            C.printCyan('{0:<20} : {1:<6} - {2}'.format(key, TYPE, val), tab = 8)


        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
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
        description=C.getYellow(description),
        usage='',                                          # non voglio lo usage
        epilog=C.getYellow(mainHelp),
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
    myParser.add_argument('mainCommand',
                metavar=C.getCyanH('primaryCommand & secondaryCommand') + C.getYellow(mainHelp),
                type=str,
                nargs=2,
                help='comando e sottocomando come elencato di seguito.'
                # help='comando e sottocomando come elencato di seguito.' + C.getYellow(mainHelp)
                )

        # ----------------------------------------------------------
        # - lanciamo il parse dei parametri subito dopo quelli posizionali
        # ----------------------------------------------------------
    posizARGS = 2
    mainArgs = myParser.parse_args(sys.argv[1:posizARGS+1])
    primaryCommand   = mainArgs.mainCommand[0]
    secondaryCommand = mainArgs.mainCommand[1]
    # print (type(mainArgs.mainCommand), mainArgs.mainCommand)

        # print dell'HELP per il primaryCommand errato
    if not (primaryCommand in positionalActionsDict.keys()):
        myParser.print_help()
        C.printYellow(".... Unrecognized command [{0}]. Valid values are:".format(primaryCommand), tab=8)
        for positionalParm in positionalActionsDict.keys():
            C.printYellow (positionalParm, tab=16)
        exit(1)

        # print dell'HELP in base al primaryComand passato
    ptr = positionalActionsDict[primaryCommand]
    if not secondaryCommand in ptr.keys():
        print()
        C.printCyan(".... Unrecognized subcommand [{0}]. Valid values for [{1}] command are:".format(secondaryCommand, primaryCommand), tab=8)
        for key, val in ptr.items():
            C.printCyanH ('{0:<20}    : {1}'.format(key, val), tab=16)
        exit(1)

    # print (subCommand)

    return mainArgs


###################################################
# - commonParsing
###################################################
def commonParsing(positionalParm, DESCR='CIAO DESCR'):
    mainCommand, secondaryCommand = positionalParm
    usageMsg = "\n          {COLOR}   {ACTION} {COLRESET}[options]".format(COLOR=C.YEL, ACTION=mainCommand, COLRESET=C.RESET)
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
        getattr(this_mod, mainCommand.upper())(myParser, secondaryCommand)
    else:
        C.printCyan ('[{0}] - Command not yet implemented!'.format(mainCommand))
        sys.exit(1)


        # ------------------------------------------------
        # - skip first/action parameter
        # ------------------------------------------------
    args = myParser.parse_args(sys.argv[len(positionalParm)+1:])
    # print (args.compareWithSource)

    return args







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
                            help=C.getYellow("""attivazione del logger.
    [DEFAULT: False]
    """))

        # log debug su console
    logGroup.add_argument( "--log-console",
                            required=False,
                            dest="LogCONSOLE",
                            action="store_true",
                            # choices=['info', 'debug'],
                            default=False,
                            help=C.getYellow("""attivazione log sulla console.
    """))

        # log debug su specifica funzione
    myParser.add_argument( "--log-function",
                            required=False,
                            dest="LogMODULE",
                            default=False,
                            help=C.getYellow("""attivazione log sul una singola funcName o stringa di essa.
    Possono essere anche porzioni di funcName separate da ',' Es: pippo,uto,ciao
    """))


    myParser.add_argument( "-D", "--debug",
                            required=False,
                            action="store_true",
                            dest="fDEBUG",
                            default=False,
                            help=C.getYellow("""enter in DEBUG mode..
    [DEFAULT: None]
    """))

    myParser.add_argument( "--elapsed",
                            required=False,
                            action="store_true",
                            dest="fELAPSED",
                            default=False,
                            help=C.getYellow("""display del tempo necessario al processo..
    [DEFAULT: False]
    """))






# ---------------------------
# - A C T I O N s
# ---------------------------
def EDIT(myParser, action):
    _debugOptions(myParser)

    if action == 'conf':
        command = [
                    gv.ini.MAIN.editor,
                    gv.Prj.iniFileName
                    ]
        rCode = gv.Ln.ExecRcode(command, timeout=5, EXECUTE=True, shell=False)
        C.printCyan('configuration file can be edited [RCODE: {}]'.format(rCode), tab=4)
        sys.exit()

    else:
        C.printCyan('Action [{0}] non prevista per il comando di edit...'.format(action), tab=4)

    myParser.print_help()

# ---------------------------
# - A C T I O N s
# ---------------------------
def EXCEL(myParser, action):
    if len(sys.argv[2:]) == 1: sys.argv.append('-h')
    from . import ParseInput_Excel as excel

    excel.SetGlobals(C)

    if action == 'export':
        excel.ExportToCSV(myParser)

    _debugOptions(myParser)

# ---------------------------
# - A C T I O N s
# ---------------------------
def SQLITE(myParser, action):
    from . import ParseInput_SQLite as sqlite

    sqlite.SetGlobals(C)

    if action == 'import':
        if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        sqlite.ImportCSV(myParser, required=True)

    elif action == 'export':
        # if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        sqlite.ExportCSV(myParser, required=False)
        sqlite.ExportQuery(myParser, required=False)

    elif action == 'fullexport':
        pass
        # if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        # sqlite.ExportCSV(myParser, required=False)

    elif action == 'backup':
        pass
        # if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        # sqlite.ExportCSV(myParser, required=False)

    elif action == 'merge':
        if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        sqlite.SourceDir(myParser, required=True)

    elif action == 'copySongs':
        if len(sys.argv[2:]) == 1: sys.argv.append('-h')
        sqlite.SourceDir(myParser, required=True)
        sqlite.DestDir(myParser, required=True)
        sqlite.ExecuteOptions(myParser, required=False)

    elif action == 'edit':
        pass

    else:
        print('''
            Action: {0} per sqlite non prevista.
            valori previsti sono:
            '''.format(action)
            )
        sys.exit()

    _debugOptions(myParser)



