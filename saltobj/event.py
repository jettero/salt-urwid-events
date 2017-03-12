# coding: utf-8

import logging, copy
import json, urwid, inspect, re
import dateutil.parser, datetime
from fnmatch import fnmatch

import salt.output

from saltobj.config import SaltConfigMixin

NA = '<n/a>'
tagtop_re = re.compile(r'^\s*([^\s{}:]+)\s*{')

class Job(object):
    def __init__(self, jid):
        self.jid       = jid
        self.events    = []
        self.expected  = set()
        self.returned  = set()
        self.listeners = []
        self.dtime     = None

    def append(self, event):
        if event.dtime and (not self.dtime or self.dtime < event.dtime):
            self.dtime = event.dtime
        self.events.append(event)

    @property
    def waiting(self):
        return bool( self.expected )

class jidcollector(object):
    def __init__(self):
        self.jids = {}

    def on_change(self, callback):
        if callback not in self.listeners:
            self.listeners.append(callback)

    def examine_event(self, event):
        if not isinstance(event,Event):
            try: event = classify_event(event)
            except: return

        actions = set()

        if hasattr(event,'jid'):
            if event.jid in self.jids:
                jitem = self.jids[ event.jid ]
            else:
                jitem = Job(event.jid)
                self.jids[ event.jid ] = jitem
                actions.add('new-jid')
            jitem.append(event)
            actions.add('append-event')
            if isinstance(event,ExpectedReturns):
                for m in event.minions:
                    if m not in jitem.expected:
                        actions.add('add-expected')
                        jitem.expected.add(m)
            if isinstance(event,Return):
                if event.id in jitem.expected:
                    if event.id in jitem.expected:
                        actions.add('remove-expected')
                        jitem.expected.remove(event.id)
                    if event.id not in jitem.returned:
                        actions.add('add-returned')
                        jitem.returned.add(event.id)

            if actions:
                for l in self.listeners:
                    l(jitem, tuple(actions))

    @property
    def waiting(self):
        ret = {}
        for jid,dat in self.jids.iteritems():
            if dat.waiting:
                ret[jid] = dat
        return ret

    def __repr__(self):
        ret = "jidcollection:\n"
        for jid,jitem in self.jids.iteritems():
            ret += ' - {jid} dtime={jitem.dtime} returned={jitem.returned} expected={jitem.expected}\n'.format(
                jid=jid, jitem=jitem)
        return ret

def grok_json_event(json_data):
    if isinstance(json_data, dict):
        return json_data

    m = tagtop_re.search(json_data)
    if m:
        tagtop = m.group(1)
        json_data = tagtop_re.sub('{', json_data)
    else:
        tagtop = None

    json_data = json.loads(json_data)
    if tagtop:
        json_data = { 'tag': tagtop, 'data': json_data }
    return json_data

def classify_event(json_data):
    raw = grok_json_event(json_data)
    tag = raw.get('tag', NA)
    cls = Event
    for clz in globals().values():
        if inspect.isclass( clz ) and issubclass(clz, Event) and hasattr(clz,'tag_match'):
            if clz.tag_match is not None and Event._match(tag, clz.tag_match):
                cls = clz
                break

    return cls(raw)

misc_format_lengths = {}
def misc_format_width(tag, the_str, lr='>'):
    l = misc_format_lengths.get(tag,0)
    this_len = len(the_str)
    if this_len > l:
        misc_format_lengths[tag] = l = this_len
    return '{0:{lr}{w}s}'.format( the_str, lr=lr, w=l )

class Event(SaltConfigMixin):
    tag_match = None

    def __init__(self, raw):
        self.log = logging.getLogger(self.__class__.__name__)
        self.raw = raw
        self.tag = self.raw.get('tag', NA)
        self.dat = self.raw.get('data', {})
        self.dinc = 0
        while 'data' in self.dat:
            self.dinc += 1
            self.dat = self.dat['data']

        self.stamp = self.dat.get('_stamp')
        self.dtime = dateutil.parser.parse(self.stamp) if self.stamp else None

    @property
    def evno(self):
        return self.raw.get('_evno')

    @property
    def long(self):
        return json.dumps(self.raw, indent=2)

    @property
    def short(self):
        return repr(self)

    @classmethod
    def _match(cls, in_str, pat):
        if isinstance(pat,str):
            return bool( fnmatch(in_str, pat) )
        return bool( pat.match(in_str) )

    def has_tag(self, pat):
        return self._glob(self.tag, pat)

    @property
    def who(self):
        id   = self.dat.get('id')
        user = self.dat.get('user','').replace('sudo_','')
        fun  = self.dat.get('fun')
        funa = self.dat.get('fun_args')

        if not id:
            return self.tag

        ret = [ misc_format_width('minion_id',id) ]
        if user: ret.append(user)
        if fun:
            ret.append(misc_format_width('fun',fun))
        if funa:
            ret.append( json.dumps(funa) )

        return ' '.join(ret)

    @property
    def cname(self):
        return misc_format_width('cname', self.__class__.__name__, lr='<')

    def __repr__(self):
        ret = '{0.evno:4d}.{0.cname} {0.who}'
        if hasattr(self,'retcode') and self.retcode is not None:
            ret += u' → {0.retcode}'
        return ret.format(self)
    __str__ = __repr__

class Auth(Event):
    tag_match = 'salt/auth'

    def __init__(self, *args, **kwargs):
        super(Auth,self).__init__(*args,**kwargs)
        self.result = self.dat.get('result', False)
        self.id     = self.dat.get('id', NA)
        self.act    = self.dat.get('act', NA)

class JobEvent(Event):
    def __init__(self, *args, **kwargs):
        super(JobEvent,self).__init__(*args,**kwargs)
        self.jid      = self.dat.get('jid', NA)
        self.fun      = self.dat.get('fun', NA)
        self.tgt      = self.dat.get('tgt', NA)
        self.tgt_type = self.dat.get('tgt_type', NA)

        self.args = self.dat.get('args', [])
        if self.args is None or not self.args:
            self.args = self.dat.get('fun_args', [])
            if self.args is None:
                self.args = []

        asr = [ ]
        for x in self.args:
            if isinstance(x,dict):
                for k,v in x.iteritems():
                    asr.append('{0}={1}'.format(k,v))
            else:
                asr.append(str(x))
        self.args_str = ' '.join(asr)

class ExpectedReturns(Event):
    tag_match = re.compile(r'\d+')

    def __init__(self, *args, **kwargs):
        super(ExpectedReturns,self).__init__(*args,**kwargs)
        self.minions = self.dat.get('minions', [])
        self.jid = self.tag.split('/')[-1]

class SyndicExpectedReturns(ExpectedReturns):
    tag_match = re.compile(r'syndic/[^/]+/\d+')

    def __init__(self, *args, **kwargs):
        super(SyndicExpectedReturns,self).__init__(*args,**kwargs)
        self.syndic = self.tag.split('/')[1]

class Publish(JobEvent):
    tag_match = 'salt/job/*/new'

    def __init__(self, *args, **kwargs):
        super(Publish,self).__init__(*args,**kwargs)
        self.user    = self.dat.get('user', NA)
        self.minions = self.dat.get('minions', [])

class Return(JobEvent):
    tag_match = 'salt/job/*/ret/*'

    def __init__(self, *args, **kwargs):
        super(Return,self).__init__(*args,**kwargs)
        self.success = self.dat.get('success', NA)
        self.retcode = self.dat.get('retcode', 0)
        self.returnd = self.dat.get('return', 0)
        self.id      = self.dat.get('id', NA)

        self.ooverrides = {}

    @property
    def outputter_opts(self):
        return {
            '[o]utput-{0}':  ['v', 'state_output', ['full', 'changes', 'terse', 'mixed']],
            '[v]erbose':     ['o', 'state_verbose', [True,False]],
        }

    @property
    def outputter(self):
        dat = self.raw.get('data', {})
        outputter = dat.get('out', 'nested')
        return_data = dat.get('return', dat)
        to_output = { dat.get('id', 'local'): return_data }
        if outputter:
            self.log.debug('trying to apply outputter')
            __opts__ = self.salt_opts
            res = salt.output.out_format(to_output, outputter, self.salt_opts)
            if res:
                ret = [
                    'jid:  {0}'.format(self.jid),
                    'fun:  {0} {1}'.format(self.fun, self.args_str),
                    'time: {0}'.format(self.dtime.ctime()),
                    '', res.rstrip()
                ]
                return '\n'.join(ret)
        return self.long

class JCReturn(Return):
    tag_match = 'uevent/job_cache/*/ret/*'
