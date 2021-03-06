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




from . Main.MainSqLite              import  Main as MainSqLite
from . Main.MainExcel               import  Main as MainExcel


from . import Setup     as setup
from . import Functions as func

from . Setup.SetupEnv               import   SetupEnv
from . Setup.SetupLog               import   SetupLog
from . Setup.ParseInput              import  ParseInput


from . Functions.SongFilter         import  songFilter
# from . Functions.SqlSongFilter         import  SqlSongFilter # NON completata perché forse più complessa della songsFilter
from . Functions.Merge              import  Merge
from . Functions.Validate              import  Validate

from . Functions.CopySongs          import  copySongs
# from . Functions.CheckSourceSongs   import  checkSourceSongs
from . Functions.CSVFile            import  ReadCSVFile
from . Functions.CSVFile            import  WriteCSVFile
from . ExcelDB.ExcelCatalog         import  ReadExcelDB

from . Functions.LnEnum             import  enumCols
from . Functions.LnEnum             import  enumColsKeyVal
from . Functions.LnEnum             import  enumColsBase2



