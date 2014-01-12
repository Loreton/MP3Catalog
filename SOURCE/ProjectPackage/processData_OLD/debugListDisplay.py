#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types

def debugListDisplay(RandomDict):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))
    StatusSectID = RandomDict.getValue(STATUS_HLQ)
    MyLogger.info("."*30)
    for varName, varValue in sorted(StatusSectID.items()):
        validTypes =  [types.IntType, types.StringType, types.FloatType, types.LongType, types.BooleanType]
        if type(varValue) in validTypes:
            MyLogger.info( "%-35s = %s" % (varName, varValue) )


    for typeName in TYPES:
        TypeSectID   = RandomDict.get(typeName)
        MyLogger.info("."*30)
        for varName, varValue in sorted(TypeSectID.items()):
            validTypes =  [types.IntType, types.StringType, types.FloatType, types.LongType, types.BooleanType]
            if type(varValue) in validTypes:
                MyLogger.info( "%-35s = %s" % (varName, varValue) )

    print

    # choice = LnSys.getKeybKeyboardInput("******* Vuoi continuare???", keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
