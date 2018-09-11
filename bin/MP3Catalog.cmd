@echo OFF

    @set "SCRIPT_DRIVE=%~d0"
    @set "SCRIPT_PATH=%~dp0"
    @set "SCRIPT_NAME=%~n0"
    @set "SOURCE_DIR=%SCRIPT_PATH%..\SOURCE"

    rem 'without rowid' richiede almeno la versione sqlite3  3.8.2 or later. Presente a partire da python 3.4
    :: @call %Ln.FreeDir%\PythonPATH.cmd 344
    @setlocal
::
    cd /D %SCRIPT_PATH%
    set "mainProgram=%SOURCE_DIR%\%SCRIPT_NAME%.zip"
    set "mainProgram=..\Source\__main__.py"

    @set "extPARAMS=%*"

    :: @goto :EXTRACT
    @goto :COPYSONGS


:: :EXTRACT
    :: set "params=extract"
    :: %START% python.exe %mainProgram% %params% %extPARAMS%
    :: python.exe %mainProgram% %params% %extPARAMS%
    :: goto :EOF

:COPYSONGS
    set "params=sqlite copySongs --source-dir=d:\LnFolders\MyData\MP3 --dest-dir=E:\tmp\MP3"
    set "params=sqlite copySongs --source-dir=e:\LnED\Toshiba1T\Filu\MyData\MP3 --dest-dir=E:\tmp\MP3"
    %Ln.PythonExe% %mainProgram% %params% %extPARAMS%
    goto :EOF


:EOF
:: @pause
    rem start python -c "import winpdb;winpdb.main()" %mainProgram% %PARAMS%