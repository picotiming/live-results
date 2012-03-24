@echo off

:: change the following line to the OrServer event name (directory name)
set event=BBN11DEZ09
set target=D:\picOR\ORclient\CLevent\%event%\CLofflineCLI\

:: let this as it is
set file=DBOResDataSingle-1.ore
set interval=20

set usr=picotiming
set project=live-results
set url=https://github.com/%usr%/%project%/

set remotePath=%url%

:Start
svn update
copy /Y %file% %target%%file%

ping -n %interval% 127.0.0.1>nul
GOTO :Start