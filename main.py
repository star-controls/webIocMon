#!/usr/bin/python

#from time import sleep
import code

from webioc import webioc

#webpage for IOC monitor
wi = webioc()

#start updating loop
wi.daemon = True
wi.start()

#open the shell
vars = globals()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()

