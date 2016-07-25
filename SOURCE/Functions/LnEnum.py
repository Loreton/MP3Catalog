#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

def enumCols(gv, record):
        # Creiamo una enum con i nomi delle colonne
    col = gv.Ln.LnDict()

    """
      -------------------------------------------------
     sampleRecord =   "Type;Author Name;Album Name;...."
     output:
        col.Type        = 1
        col.AuthorName  = 2
        col.AlbumName   = 3
        ....
      -------------------------------------------------
    """

    for index, name in enumerate(record):
        colName = name.replace(' ', '')
        col[colName] = index
        # print (index, colName)
    return col

