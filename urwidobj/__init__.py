import signal, misc

class EventApplication(object):
    pallet = [
        ('status', 'yellow', 'dark blue'),
    ]
    event_no = 0

    def __init__(self):
        self.status_txt = urwid.Text(('status', u"wating for events"))

        self.log = misc.setup_file_logger('urwidobj.EventApplication')

        self.jids = [urwid.Text('wtf')]
        self.jids_listwalker = urwid.SimpleListWalker(self.jids)
        self.jids_listbox = urwid.ListBox(self.jids_listwalker)
        self.main_frame = urwid.Frame(self.jids_listbox, footer=urwid.AttrMap(self.status_txt, 'status'))

        args   = (self.main_frame,self.pallet,)
        kwargs = { 'unhandled_input': self.exit_on_q }
        try:
            self.log.info("trying to use curses")
            kwargs['screen'] = urwid.curses_display.Screen()
            self.loop = urwid.MainLoop(*args, **kwargs)
        except Exception as e:
            self.log.debug("self.loop exception: {0}".format(e))
            self.log.info("failed to use curses, trying the default instead")
            if 'screen' in kwargs:
                del kwargs['screen']
            self.loop = urwid.MainLoop(*args, **kwargs)

        self._write_fd = self.loop.watch_pipe(self.got_event)
        self.sevent = ForkedSaltPipeWriter()
        self.sevent.pipe_loop(self._write_fd)

    def exit_on_q(self,input):
        if input in ('q', 'Q'):
            self.see_ya('q')

    def sig(self, signal,frame):
        self.hear_event('q')

    def run(self):
        signal.signal(signal.SIGINT, self.sig)
        self.loop.run()
        self.sevent.see_ya()

    def see_ya(self,*x):
        if len(x):
            self.log.debug("received signal={0}".format(x[0]))
        self.sevent.see_ya()
        raise urwid.ExitMainLoop()

    def status(self,status):
        self.status_txt.set_text(('banner', status))

    def hear_event(self, x):
        os.write( self._write_fd, x )

    def handle_salt_data(self, data):
        self.log.debug('trying to handle salt data')
        if 'data' in data:
            self.log.debug('return data found')
            if 'tag' in data:
                self.log.info('salt event tag: {0}'.format(data['tag']))
            job_data = data['data']
            if 'jid' in job_data:
                self.log.debug('trying to append jid={0} to the listbox'.format(job_data['jid']))
                self.jids_listwalker.append(urwid.Text(job_data['jid']))

    def got_event(self,data):
        if data.lower().strip() == 'q':
            self.see_ya('q')

        self.event_no += 1
        if self.event_no == 1: self.status(u'got event')
        else: self.status(u'got {0} events'.format(self.event_no))

        if data.startswith('json:'):
            try:
                self.handle_salt_data(json.loads(data[5:]))
            except Exception as e:
                self.log.warning("exception trying to handle json data: {0}".format(e))
                pass
