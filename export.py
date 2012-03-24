#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
Created on 26.09.2011

@author: dola
'''

import os
import json
from datetime import time
from time import strftime
import codecs

class Export:
    def __init__(self, data, basePath=""):
        '''
        Constructor
        '''
        self.data = data
        self.basePath = basePath

class HtmlExport(Export):
    '''
    classdocs
    '''
    
    template = {}
    
    def __init__(self, data, basePath="/Library/WebServer/Documents/", eventTitle="Ranglisten"):
        Export.__init__(self, data, basePath)
        self.eventTitle = eventTitle
    
    def _loadTemplate(self, path):
        """loads a template file and returns it as an array of lines"""
        f = open(path, "r")
        return f.readlines()
        f.close()

    def exportOverview(self, path, links, title="", caption="", templatePath="overview.html", linkformat = '<li class="arrow"><a href="{0[link]}">{0[caption]}</a> <small class="counter">{0[info]}</small></li>', otherlink={"url": 'index.html', "caption": 'Ranglisten'}):
        """exports an overview with the possiblity to choose between all categories to see their rankings/startlists"""
        template = self._loadTemplate(templatePath)
        
        f = open(os.path.join(self.basePath, path), "w")
        linkdata = ""
        for l in sorted(links):
            linkdata = linkdata + linkformat.format(l)
        
        for line in template:
            f.write(line.format(datablock=linkdata, title=title, description=caption, otherlink=otherlink))

    def _runtime(self, seconds, entry):
        """generates and returns a string containing the formated runtime out of the runtime in seconds"""
        if entry['respersidx'] == "5":
            seconds = int(seconds)
            hours = (seconds / 3600) % 24
            minutes = (seconds % 3600) / 60
            seconds = seconds % 60
            if hours > 0:
                return time(hours, minutes, seconds).strftime("%H:%M:%S")
            else:
                return time(hours, minutes, seconds).strftime("%M:%S")
        else:
            codes = {   0: 'dns',
                        1: '',
                        2: 'npl',
                        3: 'disq',
                        4: 'ncomp'}
            try:
                return codes[entry["respersidx"]]
            except LookupError:
                return ""
        return ""

    def exportData(self, folder, lineformat, naming = "{category}.html", templatePath="template.html", title="", caption="", tableprefix="", tablesuffix="", backlink={"url": "..", "caption": "Zurück"}, id="{category}"):
        """exports all data in a format specified by a template file with python string format placeholders"""
        template = self._loadTemplate(templatePath)
        links = []
        for cat in self.data:
            firstentry = cat[0]
            filename = naming.format(firstentry, category=cat)
            path = os.path.join(folder, filename)
            
            f = open(os.path.join(self.basePath, path), "w")
            
            datablock = tableprefix
            finished = 0
            for entry in self.data[cat]:
                if entry["rank"] == "0":
                    entry["rank"] = ""
                runtime = self._runtime(entry["runtime"], entry)
                datablock = datablock + lineformat.format(entry, runtime=runtime)
                finished = finished + int(entry["finished"]) + (1 - int(entry["started"]))
            datablock = datablock + tablesuffix
            
            link = {"link": folder + filename, "caption": cat, "info": (len(self.data[cat]), finished)}
            links.append(link)
            
            for line in template:
                f.write(line.format(datablock=datablock, title=title.format(firstentry, category=cat, link=link), description=caption.format(firstentry, category=cat, link=link), backlink=backlink, category=cat, id=id.format(category=cat)))
            
            f.close()
            
        return links

    def exportStartlist(self, folder=""):
        """exports startlists to a folder for every category in self.data using the exportData() method"""
        #tableprefix = '<thead><tr><th class="rank">Nr.</th><th class="name">Name</th><th class="yob">JG</th><th class="club">Club</th><th class="time">Startzeit</th></tr></thead><tbody>'
        #tablesuffix = '</tbody>'
        #lineformat = '<tr><td class="rank">{00[stnr]}</td><td class="name">{00[first]} {00[name]}</td><td class="yob">{00[yob]}</td><td class="club">{00[club]}</td><td class="time">{00[preruntime]}</td></tr>'
        
        tableprefix = '<ul><li><span class="rank">Nr.</span><span class="name">Name</span><span class="yob">JG</span><span class="club">Club</span><span class="time">Startzeit</span></li>'
        lineformat = '<li><span class="rank">{00[stnr]}</span><span class="name">{00[first]} {00[name]}</span><span class="yob">{00[yob]}</span><span class="club">{00[club]}</span><span class="time">{00[preruntime]}</span></li>'
        tablesuffix = '</ul>'
        
        templatePath = "template.html"
        title = "{category}"
        otherlink = {"url": 'index.html', "caption": 'Ranglisten'}
        caption = "Startliste der {link[info][0]} Läufer der Kategorie {category}"
        infoformat = "{0[0]} Teilnehmer"
        backlink = {"url": "#", "caption": "zurück"}
        
        links = self.exportData(folder, lineformat, "s{category}.html", templatePath, title, caption, tableprefix, tablesuffix, backlink, "s{category}")
        for i in xrange(len(links)):
            links[i]["info"] = infoformat.format(links[i]["info"])
        self.exportOverview(os.path.join(folder, "startlists.html"), links, "Startlisten", "Wähle eine Kategorie um zu deren Startliste zu kommen.", otherlink=otherlink)

    def exportRanking(self, folder=""):
        """exports all rankings from self.data to a folder using the exportData() method"""
        tableprefix = '<thead><tr><th class="rank"><span class="long">Rang</span><span class="short">R</span></th><th class="name">Name</th><th class="yob">JG</th><th class="town">Ort</th><th class="club">Club</th><th class="time"><span class="long">Laufzeit</span><span class="short">Zeit</span></th></tr></thead>'
        tablesuffix = '</tbody>'
        lineformat = '<tr><td class="rank">{00[rank]}</td><td class="name">{00[first]} {00[name]}</td><td class="yob">{00[yob]}</td><td class="town">{00[town]}</td><td class="club">{00[club]}</td><td class="time">{runtime}</td></tr>'        
        templatePath = "template.html"
        title = "{category}"
        otherlink = {"url": 'startlists.html', "caption": 'Startlisten'}
        caption = "provisonal results (" +strftime("%H:%M")+ ") after {link[info][1]} of {link[info][0]} competitors."
        infoformat = "{0[1]}/{0[0]}"
        backlink = {"url": "#", "caption": "back"}
        
        links = self.exportData(folder, lineformat, "r{category}.html", templatePath, title, caption, tableprefix, tablesuffix, backlink, "r{category}")
        for i in xrange(len(links)):
            links[i]["info"] = infoformat.format(links[i]["info"])
        self.exportOverview(os.path.join(folder, "index.html"), links, self.eventTitle, "choose category", otherlink=otherlink)

    def exportWinnerList(self, folder=""):
        """ exports top 5 of every category """
        order = ["DAL", "HAL", "HAM", "DAK", "HAK",
                 "DB", "HB", "D35", "H35",
                 "D40", "H40", "D35", "H35",
                 "D50", "H50", "D55", "H55",
                 "D60", "H60", "D65", "H65",
                 "D70", "H70", "H75", "H80",
                 
                 "D10", "H10", "D12", "H12", "D14", "H14",
                 "D16", "H16", "D18", "H18",
                 "D20", "H20",
                 "DE", "HE"]
        """
            9 Gruppen
            DAL/HAL, HAM , DAK/HAK
            DB/HB, D35/H35
            40er, 45er
            50er, 55er
            60er, 65er
            D70/H70, H75, H80
            
            Medialliekategorien:
            D/H 10, 12, 14
            D/H 16, 18
            D20, H20
            DE, HE
            Eventuell WRE H/D
            """
        
        tableprefix = '<thead><tr><th class="rank"><span class="long">Rang</span><span class="short">R</span></th><th class="name">Name</th><th class="yob">JG</th><th class="club">Club</th><th class="time"><span class="long">Laufzeit</span><span class="short">Zeit</span></th></tr></thead>'
        tablesuffix = '</tbody>'
        lineformat = '<tr><td class="rank">{00[rank]}</td><td class="name">{00[first]} {00[name]}</td><td class="yob">{00[yob]}</td><td class="club">{00[club]}</td><td class="time">{runtime}</td></tr>'        
        templatePath = "template.html"
        template = self._loadTemplate(templatePath)
        title = "{category}"
        cat = "winnerList"
        caption = "vorl&auml;ufige Gewinnerliste von " +strftime("%H:%M")

        datablock = tableprefix
        
        for c in order:
            if c in self.data:
                datablock += '<tr><td colspan="5"><h2 style="color: black;"><b>{0}</b></h2></td></tr>\n'.format(c)
                anzahl = 3
                if c == "HE" or c=="DE":
                    anzahl = 5
                for i in xrange(anzahl):
                    entry = self.data[c][i]
                    if entry["rank"] == "0":
                        entry["rank"] = ""
                    datablock += lineformat.format(self.data[c][i], runtime=self._runtime(entry["runtime"], entry))

        datablock += tablesuffix
        
        filename = "winnerList.html"
        path = os.path.join(folder, filename)
        f = open(os.path.join(self.basePath, path), "w")

        id="{category}"
        backlink = {"url": "#", "caption": "zur&uuml;ck"}
        for line in template:
            f.write(line.format(datablock=datablock, title=title.format(category=cat), description=caption.format(category=cat), backlink=backlink, category=cat, id=id.format(category=cat)))
        
        f.close()
        print("exported winnerList")

    
class JSONExport(Export):
    """exports data to a JSON file"""
    def __init__(self, data, basePath=""):
        Export.__init__(self, data, basePath)
    
    def export(self, folder):
        """exports self.data to a location specified with the folder argument"""
        f = open(folder, "w")
        f.write(json.dumps(self.data, sort_keys=True, indent=4))
        f.close()
