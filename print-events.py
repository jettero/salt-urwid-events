#!/usr/bin/env python2

import saltobj

def _just_print(j):
    print j, '\n'

saltobj.ForkedSaltPipeWriter().main_loop(_just_print)
