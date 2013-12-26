#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys, imp
import pprint


# #############################################################################
# # setBaseEnv()
# # Impostazione delle PATHs
# # La scriptDir consideriamo la curren a meno che non finisce con /bin.
# # In tal caso saliamo di una subDir.
# #############################################################################
def setBaseEnv():
    (scriptDir, FileName)   = os.path.split(os.path.abspath(sys.argv[0]))
    (Fname, Fext)           = os.path.splitext(FileName)
    drive                  = scriptDir[:2]
    MainProgramName         = Fname

    if scriptDir.endswith(os.sep + 'bin'): scriptDir = scriptDir[:-4]
    if scriptDir.endswith(os.sep + 'Bin'): scriptDir = scriptDir[:-4]

    myPaths = [
            os.path.normpath(scriptDir),
            os.path.normpath('%s/bin'    % (scriptDir) ),
            os.path.normpath('%s/Config' % (scriptDir) ),
            # os.path.normpath('%s/Loreto/ProjectsAppl/_Python/LnFunctions/Functions' % (drive) ),
            os.path.normpath('%(scriptDir)s/bin/LnFuncs201206.zip' % vars() ),
        ]

    for path in myPaths:  sys.path.insert(0, path)

    os.environ['PYTHONPATH'] = os.pathsep.join(myPaths)
    os.environ['LnProjectID'] = MainProgramName

    fDEBUG = False
    fDEBUG = True
    if fDEBUG:
        print 'MainProgramName.....', MainProgramName
        print 'PYTHONPATH......'
        for path in os.getenv('PYTHONPATH').split(os.pathsep):
            print "     ", path


    return MainProgramName

# pprint.pprint( globals() )
# sys.exit()



################################################################################
# - M A I N
################################################################################
def Main(args):
    MainProgramName = setBaseEnv()
    PYTHON_DEBUGGER = os.getenv('PY_DEBUGGER')

    try:
        mainProgram  = MainProgramName + '_Main'

        if PYTHON_DEBUGGER:
            MAIN = __import__('MP3Catalog_Main')                        # WinPDB - Debugger
        else:
            MAIN = __import__(mainProgram)                        # mainProgram senza FULLPATH e senza EXT

        MAIN.Main(MainProgramName, sys.argv[1:])

    except ImportError, why:
        print "IMPORT failed:", why
        sys.exit()

    print "Process completed."
    sys.exit()



if __name__ == "__main__":
    Main(sys.argv)