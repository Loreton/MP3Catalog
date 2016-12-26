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
def ExecuteOptions(myParser, required=False):
    mandatory = LnColor.getYellowH('MANDATORY') if required else 'OPTIONAL'
    myParser.add_argument( "--go",
                            action="store_true",
                            dest="fEXECUTE",
                            default=False,
                            help=mandatory + LnColor.getYellow("""Execute commands.
    [DEFAULT: False, run in DRY-RUN mode]
    """))



####################################
# - sqlite_importCSV
####################################
def ImportCSV(myParser, required=False):
    mandatory = LnColor.getYellowH('MANDATORY') if required else 'OPTIONAL'
    myParser.add_argument( "-f", "--import-file",
                            type=_fileCheck,
                            required=required,
                            dest="csvInputFile",
                            metavar="CSV-input-filename",
                            default=None,
                            help=mandatory + LnColor.getYellow( """ - Nome del file CSV di cui fare l'import.
    DEFAULT: None
    """))




####################################
# - sqlite_importCSV
####################################
def ExportCSV(myParser, required=False):
    mandatory = LnColor.getYellowH('MANDATORY') if required else 'OPTIONAL'
    myParser.add_argument( "-of", "--output-file",
                            type=_outFileCheck,
                            required=required,
                            dest="csvOutputFile",
                            metavar="CSV-output-filename",
                            default=None,
                            help=mandatory + LnColor.getYellow( """ - Nome del file CSV su cui fare l'export.
    DEFAULT: {0}
    """.format(LnColor.getCyan(None))))


####################################
# - sqlite_importCSV
####################################
def ExportQuery(myParser, required=False):
    mandatory = LnColor.getYellowH('MANDATORY') if required else 'OPTIONAL'
    defaultSTR=['SELECT', '*', 'FROM', 'LoretoMP3', ';']
    sampleSTR='select * from "LoretoMP3" where AuthorName is "John Denver" AND AlbumName is "Greatest Hits"'
    myParser.add_argument( "-e", "--export-string",
                            type=str,
                            required=required,
                            dest="exportQuery",
                            metavar="export query string",
                            default=defaultSTR,
                            nargs='+',
                            help=mandatory + LnColor.getYellow( """ - Stringa di query da usare per l'export.
    DEFAULT: {0}
    Esempio: {1}
    """.format(LnColor.getCyan("'" + ' '.join(defaultSTR) + "'"), LnColor.getCyan("'" + sampleSTR + "'"))))




####################################
# - SourceDir()
####################################
def SourceDir(myParser, required=False):
    mandatory = LnColor.getYellowH('MANDATORY') if required else 'OPTIONAL'
    myParser.add_argument( "-s", "--source-dir",
                            type=_dirCheck,
                            required=required,
                            default=None,
                            dest="MP3SourceDir",
                            metavar="MP3SourceDir",
                            help=mandatory + LnColor.getYellow( """ - Nome della directory da cui prelevare le canzoni ...
    [DEFAULT: {0}]
    """.format(LnColor.getCyan(None))))



####################################
# - SourceDir()
####################################
def DestDir(myParser, required=False):
    mandatory = LnColor.getYellowH('MANDATORY') if required else 'OPTIONAL'
    myParser.add_argument( "-d", "--dest-dir",
                            type=_dirCheck,
                            required=required,
                            default=None,
                            dest="MP3DestDir",
                            metavar="MP3DestDir",
                            help=mandatory + LnColor.getYellow( """ - Nome della directory di destinazione ...
    [DEFAULT: {0}]
    """.format(None)))



####################################
# - CopySongs()
####################################
def CopySongs(myParser, required=False):
    mandatory = LnColor.getYellowH('MANDATORY')
    myParser.add_argument( "-s", "--source-dir",
                            type=_dirCheck,
                            required=required,
                            default=None,
                            dest="MP3SourceDir",
                            metavar="MP3SourceDir",
                            help=mandatory + LnColor.getYellow( """ - Nome della directory da cui prelevare le canzoni ...
    [DEFAULT: {0}]
    """.format(None)))
















####################################
# # _fileCheck()
####################################
def _fileCheck(fileName):
    if not os.path.isfile(fileName):
        print ()
        LnColor.printYellow ('  {FILE} is not a valid directory...'.format(FILE=fileName) + LnColor.RESET)
        print ()
        sys.exit(1)

    return fileName



####################################
# # _fileCheck()
####################################
def _outFileCheck(fileName):
    dirName = os.path.dirname(fileName)
    if not os.path.isdir(dirName):
        print ()
        LnColor.printYellow ('  {DIR} is not a valid directory...'.format(DIR=dirName) + LnColor.RESET)
        print ()
        sys.exit(1)

    return fileName

####################################
# # _fileCheck()
####################################
def _dirCheck(dirName):
    if not os.path.isdir(dirName):
        print ()
        LnColor.printYellow ('  {DIR} is not a valid directory...'.format(DIR=dirName) + LnColor.RESET)
        print ()
        sys.exit(1)

    return dirName
