
from ioc import ioc

#_____________________________________________________________________________
class machine():
    #_____________________________________________________________________________
    def __init__(self, config):

        self.host_name = config["host"].strip()

        #iocs for the machine
        self.iocs = {}
        self.ioc_names = []

    #_____________________________________________________________________________
    def make_html(self, tab_lines):

        #html content for the machine
        tab = '<td class="d0"; style="background-color: #00dfff" colspan="3">Host: '+self.host_name+'</td>'

        tab_lines.append(tab)

        for i in self.ioc_names:
            self.iocs[i].make_html(tab_lines)

    #_____________________________________________________________________________
    def add_ioc(self, config):

        nam = config["ioc"].strip()

        self.iocs[nam] = ioc(config)
        self.ioc_names.append(nam)

    #_____________________________________________________________________________
    def sort_iocs(self):

        #sort the iocs alphabetically
        self.ioc_names.sort()

        

