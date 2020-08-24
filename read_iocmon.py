#!/usr/bin/python

from epics import PV
from time import sleep

def on_update(pvname, char_value, severity, **kws):
    #print pvname, value, char_value, severity
    print pvname, char_value, severity

#nam = "iocmon:softioc4:gasread"
nam = "iocmon:softioc4:mc"

#stat = PV(nam+":status", callback=on_update)
stat = PV(nam+":status")
desc = PV(nam+":description")

#sleep(2)

print stat.get(as_string=True)
print stat.severity

stat.add_callback(on_update)

#print stat.get(as_string=True)
#print stat.info
#print desc.get(as_string=True)
#print stat.char_value

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        print
        break

