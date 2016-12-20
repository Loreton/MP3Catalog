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
# - sqlite_importCSV
####################################
def ExportToCSV(myParser):
    mandatory = 'MANDATORY'
    # myParser.add_argument( "-if", "--input-excel-file",
    #                         type=_fileCheck,
    #                         required=True,
    #                         dest="excelFile",
    #                         metavar="EXCEL-input-filename",
    #                         default=None,
    #                         help=mandatory + LnColor.getYellow( """ - Nome del file Excel di cui fare l'export.
    # DEFAULT: None
    # """))
    myParser.add_argument( "-f", "--input-file",
                            type=str,
                            required=True,
                            dest="excelFile",
                            metavar="Excel filename",
                            default=None,
                            help=mandatory + LnColor.getYellow( """ - Nome del file Excel di cui fare l'export.
    Il file di output avrà lo stesso fullPath ma con estenzione .csv
    DEFAULT: None
    """))
