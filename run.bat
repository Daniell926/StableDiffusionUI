@echo off

call setup.bat

set PYTHONPATH=%cd%\src
cd src
python UI.py
pause