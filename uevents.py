#!/usr/bin/env python2

import argparse
import urwidobj
import misc

misc.be_root_you_fool()

if __name__=="__main__":
    parser = argparse.ArgumentParser("uevents: [options]")

    app = urwidobj.EventApplication()
    app.run()
    print "\nevents collected: {0}".format( app.event_no )
