#!/usr/bin/env python2

import urwidobj
import misc

if __name__=="__main__":
    parser = misc.ArgumentParser( prog='uevents' )

    parser.add_argument('--logfile', type=str, default='uevents.log',
        help="write a log file for the session, set to 'no'/'off'/'' to disable [default: %(default)s]")

    parser.add_argument('--loglevel', type=str, default='debug', 
        choices=['debug', 'info', 'warning', 'error'],
        help="write a log file for the session, set to 'no'/'off'/'' to disable [default: %(default)s]")

    parser.add_argument('--no-chown-sudo-user', action='store_true',
        help="by default the output logfile is owner is the user invoking sudo")

    args = parser.parse_args()

    misc.be_root_you_fool()

    app = urwidobj.EventApplication(args)
    app.run()
    print "\nevents collected: {0}".format( app.event_no )
