#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4

# sudo update-alternatives --config python
# /opt/python3.4/bin/pip3.4 install netifaces
import sys; sys.dont_write_bytecode = True
import os

# ------------------------------------------------------------
# - Inserimento delle directory del progetto nelle sysPath
# ------------------------------------------------------------

# solo per caricare il modulo setupEnv()
# import Setup as setup

import SOURCE    as Prj

################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
        # LnLib è la dir delle LnFunction oppure il nome dello zip file
    Prj.Version  = 'V0.1'
    Ln           = Prj.setup.setupEnv(Prj, LnLib='LnPythonLib')
    gv           = Ln.LnDict()      # default = _dynamic=False
    gv.Prj       = Prj
    gv.Ln        = Ln
    TEST         = ''
    prefix      = 'MP3Catalog'

    if TEST: prefix =  prefix + '_TEST'


        # ----------------------------------------------------
        # - lettura dei parametri di input in un dictionary
        # ----------------------------------------------------
    Input           = Prj.setup.parseInput(gv)
    gv.INPUT_PARAM  = Ln.LnDict(Input)
    if gv.INPUT_PARAM.fDEBUG: gv.printDict(gv)


        # ---------------------------------------------------------
        # - Intercettazione per la creazione ....
        # ---------------------------------------------------------
    if gv.INPUT_PARAM.action in ['dddd', 'xxx']:
        sys.exit()


    gv.EXECUTE = gv.INPUT_PARAM.fEXECUTE
    gv.CONSOLE = gv.INPUT_PARAM.LogCONSOLE
    gv.fDEBUG  = gv.INPUT_PARAM.fDEBUG


        # ---------------------------------------------------------
        # - SetUp del log
        # ---------------------------------------------------------
    logger = Prj.setup.setupLog(gv, prefix=prefix)

        # ---------------------------------------------------------
        # - file di configurazione
        # ---------------------------------------------------------
    iniFileName = '{CONFDIR}/{PREFIX}_hostName_{VERSION}.ini'.format(CONFDIR=gv.Prj.configDIR, PREFIX=prefix, VERSION=gv.Prj.Version)
    iniFileName = os.path.normpath(iniFileName)
    iniFileName = os.path.relpath(iniFileName)


    print (iniFileName)

        # --------------------------------------------------------
        # - CALL Project MAIN Program
        # --------------------------------------------------------
    # import MP3Catalog as MP3Catalog

    # Prj.main.MP3Catalog.Main(gv, sys.argv)
    Prj.mainLite(gv)

    gv.Ln.exit(gv, 0, "completed", printStack=False, stackLevel=9, console=True)


