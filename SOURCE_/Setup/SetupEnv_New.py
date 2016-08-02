#!/opt/python3.4/bin/python3.4

import sys, os
import time
import pathlib as p         # dalla versione 3.4

def setupEnv(Prj, LnLib=None):
        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
    scriptMain  = p.Path(sys.argv[0]).resolve()
    prjBaseDIR  = scriptMain.parent
    scriptName  = scriptMain.name
    prjName     = prjBaseDIR.stem
    scriptExt   = scriptMain.suffix[1:]

    prjDirs = [prjBaseDIR, prjBaseDIR / 'bin', prjBaseDIR / 'SOURCE']


        # ------------------------------------------
        # - Preparazione directories per LnLib
        # ------------------------------------------
    LnLibPath = prjBaseDIR.parent

    if scriptExt == 'zip':
        pass

    if LnLib.endswith('.zip'):
        LnLibPath = os.path.abspath(os.path.join(prjBaseDIR, LnLib))
        prjDirs.append(LnLibPath)                         # zipFile  della LnLib

    prjDirs.append(LnLibPath)        # Per la directory della LnLib

        # --------------------------------
        # - Controloo percorso LnLib
        # --------------------------------
    if not LnLibPath.is_dir() and not LnLibPath.is_file():
        print()
        print('File/dir {0} NOT Found...'.format(LnLibPath))
        print()
        sys.exit()

        # --------------------------------
        # - Inserimeto directories nelle path
        # --------------------------------
    for myDir in prjDirs:
        if not myDir in sys.path:
            sys.path.insert(0, str(myDir.resolve()))

    # for path in sys.path: print (path)
        # --------------------------------
        # - import dei packages LnLib
        # --------------------------------
    if (prjBaseDIR / 'SOURCE/LnLib').is_dir():
        print ('...importing local prjLnLib')
        import LnLib   as Ln
    else:
        import LnPythonLib   as Ln

    now     = time.localtime(); now = now
    today   = '{YY:04}{MM:02}{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)

    Prj.scriptName  = str(scriptName)
    Prj.prjBaseDIR  = str(prjBaseDIR)
    Prj.configDIR   = str(prjBaseDIR / 'conf')
    Prj.dataDIR     = str(prjBaseDIR / 'data')

    return Ln
