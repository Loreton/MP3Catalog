#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import sys, os
import platform


# - sys.version_info(major=3, minor=3, micro=2, releaselevel='final', serial=0)
v = sys.version_info
pyVer = '{0}{1}{2}'.format(v.major, v.minor, v.micro)
OpSys = platform.system()


from . LnCommon.LnLogger                import SetLogger
from . LnCommon.LnLogger                import InitLogger
from . LnCommon.LnLogger                import SetNullLogger
from . LnCommon.LnColor                 import LnColor
from . LnCommon.Exit                    import Exit
from . System.ExecRcode                 import ExecRcode

from . System.GetKeyboardInput          import getKeyboardInput


from . LnDict                           import DotMap  as LnDict
from . LnString.LnEnum                  import LnEnum

# from . LnDict.PrintDictionaryTree       import printDictionaryTree as printDict

# from . LnDict.DictToList                import KeyTree
# from . LnDict.DictToList                import KeyList
# from . LnDict.DictToList                import PrintTree

from . LnFile.ReadIniFile_Class         import ReadIniFile
from . LnFile.DirList                   import DirList
from . LnFile.FileStatus                import FileModificationTime as Fmtime
from . LnFile.ReadWriteTextFile         import readTextFile
from . LnFile.ReadWriteTextFile         import writeTextFile


from . SqLite.LnSqLite_Class                import LnSqLite

from . Excel.LnExcel_Class              import Excel

