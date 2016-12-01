#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4

# sudo update-alternatives --config python
# /opt/python3.4/bin/pip3.4 install netifaces
import sys; sys.dont_write_bytecode = True
# import sys
import os

# ------------------------------------------------------------
# - Inserimento delle directory del progetto nelle sysPath
# ------------------------------------------------------------

# solo per caricare il modulo setupEnv()
# import Setup as setup

import Project    as Prj
import LnLib     as Ln

################################################################################
# - M A I N
#    gv.song.primaryCols    = []
#    gv.song.attributeCols  = []
#    gv.song.colsName       = []
#    gv.song.field[colname] = enum
################################################################################
if __name__ == "__main__":
    Prj.Version  = 'V01'
    gv           = Ln.LnDict()      # default = _dynamic=False
    gv.Prj       = Prj
    gv.Ln        = Ln
    Prj.name     = 'MP3Catalog'
    Prj.prefix   = 'MP3Catalog'


    # ---------------------------------------------------------
    # - per iniziare disabilitiamo il LOG
    # ---------------------------------------------------------
    logger = gv.Ln.SetNullLogger()


    # ---------------------------------------------------------
    # - SetUp dell'ambiente
    # ---------------------------------------------------------
    Prj.SetupEnv(gv, fDEBUG=False)


    # ------------------------------------------------------------------
    # - Lettura del file ini perché
    # - mi servono i nomi delle colonne
    # - per il controllo dell'input.
    # ------------------------------------------------------------------
    iniFile = gv.Ln.ReadIniFile(gv.Prj.iniFileName)
    iniFile.read()
    gv.ini = gv.Ln.LnDict(iniFile.dict)
    # gv.ini.printDict(gv, fEXIT=True)

    primaryCols   = ''.join(gv.ini.EXCEL.NomiColonnePrimarie.split('\n'))
    attributeCols = ''.join(gv.ini.EXCEL.NomiAttributi.split('\n'))

        # rimuovi i BLANK all'interno dei nomi ei campi
    primaryCols   = primaryCols.replace(' ', '')
    attributeCols = attributeCols.replace(' ', '')
    songColumns   = primaryCols + ','+ attributeCols


    gv.song = gv.Ln.LnDict()
    gv.song.primaryCols   = [x.strip() for x in primaryCols.split(',')]
    gv.song.attributeCols = [x.strip() for x in attributeCols.split(',')]
    gv.song.colsName      = gv.song.primaryCols[:]
    gv.song.colsName.extend(gv.song.attributeCols)

        # - pseudo enum delle colonne
    gv.song.field = gv.Ln.LnDict()
    for index, colName in enumerate(gv.song.colsName):
        gv.song.field[colName] = index


    # ------------------------------------------------------------------
    # - lettura dei parametri di input
    # - Nel caso specifico abbiamo un argomento multiValue
    # -   e quindi passiamo i valori validi per detto argomento.
    # ------------------------------------------------------------------
    Input           = Prj.ParseInput(gv, args=sys.argv[1:], columnsName=gv.song.attributeCols)
    gv.INPUT_PARAM  = gv.Ln.LnDict(Input)
    gv.PrintTree()
    # gv.INPUT_PARAM.PrintDict(fEXIT=True)
    gv.fDEBUG        = gv.INPUT_PARAM.fDEBUG



        # ---------------------------------------------------------
        # - SetUp del log
        # ---------------------------------------------------------
    logger = Prj.SetupLog(gv)


    Prj.Main(gv, gv.INPUT_PARAM.songAction)

    gv.Ln.Exit(0, "completed", printStack=False, stackLevel=9, console=True)
    gv.Ln.Exit(0, "--------------- debugging exit ----------------", printStack=False, stackLevel=9, console=True)
    sys.exit()



