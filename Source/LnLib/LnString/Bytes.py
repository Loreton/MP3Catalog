#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# see:
#   http://www.diveintopython3.net/strings.htmlno
#   http://stackoverflow.com/questions/14682397/can-somone-explain-how-unicodedata-normalizeform-unistr-work-with-examples
#   byData = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
#                                               by Loreto Notarantonio 2014, August
# ######################################################################################
import codecs
def stringToBytes1(STRING ):
    bytesOut = codecs.latin_1_encode(STRING)[0]
    return bytesOut

def stringToBytes(STRING ):
    bytesOut = STRING.encode('utf-8')
    return bytesOut

def bytesToString(BYTES ):
    string = BYTES.decode('utf-8')
    return string

def bytesFind(string1, string2):
    if string1 in string2:
        # print ("FOUND IT")
        return True
    else:
        # print ("NOT FOUND")
        return False