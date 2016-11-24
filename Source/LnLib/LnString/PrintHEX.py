#!/usr/bin/env python
# -*- coding: utf-8 -*-



def printHEX(s):
    """
    Print a string as hex bytes.
    """

    print(":".join("{0:x}".format(ord(c)) for c in s))

