#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import sys
import platform


# - sys.version_info(major=3, minor=3, micro=2, releaselevel='final', serial=0)
v = sys.version_info
pyVer = '{0}{1}{2}'.format(v.major, v.minor, v.micro)
OpSys = platform.system()


from . System.LnLogger                      import setLogger
from . System.LnLogger                      import initLogger
from . System.LnLogger                      import setNullLogger
from . System.GetKeyboardInput              import getKeyboardInput
from . System.Exit                          import exit
from . System.LnColor                       import LnColors as Colors


from . LnDict                               import DotMap  as LnDict
from . LnDict.PrintDictionaryTree           import printDictionaryTree as printDict

from . LnFile.ReadIniFile                   import ReadIniFile


from . Excel.LnExcel_Class              import Excel


