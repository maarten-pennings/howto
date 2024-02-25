@ECHO OFF
REM Create a link in the Arduino library directory, to a library in a repo

REM Create
mklink /D C:\Users\maarten\Documents\Arduino\libraries\mylib  C:\repos\HowTo\LinkedLibrary\mylib

REM Show
dir C:\Users\maarten\Documents\Arduino\libraries\mylib*
