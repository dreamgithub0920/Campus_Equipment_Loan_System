@echo off
setlocal EnableExtensions DisableDelayedExpansion
title Campus Equipment Loan System

rem Start in this file's folder, including paths with spaces and UNC shares.
pushd "%~dp0" >nul 2>&1
if errorlevel 1 goto folder_error
if not exist "gui.py" goto files_missing

rem Prefer the Windows Python launcher, then Python commands on PATH.
where py >nul 2>&1
if errorlevel 1 goto try_python
py -3 -c "import sys; assert sys.version_info >= (3, 10); import tkinter, sqlite3" >nul 2>&1
if errorlevel 1 goto try_python
py -3 gui.py %*
set "gui_exit=%errorlevel%"
goto finished

:try_python
where python >nul 2>&1
if errorlevel 1 goto try_python3
python -c "import sys; assert sys.version_info >= (3, 10); import tkinter, sqlite3" >nul 2>&1
if errorlevel 1 goto try_python3
python gui.py %*
set "gui_exit=%errorlevel%"
goto finished

:try_python3
where python3 >nul 2>&1
if errorlevel 1 goto python_missing
python3 -c "import sys; assert sys.version_info >= (3, 10); import tkinter, sqlite3" >nul 2>&1
if errorlevel 1 goto python_missing
python3 gui.py %*
set "gui_exit=%errorlevel%"
goto finished

:python_missing
echo Python 3.10 or newer with Tkinter and SQLite is required.
echo Install Python from https://www.python.org/downloads/windows/
echo Include Tcl/Tk support and make the py or python command available.
echo Then double-click Start_GUI.bat again.
echo You can check Tkinter with: py -3 -m tkinter
set "gui_exit=1"
goto finished

:files_missing
echo gui.py was not found. Extract the entire ZIP before starting the app.
echo Keep Start_GUI.bat beside gui.py and the other source files.
set "gui_exit=1"
goto finished

:folder_error
echo Cannot open the program folder. Extract the ZIP to a local writable folder.
pause
exit /b 1

:finished
popd
if "%gui_exit%"=="0" exit /b 0
echo.
echo The app did not start or exited with an error. Review the message above.
pause
exit /b %gui_exit%
