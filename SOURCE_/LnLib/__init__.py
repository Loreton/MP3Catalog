#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import sys; sys.dont_write_bytecode = True
import platform;  OpSys = platform.system()

from . System.LnLogger                      import setLogger
from . System.LnLogger                      import initLogger
from . System.GetKeyboardInput              import getKeyboardInput

from . LnDict                               import DotMap  as LnDict
from . LnDict.PrintDictionaryTree           import printDictionaryTree as printDict

from . System.LnColor                       import  LnColors as Colors




