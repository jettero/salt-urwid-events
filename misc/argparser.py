
import argparse, sys

class ArgumentParser(argparse.ArgumentParser):

    def __init__(self, prog=sys.argv[0].split('/')[-1].replace('.py',''), **kwargs):
        super(ArgumentParser,self).__init__(prog=prog, **kwargs)

        self.add_argument('-r', '--replay-file', type=str,
            help='replay this logfile (print-events format)')

        self.add_argument('-j', '--replay-job-cache', action='store_true',
            help='attempt to reconstruct event-like data from the job cache')

        self.add_argument('-o', '--replay-only', action='store_true',
            help="don't read events from salt, just use replay files")
