#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4

# sudo update-alternatives --config python
# /opt/python3.4/bin/pip3.4 install netifaces
# import sys; sys.dont_write_bytecode = True
import sys
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
################################################################################
if __name__ == "__main__":
    Prj.Version  = 'V01'
    gv           = Ln.LnDict()      # default = _dynamic=False
    gv.Prj       = Prj
    gv.Ln        = Ln
    Prj.name     = 'MP3Catalog'
    Prj.prefix   = 'MP3Catalog'


    '''
    -----------------------------------------------
        per iniziare disabilitiamo il LOG
    -----------------------------------------------
    '''
    logger = gv.Ln.SetNullLogger()


        # ---------------------------------------------------------
        # - SetUp dell'ambiente
        # ---------------------------------------------------------
    Prj.setup.setupEnv(gv, fDEBUG=False)


    # ------------------------------------------------------------------
    # - Lettura del file ini perché
    # - mi servono i nomi delle colonne
    # - per il controllo dell'input.
    # ------------------------------------------------------------------
    # iniConfigParser, iniDict = gv.Ln.ReadIniFile(gv.Prj.iniFileName, RAW=False, exitOnError=True, subSectionChar='.')
    # gv.ini = gv.Ln.LnDict(iniDict)
    iniFile = gv.Ln.ReadIniFile(gv.Prj.iniFileName)
    iniFile.read()
    gv.ini = gv.Ln.LnDict(iniFile.dict)
    # gv.ini.printDict(gv, fEXIT=True)

    songColumns = ''.join(gv.ini.EXCEL.NomiColonnePrimarie.split('\n'))
    songColumns += ','+ ''.join(gv.ini.EXCEL.NomiAttributi.split('\n'))
    songColumns = songColumns.replace(' ', '')

    gv.Prj.songColumsName = [x.strip() for x in songColumns.split(',')]
    gv.Prj.songAttributes = gv.Prj.songColumsName[6:-1] # partiamo da Recomended



    # ------------------------------------------------------------------
    # - lettura dei parametri di input
    # - Nel caso specifico abbiamo un argomento multiValue
    # -   e quindi passiamo i valori validi per detto argomento.
    # ------------------------------------------------------------------
    Input           = Prj.setup.parseInput(gv, args=sys.argv[1:], columnsName=gv.Prj.songAttributes)
    gv.INPUT_PARAM  = gv.Ln.LnDict(Input)
    # gv.INPUT_PARAM.printDict(gv)
    gv.fDEBUG        = gv.INPUT_PARAM.fDEBUG



        # ---------------------------------------------------------
        # - SetUp del log
        # ---------------------------------------------------------
    logger = Prj.setup.setupLog(gv)


    Prj.Main(gv, gv.INPUT_PARAM.songAction)

    gv.Ln.Exit(0, "completed", printStack=False, stackLevel=9, console=True)
    gv.Ln.Exit(0, "--------------- debugging exit ----------------", printStack=False, stackLevel=9, console=True)
    sys.exit()



