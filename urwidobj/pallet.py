
_PALLET = {
    'main': {
        'status': ('yellow', 'darkblue',),
    }
}


def pallet(group='main'):
    p = _PALLET.get(group, _PALLET['main'])

    return [ (k,) + p[k] for sorted(p) ]
