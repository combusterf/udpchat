@echo off
cd %~dp0

cd ..
cd bin
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\FlagshipMain.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%CD%\FlagshipMain.py" >> %SCRIPT%
echo oLink.WorkingDirectory = "%CD%\" >> %SCRIPT%
echo oLink.IconLocation = "%CD%\iconfile.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%