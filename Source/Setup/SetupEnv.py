#!/opt/python3.4/bin/python3.4

import sys, os
import time
import pathlib as p         # dalla versione 3.4


def setupEnv(gv):
    C = gv.Ln.Colors()
        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
    scriptMain  = p.Path(sys.argv[0]).resolve()
    prjBaseDIR  = scriptMain.parent
    scriptName  = scriptMain.name
    prjName     = prjBaseDIR.stem
    scriptExt   = scriptMain.suffix[1:]


    configDIR   = prjBaseDIR.joinpath('conf')
    dataDIR     = prjBaseDIR.joinpath('data')

        # ---------------------------------------------------------
        # - file di configurazione
        # ---------------------------------------------------------
    iniFileName = configDIR.joinpath(gv.Prj.prefix + '_' + gv.Prj.Version + '.ini')


    gv.Prj.scriptName  = str(scriptName)
    gv.Prj.prjBaseDIR  = str(prjBaseDIR)
    gv.Prj.configDIR   = str(configDIR)
    gv.Prj.dataDIR     = str(dataDIR)
    gv.Prj.iniFileName = str(iniFileName)


    now     = time.localtime()
    gv.Prj.now     = now
    gv.Prj.today   = '{YY:04}.{MM:02}.{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.Prj.DATE    = '{YY:04}{MM:02}{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.Prj.TIME    = '{HH:02}{MM:02}{SS:02}'.format(HH=now.tm_hour, MM=now.tm_min, SS=now.tm_sec)

    if gv.fDEBUG:
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        C.printCyan('scriptName       {0}'.format(gv.Prj.scriptName), tab=8)
        C.printCyan('prjBaseDIR       {0}'.format(gv.Prj.prjBaseDIR), tab=8)
        C.printCyan('configDIR        {0}'.format(gv.Prj.configDIR), tab=8)
        C.printCyan('dataDIR          {0}'.format(gv.Prj.dataDIR), tab=8)
        C.printCyan('iniFileName      {0}'.format(gv.Prj.iniFileName), tab=8)
        print ()
        C.printCyan('today            {0}'.format(gv.Prj.today), tab=8)
        C.printCyan('DATE - TIME      {0} - {1}'.format(gv.Prj.DATE, gv.Prj.TIME), tab=8)
        C.printCyan('now              {0}'.format(gv.Prj.now), tab=8)
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()



