#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import sys, os
import time
import pathlib as p         # dalla versione 3.4


'''
###################################################
# funzione per semplificare l'import della LnLib
###################################################
def setupEnv():
        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
    prjBaseDIR  = p.Path(sys.argv[0]).resolve()
    thisDir     = p.Path(__file__).resolve().parent
    print (prjBaseDIR)
    print (thisDir)


        # -------------------------------------------
        # - mi aspetto la dir prhjDir/SOURCE/LnLib
        # -------------------------------------------
    if ( thisDir / 'LnLib').is_dir():
        print ('...importing local prjLnLib')
        from . import LnLib   as Ln

    else:
            # --------------------------------
            # - Inserimeto directories nelle path
            # - mi aspetto la dir prjDir/../LnPythonLib
            # --------------------------------
        prjDirs = [ prjBaseDIR, prjBaseDIR.parent, prjBaseDIR.parents[1]]      # per LnPythonLib
        for path in sys.path: print (path)
        for myDir in prjDirs:
            strDir = str(myDir.resolve())
            if not myDir in sys.path:
                sys.path.insert(0, strDir)
        for path in sys.path: print (path)
        import LnPythonLib   as Ln

'''


################################################
#
################################################
# -------------------------------------------
# - import della LnPythonLib
# - mi aspetto la dir prhjDir/SOURCE/LnLib
# -------------------------------------------
try:
    from . import LnLib   as Ln
except:
    print ('LnLib directory NOT FOUND ...importing main LnPythonLib')
    thisDir     = p.Path(__file__).resolve().parent
    sys.path.insert(0, str(thisDir.parents[1]))  # per LnPythonLib
    import LnPythonLib   as Ln

from . import Setup     as setup
from . import Functions as func



# from . Main.MP3Catalog              import  Main
from . Main.MP3CatalogSqlLite       import  Main

from . Functions.SongFilter         import  songFilter
from . Functions.SongFilter         import  songFilter

from . Functions.ReadWriteFile      import  readFile
from . Functions.ReadWriteFile      import  writeFile

from . Functions.CopySongs          import  copySongs
from . Functions.CheckSourceSongs   import  checkSourceSongs

from . Functions.LnEnum             import  enumCols
from . Functions.LnEnum             import  enumColsKeyVal



