@echo off

:: change the following line to the OrServer event name (directory name)
set event=BBN11DEZ09
set origin=D:\picOR\ORserver\SEevent\%event%\SEoutput\

:: let this as it is
set file=DBOResDataSingle-1.ore
set interval=20

set usr=picotiming
set project=live-results
set url=https://github.com/%usr%/%project%/

set remotePath=%url%

copy /Y "%origin%%file%" "%file%"
svn add %file%

:Start
copy /Y "%origin%%file%" "%file%"
svn commit -m "UpdateRanking@%Time%" %file%

ping -n %interval% 127.0.0.1>nul
GOTO :Start