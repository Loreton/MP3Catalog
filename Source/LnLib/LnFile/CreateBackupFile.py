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

    basedir     = os.path.basedir(fileName)
    fname, ext  = os.path.splitext(fileName)

    # newFileName = fname + '_' + lastModifiedTime + ext
    newFileName = '{FNAME}_{DATE}.{EXT}'.format(FNAME=fname, DATE=lastModifiedTime, EXT=ext)
    zipFName    = '{FNAME}_{DATE}.zip'.format(FNAME=fname,   DATE=lastModifiedTime)

    os.rename(fileName, newFileName)
    LnZip(zipFName, newFileName)



# https://pymotw.com/2/zipfile/
# https://docs.python.org/3.4/library/zipfile.html
import zipfile
def CreateZipBackupFile(archiveName, basedir, fileList=[]):

    savedDir = os.getcwd()
    os.chdir(basedir)
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    modes = { zipfile.ZIP_DEFLATED: 'deflated',
              zipfile.ZIP_STORED:   'stored',
              }

    print ('creating archive', archiveName)
    myzip = zipfile.ZipFile(archiveName, mode='w', compression=compression)
    try:
        for filename in fileList:
            print ('adding {0} with compression mode: {1}'.format(filename, modes[compression]))
            myzip.write(os.path.relpath(filename), compress_type=compression)
    finally:
        print ('closing')
        myzip.close()
        os.chdir(savedDir)

    print()
    xx = myzip.infolist()
    for item in xx:
        print ('filename        ', item.filename)
        print ('date_time       ', item.date_time)
        # print ('compress_type   ', item.compress_type)
        print ('file_size       ', item.file_size)
        print ('compress_size   ', item.compress_size)
        print ()

    print ()
    # xx = myzip.namelist()
    # for item in xx:
    #     print ('filename        ', item)
