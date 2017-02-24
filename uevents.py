#!/usr/bin/env python2

from saltobj import ArgumentParser
import urwidobj
import misc

misc.be_root_you_fool()

if __name__=="__main__":
    parser = ArgumentParser( prog='uevents' )
    args = parser.parse_args()

    app = urwidobj.EventApplication(args)
    app.run()
    print "\nevents collected: {0}".format( app.event_no )
