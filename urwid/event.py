
import saltobj
import urwid

class JobItem(urwid.Text):
    def __init__(self, jitem):
        self.jitem = jitem
        super(JobItem,self).__init__( ('jitem', jitem.jid) )

    def __eq__(self, other):
        return other.jitem == self.jitem

class JobList(uriwid.ListBox):
    def __init__(self):
        self.jc = saltobj.jidcollector()
        self.jc.on_change(self._jc_update)
        self.events = []
        self.walker = urwid.SimpleListWalker(self.events)
        super(JobList,self).__init__( self.walker )

    def _jc_update(self, jitem, actions):
        if 'new-jid' in actions:
            if jitem not in self.events:
                self.events.append(JobItem(jitem))
        # TODO: append-event, add-expected, remove-expected, add-returned
