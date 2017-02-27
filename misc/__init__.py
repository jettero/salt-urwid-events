import os

from argparser import ArgumentParser

def be_root_you_fool():
    import os
    if os.getuid() > 0:
        import sys
        a = [ x for x in sys.argv ]
        a.insert(0, 'sudo')
        os.execlp(a[0], *a)
        print "error??"
        exit(1)

def setup_file_logger(args, tag='component-name-here',
    format="%(asctime)s %(levelname)s %(name)s[%(process)d]: %(message)s"):
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

        class LogWriter(object):
            def __init__(self,fn):
                self.fn = fn
            def write(self,message):
                self.fn( message.rstrip() )
            def flush(self):
                pass
        sys.stderr = LogWriter(log.warning)

        cuid = int(os.environ.get('SUDO_UID', '0'))
        cgid = int(os.environ.get('SUDO_GID', '0'))
        if cuid:
            os.chown( logging.logfile, cuid,cgid )

    return log
