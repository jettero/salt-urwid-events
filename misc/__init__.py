
import logging, sys

def setup_file_logger(tag='component-name-here', file='urwid-events.log', format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
    fh = logging.FileHandler(file)
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
    return log
