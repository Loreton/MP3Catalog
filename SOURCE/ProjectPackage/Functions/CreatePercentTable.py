#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ....
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os
import sys


#####################################################################
# - createTables(gv)
# - Analizza la sezione del DB_Tables e cerca di crere le tabelle
#
#    Table.MP3.name         = LoretoMP3, forceCreate
#    Table.MP3.struct       = create table if not exists ${Table.MP3.name} (
#                                "Type"              STRING  NOT NULL,
#                                "Author Name"       STRING  NOT NULL
#                            )
#####################################################################

def createPercentTable(gv, DB, iniSectID, newTblPfx=None, mainTable=None):
    logger      = gv.LN.setLogger(gv, __name__, LnConsole=True)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))

    xx = newTblPfx + '.name'
    logger.debug(iniSectID[xx])
    newTableName = iniSectID[newTblPfx + '.name']

    cur = DB.cursor()

        # ----------------------------------------------------------
        # - Leggiamo la colonna Type ed estraiamo le voci differenti
        # ----------------------------------------------------------
    comando = "select distinct {COLUMN} from {TABLE};".format(TABLE=mainTable, COLUMN='Type')
    result = cur.execute(comando).fetchall()
    logger.debug("Comando:  {0}".format(comando))
    logger.debug("resType:  {0}".format(type(result)))
    logger.debug("result:   {0}".format(result))
    songTypes = [tup[0] for tup in result]
    logger.debug("Types:    {0}".format(songTypes))


        # -----------------------------------------------------------
        # - Preparazione della Struttura della tabella da creare
        # -----------------------------------------------------------
    TableStruct = '("Type"              TEXT  NOT NULL,'
    for tipo in songTypes:
        TableStruct += '"{TIPO}" INTEGER DEFAULT (0),'.format(TIPO=tipo)
    TableStruct += 'primary key ("Type") )'


        # ------------------------------------------
        # - identificazione TableName e forceCreate
        # ------------------------------------------
    tableRef    = TableVars.split(',')
    tableName   = tableRef[0].strip()
    forceCreate = True if tableRef[1].strip().lower() == 'forcecreate' else False
    preLoadTable= True if tableRef[2].strip().lower() == 'preload' else False


        # --------------------
        # - Creazione tabella
        # --------------------
    gv.Prj.sql.createTable(gv, DB, tableName, forceCreate=forceCreate,  struct=TableStruct)

        # -------------------
        # - Precaricamento
        # -------------------
    if preLoadTable:
        try:
            data = iniSectID[newTblPfx + '.data']
        except:
            data = ['DEFAULT']
            for tipo in songTypes:
                data.append(0)

        gv.Prj.sql.insertRow(gv, DB, TblName=tableName, record=data, commit=True)

