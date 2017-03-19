import os

from argparser import ArgumentParser
from xlateansi import xlate_ansi, format_code
from list_ptr  import ListWithPtr
from matcher   import Matcher

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s[%(process)d]: %(message)s"
LOG_FORMAT = "%(name)s.%(process)d: %(message)s"

def be_root_you_fool():
    import os
    if os.getuid() > 0:
        import sys
        a = [ x for x in sys.argv ]
        a.insert(0, 'sudo')
        os.execlp(a[0], *a)
        print "error??"
        exit(1)

def setup_file_logger(args, tag='component-name-here', format=LOG_FORMAT):
    import logging, sys

    # translate loglevel string to logging.<level>
    args.loglevel = getattr(logging, args.loglevel.upper())

    # support no/off/false
    if not args.logfile or args.logfile.lower() in ('no', 'off', 'false'):
        logging.root.addHandler( logging.NullHandler() )
        log = logging.getLogger(tag)

    else:
        fh = logging.FileHandler(args.logfile)
        fh.setFormatter(logging.Formatter(format))

        logging.root.addHandler(fh)
        logging.root.setLevel(logging.DEBUG)
        logging.root.debug("logging configured")
        log = logging.getLogger(tag)

        class MyLogWriter(object):
            def __init__(self,fn,old_err):
                self.fn = fn
                self.old_err = old_err
            def write(self,message):
                self.fn( message.rstrip() )
                self.old_err.write( message )
            def flush(self):
                self.old_err.flush()

        sys.stderr = MyLogWriter(log.warning, sys.stderr)

        cuid = int(os.environ.get('SUDO_UID', '0'))
        cgid = int(os.environ.get('SUDO_GID', '0'))
        if cuid:
            if not os.path.exists(args.logfile):
                open(args.logfile, 'a').close()
            os.chown(args.logfile, cuid,cgid)

    return log
