#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import os

import collections
import configparser
import codecs

from ..LnCommon.LnLogger import SetLogger
from ..LnCommon.LnColor  import LnColor

# ######################################################
# # https://docs.python.org/3/library/configparser.html
# ######################################################
def ReadIniFile(fileName, RAW=False, returnOrderedDict=False, extraSections=[], exitOnError=False, STRICT=True, subSectionChar=None):
    logger  = SetLogger(package=__name__)

        # Setting del parser
    configMain = configparser.ConfigParser( allow_no_value=False,
                                        delimiters=('=', ':'),
                                        comment_prefixes=('#',';'),
                                        inline_comment_prefixes=(';',),
                                        strict=STRICT,          # True: impone unique key/session
                                        # strict=False,
                                        empty_lines_in_values=True,
                                        default_section='DEFAULT',
                                        interpolation=configparser.ExtendedInterpolation()
                                    )
    configMain.optionxform = str        # mantiene il case nei nomi delle section e delle Keys (Assicurarsi che i riferimenti a vars interne siano case-sensitive)

    try:
        data = codecs.open(fileName, "r", "utf8")
        configMain.readfp(data)

    except (Exception) as why:
        print("Errore nella lettura del file: {FILE} - {WHY}".format(FILE=fileName, WHY=str(why)))
        sys.exit(-1)



        # ------------------------------------------------------------------
        # - per tutte le sezioni che sono extra facciamo il merge.
        # - Se Key-Val esistono esse sono rimpiazzate
        # ------------------------------------------------------------------
    for sectionName in extraSections:
        logger.info('adding Section: {SECTION}'.format(SECTION=sectionName))
        logger.info('          data: {EXTRA}'.format(EXTRA=extraSections[sectionName]))
        extraSection = extraSections[sectionName]

        if not configMain.has_section(sectionName):
            logger.debug('creating Section: {0}'.format(sectionName))
            configMain.add_section(sectionName)

        for key, val in extraSection.items():
            logger.debug('adding on Section {0}:'.format(sectionName))
            logger.debug('   key: {0}'.format(key))
            logger.debug('   val: {0}'.format(val))
            configMain.set(sectionName, key, val)







        # Parsing del file
    if type(configMain) in [configparser.ConfigParser]:
        configDict = iniConfigAsDict(configMain, returnOrderedDict=returnOrderedDict, raw=RAW, subSectionChar=subSectionChar)
    else:
        configDict = configMain

    return configMain, configDict


############################################################
# subSectionChar:  carattere da individuare nel nome della section per
#                  interpretare la stessa come section+subsection
############################################################
def iniConfigAsDict(INIConfig, sectionName=None, returnOrderedDict=False, raw=False, subSectionChar=None):
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """

    the_dict = collections.OrderedDict({}) if returnOrderedDict else {}
    fDEBUG = False
    try:
        for section in INIConfig.sections():
            # -----------------------------------------------------------------------
            # - questo blocco serve per splittare eventauli section in cui il nome
            # - contiene dei '.' ed interpretarli come subSections
            # -----------------------------------------------------------------------
            if subSectionChar:
                subSection = section.split(subSectionChar)
            else:
                subSection = [section]  # una sola section

            # if len(subSection) > 1:
                # print (subSection)
            currSECT = the_dict  # top
            for sect in subSection:
                # print (sect)
                if not sect in currSECT:
                    currSECT[sect] = collections.OrderedDict({}) if returnOrderedDict else {}
                currSECT = currSECT[sect] #  aggiorna pointer


            # else: # lavoriamo solo ad un livello di section.
            #     the_dict[section] = collections.OrderedDict({}) if returnOrderedDict else {}
            #     currSECT = the_dict[section]

            if fDEBUG: print ()
            if fDEBUG: print ('[{SECT}]'.format(SECT=section))
            for key, val in INIConfig.items(section, raw=raw):
                currSECT[key] = val
                if fDEBUG: print ('    {KEY:<30} : {VAL}'.format(KEY=key, VAL=val))

    except (configparser.InterpolationMissingOptionError) as why:
        print("\n"*2)
        print("="*60)
        print("ERRORE nella validazione del file")
        print("-"*60)
        print(str(why))
        print("="*60)
        sys.exit(-2)

    if sectionName:
        return the_dict[sectionName]
    else:
        return the_dict


############################################################
#
############################################################
def iniConfigAsDict_OneLEVEL(INIConfig, sectionName=None, returnOrderedDict=False, raw=False):
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """

    the_dict = collections.OrderedDict({}) if returnOrderedDict else {}
    fDEBUG = False
    try:
        for section in INIConfig.sections():
            # the_dict[section] = myDict
            the_dict[section] = collections.OrderedDict({}) if returnOrderedDict else {}
            if fDEBUG: print ()
            if fDEBUG: print ('[{SECT}]'.format(SECT=section))
            for key, val in INIConfig.items(section, raw=raw):
                the_dict[section][key] = val
                if fDEBUG: print ('    {KEY:<30} : {VAL}'.format(KEY=key, VAL=val))

    except (configparser.InterpolationMissingOptionError) as why:
        print("\n"*2)
        print("="*60)
        print("ERRORE nella validazione del file")
        print("-"*60)
        print(str(why))
        print("="*60)
        sys.exit(-2)

    if sectionName:
        return the_dict[sectionName]
    else:
        return the_dict




############################################################
#
############################################################
def printINIconfigparser(INI_raw):
    for section in INI_raw.sections():
        print ()
        print ('[{SECTION}]'.format(SECTION=section))
        for key, val in INI_raw.items(section):
            TAB = 37*' '
            print ('    {KEY:<30} : {VAL}'.format(KEY=key, VAL=val.replace ('\n', '\n' + TAB)))



############################################################
#
############################################################
def printINIdict(INI_dict):
    for sectName in INI_dict.keys():
        print ()
        print ('[{SECTION}]'.format(SECTION=sectName))
        # for key, val in INI_dict[sectName].items(sectName):
        TAB = 37*' '
        for key, val in INI_dict[sectName].items():
            print ('    {KEY:<30} : {VAL}'.format(KEY=key, VAL=val.replace ('\n', '\n' + TAB)))


if __name__ == '__main__':
    print ('sono qui')
    iniFile = 'ReadIniFile.test.ini'
    with open(iniFile, "r") as f:
        data = f.read()
    print (data)

    Raw, Dict = readIniFile(iniFile, RAW=True, returnOrderedDict=True, exitOnError=True, STRICT=False)
    # printINIconfigparser (Raw)
    printINIdict (Dict)
    sys.exit()
