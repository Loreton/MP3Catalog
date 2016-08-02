#!/opt/python3.4/bin/python3.4

import sys, os
import time

def setupEnv(Prj, LnLib=None):
        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
    scriptDir             = os.path.dirname(os.path.abspath(sys.argv[0]))
    scriptName, scriptExt = os.path.basename(os.path.abspath(sys.argv[0])).split('.')
    baseDIR     = scriptDir

    prjDirs = [baseDIR, baseDIR+'/bin', baseDIR+'/SOURCE']


        # ------------------------------------------
        # - Preparazione directories per LnLib
        # ------------------------------------------
    LnLibPath = os.path.dirname(baseDIR)

    if scriptExt == 'zip':
        pass

    if LnLib.endswith('.zip'):
        LnLibPath = os.path.abspath(os.path.join(baseDIR, LnLib))
        prjDirs.append(LnLibPath)                         # zipFile  della LnLib

    prjDirs.append(LnLibPath)        # Per la directory della LnLib

        # --------------------------------
        # - Controloo percorso LnLib
        # --------------------------------
    if not os.path.isdir(LnLibPath) and not os.path.isfile(LnLibPath):
        print()
        print('File/dir {0} NOT Found...'.format(LnLibPath))
        print()
        sys.exit()

        # --------------------------------
        # - Inserimeto directories nelle path
        # --------------------------------
    for prjDir in prjDirs:
        if not prjDir in sys.path:
            sys.path.insert(0, os.path.abspath(prjDir))

    # for path in sys.path: print (path)
        # --------------------------------
        # - import dei packages LnLib
        # --------------------------------
    if os.path.isdir(baseDIR + '/SOURCE/LnLib'):
        print ('...importing local prjLnLib')
        import LnLib   as Ln
    else:
        import LnPythonLib   as Ln

    now     = time.localtime(); now = now
    today   = '{YY:04}{MM:02}{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)

    Prj.scriptName  = scriptName
    Prj.baseDIR     = baseDIR
    Prj.configDIR   = baseDIR + '/conf'
    Prj.dataDIR    = baseDIR + '/data'

    return Ln
