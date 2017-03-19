# coding: utf-8

import logging, copy
import json, urwid, inspect, re
import dateutil.parser, datetime
from fnmatch import fnmatch

import salt.output

from saltobj.config import SaltConfigMixin

SHOW_JIDS = False

NA = '<n/a>'
tagtop_re = re.compile(r'^\s*([^\s{}:]+)\s*{')

REFORMAT_IDS = lambda x: x

def reformat_minion_ids(matchers):
    def _m(minion_id):
        log = logging.getLogger('REFORMAT_IDS')
        for matcher in matchers:
            if matcher.match(minion_id):
                log.debug("matcher={0} matched id={1}".format(matcher, minion_id))
                minion_id = '.'.join(matcher.groups())
                log.debug("        reformatted id={0}".format(minion_id))
        return minion_id
    global REFORMAT_IDS
    REFORMAT_IDS = _m

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

def _count_bases(x, classes):
    if x not in classes:
        return 0
    if not x._ordering:
        c = 1
        for b in x.__bases__:
            if b in classes:
                c += _count_bases(b, classes)
        x._ordering = c
    return x._ordering

def event_classes():
    # attempt to impose an orderin on the classes, such that a subclass of a
    # class is tried before the class while matching classes
    classes = []
    for cls in globals().values():
        if inspect.isclass( cls ) and issubclass(cls, Event):
            cls._ordering = 0
            classes.append(cls)
    classes = sorted([ (_count_bases(x,classes),x) for x in classes ])
    classes.reverse()
    return [ x[1] for x in classes ]

def classify_event(json_data):
    raw = grok_json_event(json_data)
    for cls in event_classes():
        if inspect.isclass( cls ) and issubclass(cls, Event) and cls.match(raw):
            return cls(raw)
    return Event(raw)

def my_args_format(x):
    if not x or x is NA:
        return ''
    if not isinstance(x, (list,tuple)):
        return json.dumps(x)

    ret = []
    for i in x:
        if isinstance(i,dict):
            for k,v in i.iteritems():
                ret.append(u'{0}={1}'.format(k,v))
        else:
            ret.append(i)
    for i,v in enumerate(ret):
        if u' ' in v:
            ret[i] = u'«{0}»'.format(v)
    return u' '.join(ret)

def my_jid_format(jid):
    try:
        jid = str(jid)
        if len(jid) != 20:
            return ''
        year = jid[:4]
        month = jid[4:6]
        day = jid[6:8]
        hour = jid[8:10]
        minute = jid[10:12]
        second = jid[12:14]
        micro = jid[14:]
        return '{0}-{1}-{2} {3}:{4}:{5}.{6}'.format( year,month,day,hour,minute,second,micro )
    except:
        return jid

class Event(SaltConfigMixin):
    matches = ()

    def __init__(self, raw):
        self.log = logging.getLogger(self.__class__.__name__)
        self.raw = raw
        self.tag = self.raw.get('tag', NA)
        self.dat = self.raw.get('data', {})

        # This is meant to descend into minion returns to syndic returns to
        # master.  It's not totally obvious when to go into data={'data': {}},
        # but this rule seems to be right most of the time.
        while 'data' in self.dat and isinstance(self.dat['data'],dict) and 'id' in self.dat['data']:
            self.dat = self.dat['data']

        self.stamp = self.dat.get('_stamp')
        self.dtime = dateutil.parser.parse(self.stamp) if self.stamp else None

    @property
    def evno(self):
        return self.raw.get('_evno')

    @property
    def long(self):
        return json.dumps(self.raw, indent=2)

    @classmethod
    def match(cls, raw):
        if not hasattr(cls,'matches') or not cls.matches:
            return False
        for m in cls.matches:
            _find = raw
            key, pat = m
            tstr = _find.get(key)
            while tstr is None and 'data' in _find:
                _find = _find['data']
                tstr = _find.get(key)
            if tstr is None:
                return False
            if isinstance(pat,str):
                if not fnmatch(tstr, pat):
                    return False
            elif not pat.match(tstr):
                return False
        return True

    def has_tag(self, pat):
        return self._glob(self.tag, pat)

    def try_attr(self, attr, default=NA, no_none=False, preformat=None):
        ret = default
        if not isinstance(attr, (list,tuple)):
            attr = (attr,)
        for a in attr:
            if hasattr(self,a):
                ret = getattr(self,a)
                break;
            elif a in self.dat:
                ret = self.dat[a]
                break;
            elif a in self.raw:
                ret = self.raw[a]
                break;
        if no_none and ret is None:
            ret = default
        if preformat and not isinstance(ret, (str,unicode)):
            ret = preformat(ret)
        return ret

    @property
    def who(self):
        return REFORMAT_IDS( self.try_attr('id') )

    @property
    def what(self):
        return (
            self.try_attr('fun'),
            self.try_attr('fun_args', preformat=my_args_format),
        )

    @property
    def columns(self):
        columns = []
        for item in [ self.__class__.__name__, self.who, self.what ]:
            if isinstance(item, (list,tuple)):
                item = u' '.join(item)
            columns.append(item.replace('<n/a>',''))
        return columns

    @property
    def short(self):
        return u' '.join(self.columns).replace('<n/a>','')

    def __repr__(self):
        return '{0.evno} {0.cname}'.format(self)
    __str__ = __repr__

class Auth(Event):
    matches = (( 'tag', 'salt/auth' ),)

    def __init__(self, *args, **kwargs):
        super(Auth,self).__init__(*args,**kwargs)
        self.result = self.dat.get('result', False)
        self.id     = self.dat.get('id', NA)
        self.act    = self.dat.get('act', NA)

    @property
    def what(self):
        v = self.try_attr('act')
        if v == 'accept':
            v = u"{0} → {1}".format(v, self.try_attr('result') )
        return v

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
    matches = (( 'tag', re.compile(r'\d+') ),)
    who = 'local'

    def __init__(self, *args, **kwargs):
        super(ExpectedReturns,self).__init__(*args,**kwargs)
        self.minions = self.dat.get('minions', [])
        self.jid = self.tag.split('/')[-1]

    @property
    def what(self):
        return ', '.join(self.minions)

class SyndicExpectedReturns(ExpectedReturns):
    matches = (('tag',re.compile(r'syndic/[^/]+/\d+')),)
    who = ''

    def __init__(self, *args, **kwargs):
        super(SyndicExpectedReturns,self).__init__(*args,**kwargs)
        self.syndic = self.tag.split('/')[1]
        self.who = self.syndic

class Publish(JobEvent):
    matches = (('tag', 'salt/job/*/new'),)
    who = ''

    def __init__(self, *args, **kwargs):
        super(Publish,self).__init__(*args,**kwargs)
        self.user    = self.dat.get('user', NA)
        self.minions = self.dat.get('minions', [])
        self.who     = 'local'

    @property
    def what(self):
        tgt = self.try_attr('tgt')
        tgt_type = self.try_attr('tgt_type')

	# this is cut and pasted from salt/minion.py:Matcher.compound_match
        # it doesn't seem to be defined anywhere else
        # then I reversed it, ... der.
        # ref = {'G': 'grain',
        #        'P': 'grain_pcre',
        #        'I': 'pillar',
        #        'J': 'pillar_pcre',
        #        'L': 'list',
        #        'N': None,      # Nodegroups should already be expanded
        #        'S': 'ipcidr',
        #        'E': 'pcre'}

        unref = {
            'grain':        'G',
            'grain_pcre':   'P',
            'pillar':       'I',
            'pillar_pcre':  'J',
            'list':         'L',
            'ipcidr':       'S',
            'pcre':         'E',
            'glob':         None
        }

        if tgt_type in unref:
            if unref[tgt_type] is not None:
                tv = u'{0}@{1}'.format(unref[tgt_type],tgt)
            else:
                tv = u'{0}'.format(tgt)
        else:
            tv = '<{0}>@{1}'.format( self.try_attr('tgt_type'), self.try_attr('tgt') )

        return u'{target} {fun} {fun_args}'.format(
            target=tv, fun=self.try_attr('fun'),
            fun_args=self.try_attr('arg', preformat=my_args_format),
        )

class Return(JobEvent):
    matches = (('tag', 'salt/job/*/ret/*'),)
    ooverrides = {}

    def __init__(self, *args, **kwargs):
        super(Return,self).__init__(*args,**kwargs)
        self.success = self.dat.get('success', NA)
        self.retcode = self.dat.get('retcode', 0)
        self.returnd = self.dat.get('return', 0)
        self.id      = self.dat.get('id', NA)

    def _oo(self,o,v=None):
        if o not in self.salt_opts:
            return None
        if o not in self.__class__.ooverrides:
            self.__class__.ooverrides[o] = self.salt_opts[o]
        if v is not None:
            if isinstance(v,(list,tuple)):
                try: idx = v.index(self.__class__.ooverrides[o])
                except: idx = 0
                idx = (idx+1) % len(v)
                self.__class__.ooverrides[o] = v[idx]
                self.log.debug("setting oo[{0}] to {1} (via idx={2})".format(o,v[idx],idx))
            else:
                self.__class__.ooverrides[o] = v
        return self.__class__.ooverrides[o]

    @property
    def outputter_opts(self):
        return [
            {'fmt': '[o]utput-{0}',  'key':'o', 'cb':self._oo, 'args':['state_output'],  'choices':['full', 'changes', 'terse', 'mixed']},
            {'fmt': '[v]erbose={0}', 'key':'v', 'cb':self._oo, 'args':['state_verbose'], 'choices':[True,False]},
        ]

    @property
    def outputter(self):
        dat = self.raw.get('data', {})
        outputter = dat.get('out', 'nested')
        return_data = copy.deepcopy( dat.get('return', dat) )
        to_output = { dat.get('id', 'local'): return_data }
        if outputter:
            self.log.debug('trying to apply outputter')
            __opts__ = self.salt_opts
            __opts__.update(self.__class__.ooverrides)
            res = salt.output.out_format(to_output, outputter, __opts__, **self.__class__.ooverrides)
            self.log.debug('outputter put out {0} bytes'.format(len(res)))
            if res:
                ret = [
                    'jid:  {0}'.format(self.jid),
                    'fun:  {0} {1}'.format(self.fun, self.args_str),
                    'time: {0}'.format(self.dtime.ctime()),
                    '', res.rstrip()
                ]
                return '\n'.join(ret)
        return self.long

class StateReturn(Return):
    matches = Return.matches + (
        ('fun', 'state.sls',),
    )

    def __init__(self, *a, **kw):
        super(StateReturn,self).__init__(*a,**kw)
        self.changes = {}
        self.results = {}

        self.changes_count = 0
        self.result_counts = [0,0]

        if isinstance(self.returnd, dict):
            for v in self.returnd.values():
                if '__id__' in v:
                    if 'changes' in v and isinstance(v['changes'],dict):
                        self.changes[ v['__id__'] ] = v['changes']
                        if v['changes']:
                            self.changes_count += 1
                    if 'result' in v:
                        self.results[ v['__id__'] ] = bool(v['result'])
                        self.result_counts[1] += 1
                        if v['result']:
                            self.result_counts[0] += 1

    @property
    def what(self):
        w = super(StateReturn,self).what
        m = 'changes={0} success={1}/{2}'.format( self.changes_count, *self.result_counts )
        if isinstance(w,(list,tuple)):
            return w + (m,)
        return '{0} {1}'.format(w,m)

class PublishRun(JobEvent):
    matches = (('tag', 'salt/run/*/new'),)

    def __init__(self, *args, **kwargs):
        super(PublishRun,self).__init__(*args,**kwargs)
        self.user = self.dat.get('user', NA)

class RunReturn(Return):
    matches = (('tag', 'salt/run/*/ret'),)

    def __init__(self, *args, **kwargs):
        super(RunReturn,self).__init__(*args,**kwargs)
        self.success = self.dat.get('success', NA)
        self.returnd = self.dat.get('return', 0)

class JCReturn(Return):
    matches = (('tag', 'uevent/job_cache/*/ret/*'),)

class EventSend(Event):
    matches = (
        ('cmd',       '_minion_event'),
        ('__pub_fun', 'event.send'),
    )

    def __init__(self, *args, **kwargs):
        super(EventSend,self).__init__(*args,**kwargs)

        dat = self.dat
        while '__pub_fun' not in dat and 'data' in dat:
            dat = dat['data']

        self.sent = {}
        if '__pub_fun' in dat:
            self.sent = copy.deepcopy(dat)
            to_remove = set()
            for k in self.sent:
                if k.startswith('__'):
                    to_remove.add(k)
            for k in to_remove:
                del self.sent[k]

    @property
    def what(self):
        return (
            self.tag,
            self.sent,
        )
