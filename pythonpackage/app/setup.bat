@ECHO OFF
REM setup.bat template

REM Set the PYTHONDIR to path for python.exe (must end in \)
SET PYTHONDIR=C:\Users\maarten\AppData\Local\Programs\Python\Python39\
IF NOT EXIST %PYTHONDIR%python.exe (
  ECHO No python.exe in %PYTHONDIR%
  ECHO Patch line 5 in %~f0
  EXIT /b
)

ECHO Creating virtual Python environment
%PYTHONDIR%python.exe -m venv env
CALL env\Scripts\activate.bat
ECHO Upgrading pip
python -m pip install -q --upgrade pip setuptools wheel
ECHO Adding packages
IF EXIST requirements.txt (
   pip install -q -r requirements.txt
)

ECHO.Setup done, now use run

