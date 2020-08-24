
from threading import Thread
import pandas as pd
from datetime import datetime
from time import sleep
from math import ceil

from machine import machine

#_____________________________________________________________________________
class webioc(Thread):
    #_____________________________________________________________________________
    def __init__(self):
        Thread.__init__(self)

        #self.htmlnam = "webioc.html"
        self.htmlnam = "/ceph/WWW/SlowControls2018/webioc.html"

        #open the configuration
        csv = pd.read_csv("config.csv")

        #all slow controls machines
        self.machines = {}
        self.machine_names = []

        #load the machines from the configuration
        for i in csv.iterrows():
            host = i[1]["host"].strip()

            if host not in self.machines:
                self.machines[host] = machine(i[1])
                self.machine_names.append(host)

            self.machines[host].add_ioc(i[1])

        #alphabetical order for machine and ioc names
        self.machine_names.sort()
        for i in self.machines.itervalues():
            i.sort_iocs()

        #html header
        self.hhead = ['<HTML><HEAD><link rel="stylesheet" type="text/css" href="stylesx.css">',
                      '<META HTTP-EQUIV="Refresh" Content="5" url="./"> </HEAD>',
                      '<title>Slow Controls IOC Monitor</title> ', '<BODY BGCOLOR=cornsilk>',
                      '  <br><table style="padding-top: 20px;">',
                      #'<caption style="font-size:160%;">Slow Controls IOC Monitor, development and testing (Jarda)</caption>'
                      '<caption style="font-size:160%;">Slow Controls IOC Monitor</caption>'
                      ]

        #html footer
        self.hfoot = ['  </table><br>',
                      'OK = IOC is present on the host. Alarm states (red): NOT_RUNNING, MULTIPLE_INSTANCES, DISCONNECTED, UNDEFINED',
                      '<br></BODY></HTML> '
        ]

        #table header
        self.tab_head = [
            '    <th class="h0">IOC</th>',
            '    <th class="h0">Status</th>',
            '    <th class="h1">Description</th>'
            ]

    #_____________________________________________________________________________
    def make_html(self):

        #lines content for the table
        tab_lines = []
        for i in self.machine_names:
            self.machines[i].make_html(tab_lines)

        #columns and rows for the table
        ncol = 2
        nrow = int( ceil( float(len(tab_lines))/ncol ) )

        #column content
        tab_col = [] #irow, icol
        for irow in xrange(nrow):
            tab_col.append([])
            for icol in xrange(ncol):
                tab_col[irow].append("<td colspan='3'></td>")

        #split input lines to column content
        for icol in xrange(ncol):
            for irow in xrange(nrow):
                if len(tab_lines) <= 0: break
                tab_col[irow][icol] = tab_lines.pop(0)

        #format the html table
        tab = []
        #table header
        tab.append('<tr>')
        for icol in xrange(ncol):
            for i in self.tab_head:
                tab.append(i)
            if icol < ncol-1:
               tab.append("<td> </td>")
        tab.append('</tr>')
        #table rows
        for irow in xrange(nrow):
            tab.append('<tr>')
            #line in row over all columns
            for icol in xrange(ncol):
                #input content
                tab.append( tab_col[irow][icol] )
                #print tab_col[irow][icol]
                #spacing between the columns
                if icol < ncol-1:
                    tab.append("<td> </td>")

            tab.append('</tr>')

        hf = open(self.htmlnam, "w")

        #write html header
        for linhead in self.hhead:
            hf.write(linhead+"\n")

        for i in tab:
            hf.write(i+"\n")

        #put table footer
        for linfoot in self.hfoot:
            hf.write(linfoot+"\n")
        #put last update time, remove ms after decimal point
        hf.write("<br>\n")
        hf.write("Last updated: " + str(datetime.now()).split(".")[0] + "\n")
        #close the html file
        hf.close()

    #_____________________________________________________________________________
    def run(self):

        #execute periodically the make_html function
        while True:
            self.make_html()
            sleep(15)

