#!/usr/bin/env python2

import saltobj, sys, collections, signal, os
import misc

misc.be_root_you_fool()

# have to salt-call test.ping to populate ec2 in order for
# glob target *.ec2 to turn into *.dom1 like you'd expect
# mebbe use shelve to cache the obdb at some point?
_obdb = collections.defaultdict(lambda: {})
def _c(x,subspace, fmt=None):
    if x not in _obdb[subspace]:
        c = len(_obdb[subspace])+1
        _obdb[subspace][x] = fmt.format(c) if fmt else c
    return _obdb[subspace][x]

def _obfu(id):
    if id in _obdb:
        return _obdb[id]
    idx  = id.index('.')
    host = id[0:idx]
    dom  = id[idx+1:]

    host = _c(host,'_h', 'host{0}')
    dom  = _c(dom,'_d', 'dom{0}')

    o = _obdb[id] = '.'.join([host,dom])
    return o

def _pre(d):
    if 'pub' in d and 'KEY' in d['pub']:
        d['pub'] = '---GPG PUBKEY--'
    if 'data' in d:
        d['data'] = _pre(d['data'])
    if 'id' in d and '.' in d['id']:
        d['id'] = _obfu(d['id'])
    if 'tgt' in d and d.get('tgt_type') == 'glob':
        t = d['tgt']
        for s in ['_h','_d']:
            for i in _obdb[s]:
                t = t.replace(i,_obdb[s][i])
        d['tgt'] = t
    return d

def _print(j):
    print j, '\n'
    sys.stdout.flush()

def see_ya(*a):
    print "\nsee ya"
    exit(0)

signal.signal(signal.SIGINT, see_ya)
args = {'preproc': _pre}
if os.path.isfile('event.log'):
    args['replay_file'] = 'event.log'
    args['replay_only'] = True
saltobj.ForkedSaltPipeWriter(**args).main_loop(_print)
