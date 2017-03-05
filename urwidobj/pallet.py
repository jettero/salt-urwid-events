
_PALLET = {
    'main': {
        'status':   ('yellow', 'dark blue'),
        'selected': ( 'white', 'dark blue'),
    }
}


def get_pallet(group='main'):
    p = _PALLET.get(group, _PALLET['main'])
    p = [ (k,) + p[k] for k in sorted(p) ]

    return p
