#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import os
import argparse

LnColor = None
def SetGlobals(color):
    global LnColor
    LnColor = color

####################################
# - executeOptions
####################################
def ExecuteOptions(myParser):
    myParser.add_argument( "--go",
                            action="store_true",
                            dest="fEXECUTE",
                            default=False,
                            help=LnColor.getYellow("""Execute commands.
    [DEFAULT: False, run in DRY-RUN mode]
    """))



####################################
# - sqlite_importCSV
####################################
def ImportCSV(myParser):
    mandatory = ''
    myParser.add_argument( "-i", "--import-file",
                            type=_fileCheck,
                            required=False,
                            dest="csvInputFile",
                            metavar="CSV_input_filename",
                            default=None,
                            help=mandatory + LnColor.getYellow( """ - Nome del file CSV di cui fare l'import.
    DEFAULT: None
    """))


####################################
# - verifyWithSource()
####################################
def VerifyWithSource(myParser):
    mandatory = ''
    myParser.add_argument( "--verify-with-source",
                            required=False,
                            dest="verifyWithSource",
                            action="store_true",
                            default=False,
                            help=mandatory + LnColor.getYellow( """ - Confronta il DB con i file sorgenti per verificarne l'esistenza.
    DEFAULT: False
    """))

####################################
# - SourceDir()
####################################
def SourceDir(myParser):
    myParser.add_argument( "--source-dir",
                            type=str,
                            required=False,
                            default=None,
                            dest="MP3SourceDir",
                            # metavar="directory sorgente",
                            help=LnColor.getYellow( """ - Nome della directory da cui prelevare le canzoni ...
    [DEFAULT: {0}]
    """.format(None)))



####################################
# # _fileCheck()
####################################
def _fileCheck(fileName):
    if not os.path.isfile(fileName):
        print ()
        LnColor.printYellow ('  {FILE} is not a valid filename...'.format(FILE=fileName) + LnColor.RESET)
        print ()
        sys.exit(1)

    return fileName
