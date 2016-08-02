#!/bin/bash
ACTION=$1
EXECUTE=
[[ "$ACTION" != "--GO" ]] && EXECUTE='echo'


       thisDir="$(dirname  "$(test -L "$0" && readlink "$0" || echo "$0")")"     # risolve anche eventuali LINK presenti sullo script
       thisDir=$(cd $(dirname "$thisDir"); pwd -P)/$(basename "$thisDir")        # GET AbsolutePath
        prjDir=${thisDir%/.*}                                                      # Remove /. finale (se esiste)
       rootDir=$(dirname "$prjDir")
      LnLibDir=$rootDir/LnPythonLib
LnPythonLibDir=$rootDir/LnPythonLib
      LnLibDir=$prjDir/SOURCE/LnLib

echo $prjDir
echo $rootDir
echo $LnPythonLibDir

cp



exit
outDIR="$prjDir/bin"
LnPythonLibDir=/home/pi/gitREPO
ProjectDir=${prjDir}

# Creazione della LnPythonLib_YYYYMMDD.zip nella directory ${outDIR}
cd ${LnPythonLibDir}
echo
echo "I am in directory:.. ${PWD}"
    zipFileName="LnPythonLib_$(date +"%Y%m%d").zip"
    $EXECUTE zip -r --exclude='*.git*' ${outDIR}/${zipFileName} ./LnPythonLib/*
echo

# Creazione dello zip di DDNS nella directory ${outDIR}
cd ${ProjectDir}
echo
echo "I am in directory:.. ${PWD}"
    zipFileName="DDNS_$(date +"%Y%m%d").zip"
    $EXECUTE zip -r --exclude='*.git*' --exclude='bin*' --exclude='conf*' ${outDIR}/${zipFileName} *
echo
