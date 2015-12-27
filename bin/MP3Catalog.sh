#!/bin/bash
#

    thisDir="$(dirname  "$(test -L "$0" && readlink "$0" || echo "$0")")"     # risolve anche eventuali LINK presenti sullo script
    thisDir=$(cd $(dirname "$thisDir"); pwd -P)/$(basename "$thisDir")        # GET AbsolutePath
    baseDir=${thisDir%/.*}                                                      # Remove /. finale (se esiste)
    parentDir=${baseDir%/bin}                                               # Remove /bin finale (se esiste)
    parentDir="$(dirname $baseDir)"
    sourceDir="${parentDir}/SOURCE"

    if [ -d "$sourceDir"  ]; then
        mainProgram="$sourceDir/__main__.py"
    else
        mainProgram="$baseDir/projectTemplate.zip"
    fi

    # source /opt/rh/python33/enable
    # python3 $mainProgram $*
    python $mainProgram $*

    exit 0
