#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types


# =======================================================================
# sample()
# =======================================================================
def getRealDirStatus(RandomDict):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))


    StatusSectID = RandomDict.getValue(STATUS_HLQ)
    destDIR      = StatusSectID[STATUS_DEST_DIR]

    for typeName in TYPES:
        TypeSectID  = RandomDict.getValue(typeName)
        outTypeDIR  = "%s\\%s" % (destDIR, typeName)
        StatusSectID[STATUS_COPIED_BYTES]   = LnFile.getDirSize(destDIR)

        # StatusSectID[STATUS_COPIED_SONGS]   = len(LnFile.dirListType1(destDIR, pattern='*.mp3', what='FS') )
        (rCode, list) = LnFile.dirListType1(destDIR, pattern='*.mp3', what='FS')
        if rCode: choice = LnSys.getKeyboardInput("ERROR Reading directory %s (see LOG file)" % (destDIR), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
        StatusSectID[STATUS_COPIED_SONGS]   = len(list)


        # StatusSectID[STATUS_COPIED_SONGS]   = len(LnFile.dirList(destDIR, includeFILES='*.mp3', what='FS', RETURN='INCL') )
        TypeSectID[BYTES_COPIED]            = LnFile.getDirSize(outTypeDIR)

        # TypeSectID[COPIED_SONGS]            = len(LnFile.dirListType1(outTypeDIR, pattern='*.mp3', what='FS') )
        (rCode, list) = LnFile.dirListType1(outTypeDIR, pattern='*.mp3', what='FS')
        if rCode: choice = LnSys.getKeyboardInput("ERROR Reading directory %s (see LOG file)" % (outTypeDIR), keyLIST='ENTER', exitKey='QX', AnswerForDEBUG=None)
        TypeSectID[COPIED_SONGS]   = len(list)


        # TypeSectID[COPIED_SONGS]            = len(LnFile.dirList(outTypeDIR, includeFILES='*.mp3', what='FS', RETURN='INCL') )


    # ###################################
    # choice = LnSys.getKeyboardInput("******* STOP Temporaneo *******", keyLIST='xENTER', exitKey='QX', AnswerForDEBUG=None)
    # ###################################


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
