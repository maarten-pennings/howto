@ECHO OFF

SET LOCATION=C:\Programs\Python\

%LOCATION%python.exe -m venv env
CALL env\Scripts\activate.bat
env\Scripts\python -m pip install --upgrade pip setuptools wheel
IF EXIST requirements.txt (
   pip install -r requirements.txt
)
