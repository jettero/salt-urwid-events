
import json, glob, os, re, collections
import saltobj.event

notes    = glob.glob(os.path.dirname(__file__) + "/*.js")
events   = {}
event_re = re.compile(r'^{$.+?^}$', re.DOTALL|re.MULTILINE)

for fname in notes:
    with open(fname,'r') as fh:
        dat = event_re.findall(fh.read())
    if dat:
        key = os.path.basename(fname).replace('.js','').replace('-','_')
        events[key] = []
        for item in dat:
            try: events[key].append( saltobj.event.classify_event(item) )
            except: pass

NTUPTYPE = collections.namedtuple('Notes', events.keys())
events = NTUPTYPE(**events)
