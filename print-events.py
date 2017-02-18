#!/usr/bin/env python2

import saltobj, sys, signal, os, argparse, shelve
import misc

misc.be_root_you_fool()

_obdb = shelve.open('ob.db')

def _c(x,subspace, fmt=None):
    ss = _obdb.get(subspace, {})
    if x not in ss:
        c = len(ss)+1
        ss[x] = fmt.format(c) if fmt else c
        _obdb[subspace] = ss
        _obdb.sync()
    return ss[x]

def _obfu(id):
    id = str(id)
    if id in _obdb:
        return _obdb[id]
    idx  = id.index('.')
    host = id[0:idx]
    dom  = id[idx+1:]

    host = _c(host,'_h', 'host{0}')
    dom  = _c(dom,'_d', 'dom{0}')

    o = _obdb[id] = '.'.join([host,dom])
    return o

def _obfur(dat, namespaces=True):
    for k in _obdb:
        if isinstance(_obdb[k],dict) and namespaces:
            for i in _obdb[k]:
                dat = dat.replace(i,_obdb[k][i])
        elif isinstance(_obdb[k],str):
            dat = dat.replace(k,_obdb[k])
    return dat

def _pre(d):
    if 'pub' in d and 'KEY' in d['pub']:
        d['pub'] = '---GPG PUBKEY--'
    if 'data' in d:
        d['data'] = _pre(d['data'])
    if 'id' in d and '.' in d['id']:
        d['id'] = _obfu(d['id'])
    if 'minions' in d:
        d['minions'] = [ _obfu(x) for x in d['minions'] ]
    if 'tag' in d:
        d['tag'] = _obfur(d['tag'],False)
    if 'tgt' in d and d.get('tgt_type') == 'glob':
        d['tgt'] = _obfur(d['tgt'])
    return d

def _print(j):
    print j, '\n'
    sys.stdout.flush()

def see_ya(*a):
    print "\nsee ya"
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("print-events: [options]")
    parser.add_argument('-r', '--replay-file', type=str)
    parser.add_argument('-o', '--replay-only', action='store_true')
    args = parser.parse_args()

    signal.signal(signal.SIGINT, see_ya)
    a = {
        'preproc':     _pre,
        'replay_file': args.replay_file,
        'replay_only': args.replay_only,
    }
    saltobj.ForkedSaltPipeWriter(**a).main_loop(_print)
