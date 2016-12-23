#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import time



def CreateBackupFile(fileName):
    mtime = 0
    if os.path.isfile(fileName):
        mtime = os.path.getmtime(fileName)
        # print (mtime)
    else:
        return

    Tuple = time.gmtime(mtime)
    # print (Tuple)
    outputFormat="%Y%m%d_%H%M%S"
    lastModifiedTime =  time.strftime(outputFormat, Tuple)

    fname, ext  = os.path.splitext(fileName)
    newFileName = fname + '_' + lastModifiedTime + ext
    os.rename(fileName, newFileName)