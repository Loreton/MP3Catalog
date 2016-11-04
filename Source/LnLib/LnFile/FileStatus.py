#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import pathlib
import datetime


# #########################################################################
# - dirList()
#   Return a list of file names found in directory 'dirName'
#       patternLIST: ["*.x", "*x*.y*", ...]
# #########################################################################
def _FileModificationTime(fileName):
    if os.path.isfile(fileName):
        try:
            p = pathlib.Path(fileName)
        except OSError:
            p = null
        last_modified_date = p.stat().st_mtime

    else:
        last_modified_date = 0

    # last_modified_date = p.stat().st_size

    # formato: 1474961500.0
    return last_modified_date

def FileModificationTime(fileName):
    try:
        mtime = os.path.getmtime(fileName)
    except OSError:
        mtime = 0

    last_modified_date = datetime.datetime.fromtimestamp(mtime)

    # formato: 2016-11-04 11:33:06
    return last_modified_date