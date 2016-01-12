#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

try:
    from dotmap import DotMap   # da decidere se usarlo sempre
    from .Setup.SetUpEnv_DotMap      import setUpEnv          # richiamato Prj.globalVariables()
    DOTMAP = True
except:
    from .Setup.SetUpEnv_LnClass     import setUpEnv          # richiamato Prj.globalVariables()
    DOTMAP = False

# from .Setup.SetUpEnv                import setUpEnv          # richiamato Prj.globalVariables()


# init_Type1                - nel folder della funzione scrivo: from <function> import *
from . import Functions              as funcs
from . import Setup                  as setup
from . import Extract                as extract
from . import Excel                  as excel
from . import Main                   as main                         # richiamato Prj.main.MP3Catalog()
from . import LnSqlite               as sql

from .Main.MainProject              import Main                     # richiamato Prj.Main()

class LnClass(): pass       # accedibile via Prj.LnClass()  <class 'ProjectPackage.LnClass'>

# ====================================================================================
# richiamando questa funzione posso dirottare l'out della log su CONSOLE previa
# impostazione del logger.ini con:
#
#        [logger_LnConsole]
#            handlers=consoleHandler
#            level=DEBUG
#            qualname=LnConsole
#            propagate=0
#
#  call: logger = gv.Prj.consoleLOG(gv, __name__)
#  Copia di quanto definito anche su LNFunctions
# ====================================================================================
def consoleLOG(gv, module):
    return gv.LN.logger.setLogger(gv, package='LnConsole.{0}'.format(module.split('.')[-1]))
