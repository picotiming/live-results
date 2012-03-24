@echo off

:: change the following line to the OrServer event name (directory name)
set event=BBN11DEZ09
set target=D:\picOR\ORclient\CLevent\%event%\CLofflineCLI\

:: let this as it is
set url=https://pico-timing.googlecode.com/svn/trunk/
set repo=pico-timing
set file=DBOResDataSingle-1.ore
set interval=20

set usr=picotiming@gmail.com
set pw=jJ8nJ4SE3cY2

set remotePath=%url%

cd ..
svn checkout %remotePath% %repo% --username %usr% --password %pw%
cd %repo%

:Start
svn update --username %usr% --password %pw%
copy /Y %file% %target%%file%

ping -n %interval% 127.0.0.1>nul
GOTO :Start