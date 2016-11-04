#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import sys, os
import platform


# - sys.version_info(major=3, minor=3, micro=2, releaselevel='final', serial=0)
v = sys.version_info
pyVer = '{0}{1}{2}'.format(v.major, v.minor, v.micro)
OpSys = platform.system()
# print (os.getcwd())
# sys.path.insert(0, os.path.abspath('System'))
# sys.path.insert(0, os.path.abspath('System/LnLogger'))
# sys.path.insert(0, os.path.abspath('System'))
# sys.path.insert(0, os.getcwd())
# sys.exit()

from . LnCommon.LnLogger                      import SetLogger
from . LnCommon.LnLogger                      import InitLogger
from . LnCommon.LnLogger                      import SetNullLogger

from . LnCommon.LnColor                       import LnColor

from . System.GetKeyboardInput              import getKeyboardInput
from . System.Exit                          import Exit


from . LnDict                               import DotMap  as LnDict
from . LnDict.PrintDictionaryTree           import printDictionaryTree as printDict

from . LnFile.ReadIniFile_Class                   import ReadIniFile
from . LnFile.DirList                   import DirList
from . LnFile.FileStatus                  import FileModificationTime as Fmtime


from . Excel.LnExcel_Class              import Excel

