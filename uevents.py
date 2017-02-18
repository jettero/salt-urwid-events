#!/usr/bin/env python2

import urwidobj

misc.be_root_you_fool()

if __name__=="__main__":
    app = urwidobj.EventApplication()
    app.run()
    print "\nevents collected: {0}".format( app.event_no )
