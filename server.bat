@echo off

:: set this to the path of the htdocs dir of your apache installation
set serverPath=C:\xampp\htdocs
set eventTitle="Bern by Night 3, R&uuml;fenacht"
:: Note: escape all umlauts with html entities

:: let this as it is
set interval=20

set usr=picotiming
set project=live-results
set url=https://github.com/%usr%/%project%/

set remotePath=%url%

:Start
svn update
python import.py %serverPath% %eventTitle%

ping -n %interval% 127.0.0.1>nul
GOTO :Start