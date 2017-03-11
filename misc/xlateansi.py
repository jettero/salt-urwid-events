
import re, itertools

ansi_color_sequence = re.compile(r'\x1b\[([\d\;]*)m')

ANSI_PALLET16 = (
    ('ansi-black',           'black',          'default'),
    ('ansi-red',             'dark red',       'default'),
    ('ansi-green',           'dark green',     'default'),
    ('ansi-yellow',          'brown',          'default'),
    ('ansi-blue',            'dark blue',      'default'),
    ('ansi-magenta',         'dark magenta',   'default'),
    ('ansi-cyan',            'dark cyan',      'default'),
    ('ansi-white',           'light gray',     'default'),
                                              
    ('ansi-bold-black',      'dark gray',      'default'),
    ('ansi-bold-red',        'light red',      'default'),
    ('ansi-bold-green',      'light green',    'default'),
    ('ansi-bold-yellow',     'yellow',         'default'),
    ('ansi-bold-blue',       'light blue',     'default'),
    ('ansi-bold-magenta',    'light magenta',  'default'),
    ('ansi-bold-cyan',       'light cyan',     'default'),
    ('ansi-bold-white',      'white',          'default'),
)

def split_ansi(x):
    s = ansi_color_sequence.split(x)
    return [ ('',s.pop(0)) ] + zip(s[::2],s[1::2])

class AnsiAttr(object):
    bolded = False
    color  = None

    color_map = {
        30: 'black',
        31: 'red',
        32: 'green',
        33: 'yellow',
        34: 'blue',
        35: 'magenta',
        36: 'cyan',
        37: 'white',
    }

    def __init__(self,blah=False):
        self.update(blah)

    def update(self, blah):
        if not blah:
            self.bolded = False
            self.color  = None

        else:
            for i in blah.split(';'):
                try: i = int(i)
                except: continue
                if not i: continue

                if i == 39:
                    self.color = None
                    self.bolded = False
                elif i == 1:
                    self.bolded = True
                elif i == 0:
                    self.bolded = False
                elif self.color_map.get(i):
                    self.color = i
                    self.bolded = False

    @property
    def mapped(self):
        c = self.color_map.get(self.color, 'default')
        if c == 'default' or c is None:
            self.bolded = False
        return (self.bolded, c)

    @property
    def attr(self):
        if self.color is None:
            return 'default'
        m = self.mapped
        ret = ['ansi']
        if m[0]:
            ret.append('bold')
        ret.append(m[1])
        return '-'.join(ret)

    def __repr__(self):
        return "AnsiAttr({0.attr})".format(self)

def xlate_ansi(x):
    ret = []
    aa = AnsiAttr()
    for c,t in split_ansi(x):
        aa.update(c)
        ret.append( (aa.attr,t) )
    return ret


def format_code(x, xlate=True, to_try=None, no_errors=False, with_meta=False):
    try:
        import pygments
    except Exception as e:
        print "exception trying to format code: {0}".format(e)
        return x

    f = pygments.formatters.TerminalFormatter()

    if to_try is None:
        to_try = ('json', 'yaml', 'python')

    if not isinstance(to_try, (tuple,list)):
        to_try = (to_try,)

    best_tokens = False
    for lname in to_try:
        lexer = pygments.lexers.get_lexer_by_name(lname)
        tokens,spare_tokens = itertools.tee(pygments.lex(x, lexer))

        c = 0
        for t in spare_tokens:
            if t[0][0] == 'Error':
                c += 1

        if no_errors and c:
            continue

        if best_tokens and c >= best_tokens[0]:
            continue

        best_tokens = (c, tokens, lname)

    if best_tokens:
        formatted = pygments.format(best_tokens[1],f)
        if xlate:
            formatted = xlate_ansi( formatted )
        if with_meta:
            return {'errors': best_tokens[0], 'formatted': formatted, 'lexer': best_tokens[2]}
        return formatted

    return x
