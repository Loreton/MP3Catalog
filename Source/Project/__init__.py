#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

# import sys, os
# import time
# import pathlib as p         # dalla versione 3.4

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-


################################################
#
################################################
# -------------------------------------------
# - import della LnPythonLib
# - mi aspetto la dir prhjDir/SOURCE/LnLib
# -------------------------------------------
# try:
#     from . import LnLib   as Ln
# except:
#     print ('LnLib directory NOT FOUND ...importing main LnPythonLib')
#     thisDir     = p.Path(__file__).resolve().parent
#     sys.path.insert(0, str(thisDir.parents[1]))  # per LnPythonLib
#     import LnPythonLib   as Ln




from . Main.MP3Catalog              import  Main
# from . Main.MP3CatalogSqlLite       import  Main




from . import Setup     as setup
from . import Functions as func

from . Functions.SongFilter         import  songFilter
from . Functions.SongFilter         import  songFilter

from . Functions.ReadWriteFile      import  readFile
from . Functions.ReadWriteFile      import  writeFile

from . Functions.CopySongs          import  copySongs
from . Functions.CheckSourceSongs   import  checkSourceSongs
from . Functions.ReadCSVFile        import  ReadCSVFile

from . Functions.LnEnum             import  enumCols
from . Functions.LnEnum             import  enumColsKeyVal
from . Functions.LnEnum             import  enumColsBase2



