FILES IN THIS REPOSITORY
========================

DBOResDataSingle-1.ore
----------------------
OrWare file with all results in it

download.bat
------------
batch script that downloads the result file in some interval and copies it to the directory of an offline ORclient

upload.bat
----------
batch script to first retrieve the newest result file from the servers SEevent directory and then uploads it in a certain interval

server.bat
----------
batch script to download the newest result file and then call import.py to generate a new webpage out of the results

import.py
---------
imports the newest result file and calls export.py to export the result as webpage to the local apache server

export.py
---------
exports the rankings to the local apache server using the templates for overview and template. (see below)

overview.html
-------------
template for the overview of the result webpage.

template.html
-------------
template for each result page.

readme.txt
----------
this file.


CONFIGURATION
=============

possible to configurate the following:

event name (folder name)
------------------------
in each of the following files:
download.bat
upload.bat

change the line like this:
set event=LOM2011

event name (display name)
------------------------
in each of the following files:
server.bat

change the line like this:
set eventTitle="Bern by Night 3, R&uuml;fenacht"

Note that all special characters like umlauts (הצü) have to be written as html entities to ensure correct encoding. (see following table)
 
 char   | entity
--------+---------
   ü    |  &uuml;
   ה    |  &auml;
   צ    |  &ouml;
   Ü    |  &Uuml;
   ִ    |  &Auml;
   ײ    |  &Ouml;
   &    |  &amp;


path of offline client
----------------------
to be set in download.bat

default:
set target=D:\picOR\ORclient\CLevent\%event%\CLofflineCLI\


path of webserver
-----------------
the htdocs directory has to be specified in server.bat

default:
set serverPath=C:\xampp\htdocs


path of SEoutput folder
-----------------------
to be set in upload.bat (will most likely be something in the network)

default:
set origin=D:\picOR\ORserver\SEevent\%event%\SEoutput\


WEB SERVER
==========
note that the webserver has to include the stylesheet in it's htdocs directory.
ask for them by sending an email to dola@gmx.ch