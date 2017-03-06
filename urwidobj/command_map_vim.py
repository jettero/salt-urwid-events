
import urwid

def add_vim_keys():
    urwid.command_map['h'] = urwid.CURSOR_LEFT
    urwid.command_map['j'] = urwid.CURSOR_DOWN
    urwid.command_map['k'] = urwid.CURSOR_UP
    urwid.command_map['l'] = urwid.CURSOR_RIGHT

    urwid.command_map['ctrl b'] = urwid.CURSOR_PAGE_UP
    urwid.command_map['ctrl f'] = urwid.CURSOR_PAGE_DOWN

def add_right_activate(widget):
    widget._command_map = ac = urwid.command_map.copy()
    ac['l'] = ac['right'] = urwid.ACTIVATE

