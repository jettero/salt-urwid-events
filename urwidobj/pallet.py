
from misc.xlateansi import ANSI_PALLET16

_PALLET = {
    'main': {
        'status':   ( 'yellow',     'dark blue'),
        'selected': ( 'light blue', 'default'  ),

        'ayt':     ( 'yellow',     'default' ),
        'rc_bad':  ( 'dark red',   'default' ),
        'rc_ok':   ( 'dark green', 'default' ),
        'changes': ( 'bold',       'default' ),
    }
}

def get_pallet(group='main'):
    p = _PALLET.get(group, _PALLET['main'])

    p = [ (k,) + p[k] for k in sorted(p) ]
    p.extend( ANSI_PALLET16 )

    return p
