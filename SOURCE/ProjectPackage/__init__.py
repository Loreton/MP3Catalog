#!/usr/bin/python
# -*- coding: iso-8859-1 -*-


class LnClass(): pass       # accedibile via Prj.LnClass()  <class 'ProjectPackage.LnClass'>

# init_Type1                - nel folder della funzione scrivo: from <function> import *
from . import Functions              as funcs
from . import Setup                  as setup
from . import Extract                as extract
from . import Excel                  as excel
from . import Main                   as main                         # richiamato Prj.main.MP3Catalog()

from .Main.MainProject              import Main                     # richiamato Prj.Main()
from .Setup.SetUpEnv               import setUpEnv          # richiamato Prj.globalVariables()


