#!/usr/bin/env python2

import urwidobj
import misc

if __name__=="__main__":
    misc.be_root_you_fool()

    parser = misc.ArgumentParser( prog='uevents' )

    parser.add_argument('-J', '--max-jobs',   type=int, default= 50, help="the max number of tracked jobs in the jobs list")
    parser.add_argument('-E', '--max-events', type=int, default=100, help="the max number of tracked events in the event list")

    parser.add_argument('--id-format', type=misc.Matcher, nargs='*',
        help="use a regex to reformat ids if yours are long or troublesome. "
             "option can be repeated, regex must use capture groups"
             "(e.g., (.+).long.domainname.here)")

    parser.add_argument('--logfile', type=str, default='uevents.log',
        help="write a log file for the session, set to 'no'/'off'/'' to disable [default: %(default)s]")

    parser.add_argument('--loglevel', type=str, default='debug', 
        choices=['debug', 'info', 'warning', 'error'],
        help="write a log file for the session, set to 'no'/'off'/'' to disable [default: %(default)s]")

    parser.add_argument('--no-chown-sudo-user', action='store_true',
        help="by default the output logfile is owner is the user invoking sudo")

    args = parser.parse_args()

    if args.id_format:
        import saltobj.event
        saltobj.event.reformat_minion_ids(args.id_format)

    app = urwidobj.EventApplication(args)
    app.run()
    print "\nevents collected: {0}".format( app.event_no )
