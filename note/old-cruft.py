# this used to be a way to load examples right from the sources, but  
# the replay logs turn out to be more convenient imo

def extract_examples(classify=True):
    jsons = []
    f = __file__.replace('.pyc','.py')
    with open(f, 'r') as fh:
        cur = ''
        for line in fh.readlines():
            if line.startswith('#E# '):
                cur += line[4:]
            elif cur:
                jsons.append(cur)
                cur = ''
    if classify:
        ret = []
        for x in jsons:
            try: ret.append( classify_event(x) )
            except Exception as e:
                x = x.splitlines()
                y = 0
                for i in range(len(x)):
                    y += 1
                    x[i] = '{0:03d} {1}'.format(y,x[i])
                x = '\n'.join(x)
                raise
                #print "Exception({e}), failed to classify:\n{x}".format(e=e, x=x)
        return ret
    return jsons

# XXX: below examples include syndics returning lists of minions expected to return
#      incorporate that somehow

# XXX: the examples below also show a re-written result, data-in-data is removed already
#      what does state.event pretty do to refornicate the data??
#      collected examples of syndication... looks like we receive the events multiple times
#      the final form has the syndic info stripped off already

### examples from experimental/no-urwid-events.py
#E# {
#E#   "tag": "20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:53.974017", 
#E#     "minions": []
#E#   }
#E# } 

#E# {
#E#   "tag": "salt/job/20170211093753973385/new", 
#E#   "data": {
#E#     "tgt_type": "glob", 
#E#     "jid": "20170211093753973385", 
#E#     "tgt": "host00.dc2", 
#E#     "_stamp": "2017-02-11T17:37:53.974437", 
#E#     "user": "sudo_jettero", 
#E#     "arg": [
#E#       "role"
#E#     ], 
#E#     "fun": "grains.get", 
#E#     "minions": []
#E#   }
#E# } 

#E# {
#E#   "tag": "20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:54.321302", 
#E#     "tag": "20170211093753973385", 
#E#     "data": {
#E#       "_stamp": "2017-02-11T17:37:54.249523", 
#E#       "minions": []
#E#     }
#E#   }
#E# } 

#E# {
#E#   "tag": "syndic/salt.stage.or1:b91edb59-f18c-9a7d-5af4-c28358f401fb/20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:54.321722", 
#E#     "minions": []
#E#   }
#E# } 

#E# {
#E#   "tag": "salt/job/20170211093753973385/new", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:54.322040", 
#E#     "tag": "salt/job/20170211093753973385/new", 
#E#     "data": {
#E#       "tgt_type": "glob", 
#E#       "jid": "20170211093753973385", 
#E#       "tgt": "host00.dc2", 
#E#       "_stamp": "2017-02-11T17:37:54.249680", 
#E#       "user": "sudo_jettero", 
#E#       "arg": [
#E#         "role"
#E#       ], 
#E#       "fun": "grains.get", 
#E#       "minions": []
#E#     }
#E#   }
#E# } 

#E# {
#E#   "tag": "20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.103770", 
#E#     "tag": "20170211093753973385", 
#E#     "data": {
#E#       "_stamp": "2017-02-11T17:37:54.396075", 
#E#       "minions": []
#E#     }
#E#   }
#E# } 

#E# {
#E#   "tag": "syndic/saltmaster.dc5/20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.104137", 
#E#     "minions": []
#E#   }
#E# } 

#E# {
#E#   "tag": "salt/job/20170211093753973385/new", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.104408", 
#E#     "tag": "salt/job/20170211093753973385/new", 
#E#     "data": {
#E#       "tgt_type": "glob", 
#E#       "jid": "20170211093753973385", 
#E#       "tgt": "host00.dc2", 
#E#       "_stamp": "2017-02-11T17:37:54.397843", 
#E#       "user": "sudo_jettero", 
#E#       "arg": [
#E#         "role"
#E#       ], 
#E#       "fun": "grains.get", 
#E#       "minions": []
#E#     }
#E#   }
#E# } 

#E# {
#E#   "tag": "syndic/saltmaster.dc5/salt/job/20170211093753973385/new", 
#E#   "data": {
#E#     "tgt_type": "glob", 
#E#     "jid": "20170211093753973385", 
#E#     "tgt": "host00.dc2", 
#E#     "_stamp": "2017-02-11T17:37:55.104706", 
#E#     "user": "sudo_jettero", 
#E#     "arg": [
#E#       "role"
#E#     ], 
#E#     "fun": "grains.get", 
#E#     "minions": []
#E#   }
#E# } 

#E# {
#E#   "tag": "20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.456486", 
#E#     "tag": "20170211093753973385", 
#E#     "data": {
#E#       "_stamp": "2017-02-11T17:37:54.357814", 
#E#       "minions": [
#E#         "host00.dc2"
#E#       ]
#E#     }
#E#   }
#E# } 

#E# {
#E#   "tag": "syndic/saltmaster.dc2/20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.456856", 
#E#     "minions": [
#E#       "host00.dc2"
#E#     ]
#E#   }
#E# } 

#E# {
#E#   "tag": "20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.456890", 
#E#     "tag": "20170211093753973385", 
#E#     "data": {
#E#       "_stamp": "2017-02-11T17:37:54.351020", 
#E#       "minions": []
#E#     }
#E#   }
#E# } 

#E# {
#E#   "tag": "salt/job/20170211093753973385/new", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.457123", 
#E#     "tag": "salt/job/20170211093753973385/new", 
#E#     "data": {
#E#       "tgt_type": "glob", 
#E#       "jid": "20170211093753973385", 
#E#       "tgt": "host00.dc2", 
#E#       "_stamp": "2017-02-11T17:37:54.358251", 
#E#       "user": "sudo_jettero", 
#E#       "arg": [
#E#         "role"
#E#       ], 
#E#       "fun": "grains.get", 
#E#       "minions": [
#E#         "host00.dc2"
#E#       ]
#E#     }
#E#   }
#E# } 

#E# {
#E#   "tag": "syndic/saltmaster.dc3/20170211093753973385", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.457289", 
#E#     "minions": []
#E#   }
#E# } 

#E# {
#E#   "tag": "syndic/saltmaster.dc2/salt/job/20170211093753973385/new", 
#E#   "data": {
#E#     "tgt_type": "glob", 
#E#     "jid": "20170211093753973385", 
#E#     "tgt": "host00.dc2", 
#E#     "_stamp": "2017-02-11T17:37:55.457439", 
#E#     "user": "sudo_jettero", 
#E#     "arg": [
#E#       "role"
#E#     ], 
#E#     "fun": "grains.get", 
#E#     "minions": [
#E#       "host00.dc2"
#E#     ]
#E#   }
#E# } 

#E# {
#E#   "tag": "salt/job/20170211093753973385/new", 
#E#   "data": {
#E#     "_stamp": "2017-02-11T17:37:55.457563", 
#E#     "tag": "salt/job/20170211093753973385/new", 
#E#     "data": {
#E#       "tgt_type": "glob", 
#E#       "jid": "20170211093753973385", 
#E#       "tgt": "host00.dc2", 
#E#       "_stamp": "2017-02-11T17:37:54.352037", 
#E#       "user": "sudo_jettero", 
#E#       "arg": [
#E#         "role"
#E#       ], 
#E#       "fun": "grains.get", 
#E#       "minions": []
#E#     }
#E#   }
#E# } 

### from salt-run state.event pretty=true, not how the data is really presented.
# Data really arrives with an outer wrapper dict with 'tag' and 'data' (which
# is pictured below) — e.g., { 'tag': 'salt/auth', 'data': {'_stamp': …, 'id': … …}}

#E# salt/auth	{
#E#     "_stamp": "2017-02-11T15:23:10.007126", 
#E#     "act": "accept", 
#E#     "id": "blarg.minion", 
#E#     "pub": "xXxPUBKEYxXx", 
#E#     "result": true
#E# }

#E# salt/job/20170211102312056408/ret/blarg.minion	{
#E#     "_stamp": "2017-02-11T15:23:12.057250", 
#E#     "arg": [], 
#E#     "cmd": "_return", 
#E#     "fun": "test.ping", 
#E#     "fun_args": [], 
#E#     "id": "blarg.minion", 
#E#     "jid": "20170211102312056408", 
#E#     "retcode": 0, 
#E#     "return": true, 
#E#     "tgt": "blarg.minion", 
#E#     "tgt_type": "glob"
#E# }

#E# salt/auth	{
#E#     "_stamp": "2017-02-11T15:23:14.038099", 
#E#     "act": "accept", 
#E#     "id": "blarg.minion", 
#E#     "pub": "xXxPUBKEYxXx", 
#E#     "result": true
#E# }

#E# salt/job/20170211102316011780/ret/blarg.minion	{
#E#     "_stamp": "2017-02-11T15:23:16.012546", 
#E#     "arg": [
#E#         "role"
#E#     ], 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "blarg.minion", 
#E#     "jid": "20170211102316011780", 
#E#     "retcode": 0, 
#E#     "return": [
#E#         "salt-minion", 
#E#         "unifi"
#E#     ], 
#E#     "tgt": "blarg.minion", 
#E#     "tgt_type": "glob"
#E# }

### another example from a syndicated environment
#E# 20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:07.942976", 
#E#     "minions": [
#E#         "host29.dc1", 
#E#         "host20.dc1", 
#E#         "host26.dc1", 
#E#         "host30.dc1", 
#E#         "host21.dc1", 
#E#         "host22.dc1", 
#E#         "host28.dc1", 
#E#         "host27.dc1", 
#E#         "host24.dc1", 
#E#         "host31.dc1", 
#E#         "host23.dc1", 
#E#         "host25.dc1"
#E#     ]
#E# }

#E# salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:07.943359", 
#E#     "arg": [
#E#         "role"
#E#     ], 
#E#     "fun": "grains.get", 
#E#     "jid": "20170211073107942342", 
#E#     "minions": [
#E#         "host29.dc1", 
#E#         "host20.dc1", 
#E#         "host26.dc1", 
#E#         "host30.dc1", 
#E#         "host21.dc1", 
#E#         "host22.dc1", 
#E#         "host28.dc1", 
#E#         "host27.dc1", 
#E#         "host24.dc1", 
#E#         "host31.dc1", 
#E#         "host23.dc1", 
#E#         "host25.dc1"
#E#     ], 
#E#     "tgt": "host*.dc1 or host*.dc2", 
#E#     "tgt_type": "compound", 
#E#     "user": "sudo_jettero"
#E# }

#E# salt/job/20170211073107942342/ret/host30.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.242188", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host30.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host21.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.245316", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host21.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host20.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.245463", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host20.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host28.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.247815", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host28.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host29.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.250420", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host29.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host25.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.261851", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host25.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host31.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.274349", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host31.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host24.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.279060", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host24.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host23.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.320691", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host23.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# 20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:08.321102", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.209046", 
#E#         "minions": []
#E#     }, 
#E#     "tag": "20170211073107942342"
#E# }

#E# salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:08.321796", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.209206", 
#E#         "arg": [
#E#             "role"
#E#         ], 
#E#         "fun": "grains.get", 
#E#         "jid": "20170211073107942342", 
#E#         "minions": [], 
#E#         "tgt": "host*.dc1 or host*.dc2", 
#E#         "tgt_type": "compound", 
#E#         "user": "sudo_jettero"
#E#     }, 
#E#     "tag": "salt/job/20170211073107942342/new"
#E# }

#E# salt/job/20170211073107942342/ret/host27.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.357965", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host27.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host22.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.360358", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host22.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# salt/job/20170211073107942342/ret/host26.dc1	{
#E#     "_stamp": "2017-02-11T15:31:08.387076", 
#E#     "cmd": "_return", 
#E#     "fun": "grains.get", 
#E#     "fun_args": [
#E#         "role"
#E#     ], 
#E#     "id": "host26.dc1", 
#E#     "jid": "20170211073107942342", 
#E#     "retcode": 0, 
#E#     "return": "prod", 
#E#     "success": true
#E# }

#E# 20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:09.077900", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.522528", 
#E#         "minions": []
#E#     }, 
#E#     "tag": "20170211073107942342"
#E# }

#E# syndic/saltmaster.dc3/20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:09.078256", 
#E#     "minions": []
#E# }

#E# salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:09.078519", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.525079", 
#E#         "arg": [
#E#             "role"
#E#         ], 
#E#         "fun": "grains.get", 
#E#         "jid": "20170211073107942342", 
#E#         "minions": [], 
#E#         "tgt": "host*.dc1 or host*.dc2", 
#E#         "tgt_type": "compound", 
#E#         "user": "sudo_jettero"
#E#     }, 
#E#     "tag": "salt/job/20170211073107942342/new"
#E# }

#E# syndic/saltmaster.dc3/salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:09.078812", 
#E#     "arg": [
#E#         "role"
#E#     ], 
#E#     "fun": "grains.get", 
#E#     "jid": "20170211073107942342", 
#E#     "minions": [], 
#E#     "tgt": "host*.dc1 or host*.dc2", 
#E#     "tgt_type": "compound", 
#E#     "user": "sudo_jettero"
#E# }

#E# 20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:09.390708", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.320270", 
#E#         "minions": []
#E#     }, 
#E#     "tag": "20170211073107942342"
#E# }

#E# salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:09.391356", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.325005", 
#E#         "arg": [
#E#             "role"
#E#         ], 
#E#         "fun": "grains.get", 
#E#         "jid": "20170211073107942342", 
#E#         "minions": [], 
#E#         "tgt": "host*.dc1 or host*.dc2", 
#E#         "tgt_type": "compound", 
#E#         "user": "sudo_jettero"
#E#     }, 
#E#     "tag": "salt/job/20170211073107942342/new"
#E# }

#E# 20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:09.422275", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.340493", 
#E#         "minions": [
#E#             "host06.dc2", 
#E#             "host13.dc2", 
#E#             "host10.dc2", 
#E#             "host11.dc2", 
#E#             "host12.dc2", 
#E#             "host09.dc2", 
#E#             "host07.dc2", 
#E#             "host01.dc2", 
#E#             "host08.dc2", 
#E#             "host02.dc2", 
#E#             "host03.dc2", 
#E#             "host05.dc2", 
#E#             "host00.dc2", 
#E#             "host04.dc2"
#E#         ]
#E#     }, 
#E#     "tag": "20170211073107942342"
#E# }

#E# syndic/saltmaster.dc2/20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:09.422792", 
#E#     "minions": [
#E#         "host06.dc2", 
#E#         "host13.dc2", 
#E#         "host10.dc2", 
#E#         "host11.dc2", 
#E#         "host12.dc2", 
#E#         "host09.dc2", 
#E#         "host07.dc2", 
#E#         "host01.dc2", 
#E#         "host08.dc2", 
#E#         "host02.dc2", 
#E#         "host03.dc2", 
#E#         "host05.dc2", 
#E#         "host00.dc2", 
#E#         "host04.dc2"
#E#     ]
#E# }

#E# salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:09.423175", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.341049", 
#E#         "arg": [
#E#             "role"
#E#         ], 
#E#         "fun": "grains.get", 
#E#         "jid": "20170211073107942342", 
#E#         "minions": [
#E#             "host06.dc2", 
#E#             "host13.dc2", 
#E#             "host10.dc2", 
#E#             "host11.dc2", 
#E#             "host12.dc2", 
#E#             "host09.dc2", 
#E#             "host07.dc2", 
#E#             "host01.dc2", 
#E#             "host08.dc2", 
#E#             "host02.dc2", 
#E#             "host03.dc2", 
#E#             "host05.dc2", 
#E#             "host00.dc2", 
#E#             "host04.dc2"
#E#         ], 
#E#         "tgt": "host*.dc1 or host*.dc2", 
#E#         "tgt_type": "compound", 
#E#         "user": "sudo_jettero"
#E#     }, 
#E#     "tag": "salt/job/20170211073107942342/new"
#E# }

#E# syndic/saltmaster.dc2/salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:09.423629", 
#E#     "arg": [
#E#         "role"
#E#     ], 
#E#     "fun": "grains.get", 
#E#     "jid": "20170211073107942342", 
#E#     "minions": [
#E#         "host06.dc2", 
#E#         "host13.dc2", 
#E#         "host10.dc2", 
#E#         "host11.dc2", 
#E#         "host12.dc2", 
#E#         "host09.dc2", 
#E#         "host07.dc2", 
#E#         "host01.dc2", 
#E#         "host08.dc2", 
#E#         "host02.dc2", 
#E#         "host03.dc2", 
#E#         "host05.dc2", 
#E#         "host00.dc2", 
#E#         "host04.dc2"
#E#     ], 
#E#     "tgt": "host*.dc1 or host*.dc2", 
#E#     "tgt_type": "compound", 
#E#     "user": "sudo_jettero"
#E# }

#E# 20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:09.456502", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.297019", 
#E#         "minions": []
#E#     }, 
#E#     "tag": "20170211073107942342"
#E# }

#E# syndic/saltmaster.dc4/20170211073107942342	{
#E#     "_stamp": "2017-02-11T15:31:09.456974", 
#E#     "minions": []
#E# }

#E# salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:09.457289", 
#E#     "data": {
#E#         "_stamp": "2017-02-11T15:31:08.297193", 
#E#         "arg": [
#E#             "role"
#E#         ], 
#E#         "fun": "grains.get", 
#E#         "jid": "20170211073107942342", 
#E#         "minions": [], 
#E#         "tgt": "host*.dc1 or host*.dc2", 
#E#         "tgt_type": "compound", 
#E#         "user": "sudo_jettero"
#E#     }, 
#E#     "tag": "salt/job/20170211073107942342/new"
#E# }

#E# syndic/saltmaster.dc4/salt/job/20170211073107942342/new	{
#E#     "_stamp": "2017-02-11T15:31:09.457660", 
#E#     "arg": [
#E#         "role"
#E#     ], 
#E#     "fun": "grains.get", 
#E#     "jid": "20170211073107942342", 
#E#     "minions": [], 
#E#     "tgt": "host*.dc1 or host*.dc2", 
#E#     "tgt_type": "compound", 
#E#     "user": "sudo_jettero"
#E# }

#E# salt/job/20170211073107942342/ret/host06.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.132189", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host06.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host13.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.134529", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host13.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host10.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.136938", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host10.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host11.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.139644", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host11.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host01.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.142688", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host01.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host04.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.145832", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host04.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host08.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.148256", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host08.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host12.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.150758", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host12.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host09.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.153952", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host09.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host02.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.157807", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host02.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host03.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.161189", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host03.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host05.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.164399", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host05.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host00.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.168359", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host00.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }

#E# salt/job/20170211073107942342/ret/host07.dc2	{
#E#     "_stamp": "2017-02-11T15:31:10.173745", 
#E#     "fun": "grains.get", 
#E#     "fun_args": null, 
#E#     "id": "host07.dc2", 
#E#     "jid": "20170211073107942342", 
#E#     "return": "prod"
#E# }
