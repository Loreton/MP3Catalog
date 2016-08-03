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

import Source    as Prj

################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    Prj.Version  = 'V01'
    gv           = Prj.Ln.LnDict()      # default = _dynamic=False
    gv.Prj       = Prj
    gv.Ln        = Prj.Ln
    Prj.prefix     = 'MP3Catalog'

        # ----------------------------------------------------
        # - lettura dei parametri di input
        # - Nel caso specifico abbiamo un argomento multiValue
        # -   e quindi passiamo i valori validi per detto argomento.
        # ----------------------------------------------------
    # songsFlags = 'Analysed, Recomended, Loreto, Buona, Soft, Car, Vivace Molto, Vivace, Camera'
    # gv.Prj.songFlags = [
    #                 'Analizzata',
    #                 'Buona',
    #                 'Camera'
    #                 'Car',
    #                 'Loreto',
    #                 'MoltoViv',
    #                 'Recomended',
    #                 'Soft',
    #                 'Vivace',
    #             ]


    songColums = 'Type;Author Name;Album Name;Song Name;Punteggio;Analizzata;Recomended;Loreto;Buona;Soft;Vivace;Molto Viv;Camera;Car;Lenta;Country;Strumentale;Classica;Lirica;Live;Discreta;Undefined;Avoid it;Confusionaria;Song Size'
    gv.Prj.songColumName = songColums.replace(' ', '').split(';')

    # gv.Prj.songColums = [
    #                 'Type',
    #                 'Author Name',
    #                 'Album Name',
    #                 'Song Name',
    #                 'Punteggio',
    #                 'Analizzata',
    #                 'Recomended',
    #                 'Loreto',
    #                 'Buona',
    #                 'Soft',
    #                 'Vivace',
    #                 'Molto Viv',
    #                 'Camera',
    #                 'Car',
    #                 'Lenta',
    #                 'Country',
    #                 'Strumentale',
    #                 'Classica',
    #                 'Lirica',
    #                 'Live',
    #                 'Discreta',
    #                 'Undefined',
    #                 'Avoid it',
    #                 'Confusionaria',
    #                 'Song Size',
    #             ]


    Input           = Prj.setup.parseInput(gv, args=sys.argv[1:], flags=gv.Prj.songColumName)
    gv.INPUT_PARAM  = gv.Ln.LnDict(Input)
    if gv.INPUT_PARAM.fTRACE: gv.printDict(gv)

    gv.EXECUTE = gv.INPUT_PARAM.fEXECUTE
    gv.CONSOLE = gv.INPUT_PARAM.LogCONSOLE
    gv.fDEBUG  = gv.INPUT_PARAM.fDEBUG

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
    Prj.Main(gv, gv.INPUT_PARAM.action)

    gv.Ln.exit(gv, 0, "completed", printStack=False, stackLevel=9, console=True)


