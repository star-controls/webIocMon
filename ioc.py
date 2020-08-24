
from epics import PV, caget

#_____________________________________________________________________________
class ioc():
    #_____________________________________________________________________________
    def __init__(self, config):

        host = config["host"].strip()
        self.nam = config["ioc"].strip()
        pvnam = "iocmon:"+host+":"+self.nam

        #print pvnam, self.description

        #color map
        self.col = {"ok":"00ff00", "alarm":"ff0000", "nocon":"ffffff"}

        self.pv_stat = PV(pvnam+":status", connection_callback=self.on_stat_conn)
        self.status = self.pv_stat.get(as_string=True)
        self.severity = self.pv_stat.severity
        if self.status == None:
            self.status = "   "
            self.severity = -1
            self.description = "   "
            print "Error: no connection to", pvnam+":status"
            return

        self.pv_stat.add_callback(self.on_stat_update)

        self.description = caget(pvnam+":description")

    #_____________________________________________________________________________
    def make_html(self, tab_lines):

        #html content for the ioc
        bgcol = self.col["alarm"]
        if self.severity == 0:
            bgcol = self.col["ok"]
        if self.severity == -1:
            bgcol = self.col["nocon"]

        tab = '<td style="background-color: #'+bgcol+'">'+self.nam+'</td>'
        tab += '<td style="background-color: #'+bgcol+'">'+self.status+'</td>'
        tab += '<td>'+self.description+'</td>'

        tab_lines.append(tab)


    #_____________________________________________________________________________
    def on_stat_update(self, char_value, severity, **kws):

        self.status = char_value
        self.severity = severity

        #print severity, char_value

    #_____________________________________________________________________________
    def on_stat_conn(self, conn, **kws):

        if conn == True: return

        self.status = "   "
        self.severity = -1







