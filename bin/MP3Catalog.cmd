@ECHO OFF

    @SET SCRIPT_DRIVE=%~d0
    @SET SCRIPT_PATH=%~dp0
    @SET SCRIPT_NAME=%~n0
    @SET SOURCE_DIR=%SCRIPT_PATH%..\SOURCE

    rem 'without rowid' richiede almeno la versione sqlite3  3.8.2 or later. Presente a partire da python 3.4
    @CALL %Ln.FreeDir%\PythonPATH.cmd 3.3
    @SETLOCAL

    if EXIST "%SOURCE_DIR%\__main__.py" (
        SET mainProgram="%SOURCE_DIR%\__main__.py"
    ) else (
        SET mainProgram="%SOURCE_DIR%\%SCRIPT_NAME%.zip"
    )

    IF /I "%1"=="DEBUG" (
        @SET PARAMS=%2 %3 %4 %4 %6 %7 %8 %9
        @SET DEBUG=-c "import winpdb;winpdb.main()" && SET START=start

    ) ELSE (
        @SET PARAMS=%*
    )

    @GOTO :PROCESS

:PROCESS
    @echo %PARAMS%
    %START% python.exe %DEBUG% %mainProgram% %PARAMS%




:: @pause
    rem start python -c "import winpdb;winpdb.main()" %mainProgram% %PARAMS%