
import re

ansi_color_sequence = re.compile(r'\x1b\[([\d\;]*)m')

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
        39: None, # reset foreground color
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

                if i == 1:
                    self.bolded = True
                elif i == 0:
                    self.bolded = False
                elif i in self.color_map:
                    # don't set the color if we don't handle it
                    # so we effectively ignore codes we don't handle
                    self.color = i

    @property
    def words(self):
        if self.color is None:
            return 'default'

        # XXX: handle extended colors
        # XXX: handle background colors

        if self.color == 33:
            return "yellow" if self.bolded else "brown"

        if self.color == 37:
            return "white" if self.bolded else "light gray"

        if self.color == 30:
            return "dark gray" if self.bolded else "black"

        c = self.color_map.get(self.color)
        if c is None:
            # this shouldn't happen since we ignore colors we don't know  in
            # update, but better safe than sorry
            return 'default'
        return ("light {0}" if self.bolded else "dark {0}").format(c)

    def __repr__(self):
        return "AnsiAttr(bolded={0.bolded}, color={0.color})".format(self)

def xlate_ansi(x):
    ret = []
    aa = AnsiAttr()
    for c,t in split_ansi(x):
        aa.update(c)
        ret.append( (aa.words,t) )
    return ret


def format_code(x, xlate=True):
    try:
        import pygments

        f = pygments.formatters.TerminalFormatter()

        to_try = ('json', 'yaml', 'python', 'bash')
        for lname in to_try:
            l = pygments.lexers.get_lexer_by_name(lname)
            h = pygments.highlight(x,l,f)
            if xlate:
                return xlate_ansi( pygments.highlight(x, l, f) )
            return h

    except Exception as e:
        print "exception trying to format code: {0}".format(e)

    return x
