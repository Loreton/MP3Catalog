#!/opt/python3.4/bin/python3.4

import sys
import os
import shutil

        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
scriptDir             = os.path.dirname(os.path.abspath(sys.argv[0]))
scriptName, scriptExt = os.path.basename(os.path.abspath(sys.argv[0])).split('.')
prjDir                = scriptDir

prjDirs = [prjDir, prjDir+'/bin']


        # ------------------------------------------
        # - Preparazione directories per LnLib
        # ------------------------------------------
rootDir = os.path.dirname(prjDir)
LnPythonLibDir = os.path.join(rootDir, 'LnPythonLib')
LnPrjLibDir    = os.path.join(prjDir, 'SOURCE', 'LnLib')

print ('sourceLib:', LnPythonLibDir)
print ('destLib:  ',   LnPrjLibDir)


files = [
            '__init__.py',

            'System/__init__.py',
            'System/LnLogger.py',
            'System/LnColor.py',
            'System/Exit.py',
            'System/GetKeyboardInput.py',

            'LnDict/__init__.py',
            'LnDict/PrintDictionaryTree.py',

            'colorama/__init__.py',
            'colorama/ansi.py',
            'colorama/ansitowin32.py',
            'colorama/initialise.py',
            'colorama/win32.py',
            'colorama/winterm.py',
        ]


for fname in files:
    sourceFileName  = os.path.join(LnPythonLibDir,  fname)
    destFileName    = os.path.join(LnPrjLibDir,     fname)
    if not os.path.isfile(destFileName):
        print ('copying...{0:<60} --> {1}'.format( sourceFileName, destFileName))
        try:
            destdir = os.path.dirname(destFileName)
            if not os.path.exists(destdir): os.makedirs(destdir)
            shutil.copyfile(sourceFileName, destFileName)


        except (IOError, os.error) as why:
            msg = "Can't COPY [{0}] to [{1}]: {2}".format(sourceFileName, destFileName, str(why))
            print ()
            print (msg)
            print ()
