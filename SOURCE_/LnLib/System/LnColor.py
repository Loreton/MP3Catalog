#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
from .. import colorama

'''
    C = gv.Ln.Colors()
    C.printRed('loreto', tab=5)
    C.printERROR('loreto', tab=20)
'''
class LnColors:
    colorama.init(autoreset=True)
    # for i in dir('LnColors'): print (i)
    '''
        devo mantenere i valori seguenti perché a volte
        devo mandare una stringa pronta con il colore e non posso usare il printColor(msg) oppure il getColor()
        in quanto ho una stringa multicolor
        usageMsg = " {COLOR}   {TEXT} {COLRESET}[options]".format(COLOR=C.YEL, TEXE='Loreto', COLRESET=C.RESET)

    '''
    FG         = colorama.Fore
    BG         = colorama.Back
    HI         = colorama.Style

    CRITICAL   = FG.BLUE
    ERROR      = FG.RED
    WARNING    = FG.MAGENTA
    INFO       = FG.GREEN

    BLACK      = FG.BLACK
    RED        = FG.RED
    GREEN      = colorama.Fore.GREEN
    YELLOW     = FG.YELLOW
    BLUE       = FG.BLUE
    MAGENTA    = FG.MAGENTA
    FUCSIA     = FG.MAGENTA + HI.BRIGHT
    CYAN       = FG.CYAN
    WHITE      = FG.WHITE

    REDH       = FG.RED    + HI.BRIGHT
    GREENH     = FG.GREEN  + HI.BRIGHT
    YELLOWH    = FG.YELLOW + HI.BRIGHT
    CYANH      = FG.CYAN   + HI.BRIGHT

    RESET      = HI.RESET_ALL

    BW         = FG.BLACK + BG.WHITE
    BWH        = FG.BLACK + BG.WHITE + HI.BRIGHT




    def printYellow(self, msg, tab=0, end='\n', reset=True):
        self._print (self.YELLOW + ' '*tab, msg, end, reset)

    def printYellowH(self, msg, tab=0, end='\n', reset=True):
        self._print (self.YELLOWH + ' '*tab, msg, end, reset)

    def printGreen(self, msg, tab=0, end='\n', reset=True):
        self._print (self.GREEN + ' '*tab, msg, end, reset)

    def printBlue(self, msg, tab=0, end='\n', reset=True):
        self._print (self.BLUE + ' '*tab, msg, end, reset)

    def printMagenta(self, msg, tab=0, end='\n', reset=True):
        self._print (self.MAGENTA + ' '*tab, msg, end, reset)

    def printFucsia(self, msg, tab=0, end='\n', reset=True):
        self._print (self.FUCSIA + ' '*tab, msg, end, reset)

    def printCyan(self, msg, tab=0, end='\n', reset=True):
        self._print (self.CYAN + ' '*tab, msg, end, reset)

    def printCyanH(self, msg, tab=0, end='\n', reset=True):
        self._print (self.CYANH + ' '*tab, msg, end, reset)

    def printWhite(self, msg, tab=0, end='\n', reset=True):
        self._print (self.WHITE + ' '*tab, msg, end, reset)

    def printRed(self, msg, tab=0, end='\n', reset=True):
        self._print (self.RED + ' '*tab, msg, end, reset)

    def printRedH(self, msg, tab=0, end='\n', reset=True):
        self._print (self.REDH + ' '*tab, msg, end, reset)


        # -----------------------------------------------
        # - ritorna una stringa colorata come richiesto
        # -----------------------------------------------
    def getYellow(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.YELLOW + ' '*tab, msg, end, reset)

    def getYellowH(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.YELLOWH + ' '*tab, msg, end, reset)

    def getGreen(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.GREEN + ' '*tab, msg, end, reset)

    def getBlue(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.BLUE + ' '*tab, msg, end, reset)

    def getMagenta(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.MAGENTA + ' '*tab, msg, end, reset)

    def getFucsia(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.FUCSIA + ' '*tab, msg, end, reset)

    def getCyan(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.CYAN + ' '*tab, msg, end, reset)

    def getWhite(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.WHITE + ' '*tab, msg, end, reset)

    def getRed(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.RED + ' '*tab, msg, end, reset)

    def getRedH(self, msg, tab=0, end='\n', reset=True):
        return self._print (self.REDH + ' '*tab, msg, end, reset)




        #  aliases
    YEL         = YELLOW

    printERROR  = printRedH
    # getREDH     = printRedH
    # getYellow   = printYellow
    # getGreen    = printGreen
    # getFucsia   = printFucsia
    # getWhite    = printWhite
    # getMagenta  = printMagenta
    # getCyan     = printCyan


        # common
    def _print(self, color, msg, end, reset=True):
        endColor = self.RESET if reset else ''
        outText = color + msg + endColor

        callerFunc = sys._getframe(1).f_code.co_name
        if callerFunc.startswith('get'):
            return outText
        else:
            print (outText, end=end )
            return None

