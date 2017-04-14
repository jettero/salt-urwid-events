
from misc.xlateansi import ANSI_PALLET16

_PALLET = {
    'main': {
        'status':   ( 'yellow',     'dark blue'),
        'selected': ( 'light blue', 'default'  ),

        'ayt':             ( 'yellow',      'default' ),
        'rc_bad':          ( 'dark red',    'default' ),
        'rc_ok':           ( 'dark green',  'default' ),
        'rc_bad-changes':  ( 'light red',   'default' ),
        'rc_ok-changes':   ( 'light green', 'default' ),
        'changes':         ( 'dark cyan',   'default' ),
    }
}

def get_pallet(group='main'):
    p = _PALLET.get(group, _PALLET['main'])

    p = [ (k,) + p[k] for k in sorted(p) ]
    p.extend( ANSI_PALLET16 )

    return p
