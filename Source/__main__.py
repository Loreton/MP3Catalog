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
################################################################################
if __name__ == "__main__":
    Prj.Version  = 'V01'
    gv           = Ln.LnDict()      # default = _dynamic=False
    gv.Prj       = Prj
    gv.Ln        = Ln
    Prj.name     = 'MP3Catalog'
    Prj.prefix   = 'MP3Catalog'

        # ----------------------------------------------------
        # - lettura dei parametri di input
        # - Nel caso specifico abbiamo un argomento multiValue
        # -   e quindi passiamo i valori validi per detto argomento.
        # ----------------------------------------------------

    # gv.songFilter.excludeType   = ['Bambini', 'Natale', 'Popolari', 'Themes']
    # gv.songFilter.excludeAuthor = []
    # gv.songFilter.column        = ['Type', 'Author Name', 'Album Name', 'Song Name', 'Punteggio', 'Analizzata', 'Recomended', 'Loreto', 'Buona', 'Soft', 'Vivace', 'Molto Viv', 'Camera', 'Car', 'Lenta', 'Country', 'Strumentale', 'Classica', 'Lirica', 'Live', 'Discreta', 'Undefined', 'Avoid it', 'Confusionaria', 'Song Size']

    songColumns = 'Type;Author Name;Album Name;Song Name;Punteggio;Analizzata;Recomended;Loreto;Buona;Soft;Vivace;Molto Viv;Camera;Car;Lenta;Country;Strumentale;Classica;Lirica;Live;Discreta;Undefined;Avoid it;Confusionaria;Song Size'
    gv.Prj.songColumsName = songColumns.replace(' ', '').split(';')
    gv.Prj.songAttributes = gv.Prj.songColumsName[6:-1] # partiamo da Recomended



    Input           = Prj.setup.parseInput(gv, args=sys.argv[1:], columnsName=gv.Prj.songAttributes)
    gv.INPUT_PARAM  = gv.Ln.LnDict(Input)
    # if gv.INPUT_PARAM.fTRACE: gv.printDict(gv)

    gv.fEXECUTE    = gv.INPUT_PARAM.fEXECUTE
    gv.fIMPORT_EXCEL  = gv.INPUT_PARAM.fIMPORT_EXCEL
    gv.LogCONSOLE = gv.INPUT_PARAM.LogCONSOLE
    gv.fDEBUG     = gv.INPUT_PARAM.fDEBUG

        # ---------------------------------------------------------
        # - SetUp dell'ambiente
        # ---------------------------------------------------------
    Prj.setup.setupEnv(gv)

        # ---------------------------------------------------------
        # - SetUp del log
        # ---------------------------------------------------------
    logger = Prj.setup.setupLog(gv)


        # --------------------------------------------------------
        # - CALL Project MAIN Program
        # --------------------------------------------------------
    # import MP3Catalog as MP3Catalog

    # Prj.main.MP3Catalog.Main(gv, sys.argv)
    Prj.Main(gv, gv.INPUT_PARAM.songAction)

    gv.Ln.exit(gv, 0, "completed", printStack=False, stackLevel=9, console=True)
    # gv.Ln.exit(gv, 0, "--------------- debugging exit ----------------", printStack=False, stackLevel=9, console=True)


