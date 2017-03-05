
_PALLET = {
    'main': {
        'status':   (     'yellow', 'dark blue'),
        'selected': ( 'light blue',   'default'),
    }
}


def get_pallet(group='main'):
    p = _PALLET.get(group, _PALLET['main'])
    p = [ (k,) + p[k] for k in sorted(p) ]

    return p
