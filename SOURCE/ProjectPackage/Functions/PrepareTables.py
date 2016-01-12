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
def prepareTables(gv, DB, DBSectID, csvData):
    logger      = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:{CALLER}]'.format(CALLER=calledBy(1)))


    for key, val in DBSectID.items():
        # print (key)
        if key.startswith('Table.') and key.endswith('.struct'):
            (left, midName, right) = key.split('.')

                # identificazione TableName e forceCreate
            keyName     = '{LEFT}.{MID}.name'.format(LEFT=left, MID=midName)
            tableRef    = DBSectID[keyName].split(',')
            tableName   = tableRef[0].strip()
            forceCreate = True if tableRef[1].strip().lower() == 'forcecreate' else False
            preLoadTable= True if tableRef[2].strip().lower() == 'preload' else False
            # print('.............', len(tableRef), tableRef)
            recordSep   = tableRef[3].strip() if len(tableRef) > 3 else '\n'

                # Creazione tabella
            gv.Prj.sql.createTable(gv, DB, tableName, forceCreate=forceCreate,  struct=val)

                # per la Tabella primaria vediamo se importare i dati da csvData
            if midName == 'MP3' and csvData:
                rCode = gv.Prj.sql.insertRow(gv, DB, TblName=tableName, record=csvData)

                # Se per questa tablella è previsto un precaricamento ...
            if forceCreate and preLoadTables:
                keyName = '{LEFT}.{MID}.data'.format(LEFT=left, MID=midName)
                data = DBSectID.get(keyName)
                if data:
                    preLoadTables(gv, DB, tableName, data, recordSep)

                # inseriamo i nomi delle tabelle

            if gv.DOTMAP:
                gv.Table[midName] = gv.LnClass()
                gv.Table[midName].name = tableName
            else:
                if not hasattr(gv.Table, midName):
                    setattr(gv.Table, midName, gv.LnClass())
                gv.Table.__dict__[midName].name = tableName


#####################################################################
# - preLoadTables(gv)
# - Precarica i dati nella tabella Table.Percent.name
# - Per ogni riga sarà creata una LIST ed il tutto in una LIST esterna
# -          [
# -             ['Natale', '0']
# -             ['xxxx', 'x']
# -          ]
#    Table.Percent.data     =    Natale     :  0
#                                Bambini    :  0
#                                Italiani   : 71
#                                Stranieri  : 20
#                                Themes     :  0
#                                Classica   :  0
#                                Popolari   :  5
#                                Country    : 10
#                                Chitarra   :  5
#####################################################################
def preLoadTables(gv, DB, tableName, inpData, recordSEP):

    fieldSEP = ':'
    Records = [x.replace('\n', '').strip() for x in inpData.split(recordSEP) if x]
    print ('    ...preloading Table {TABLE} - nFields: {LEN}'.format(TABLE=tableName, LEN=len(Records[0].split(fieldSEP))))
    data = []
    for x in Records:
        if x:
            Vals = x.split(fieldSEP)
            line = []
            for val in Vals:
                line.append(val.strip())
            data.append(line)


    gv.Prj.sql.insertRow(gv, DB, TblName=tableName, record=data)
