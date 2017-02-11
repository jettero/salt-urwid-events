# coding: utf-8

import json, urwid

__all__ = ["Return"]

class Return(object):
    def __init__(self, json_data):
        self.raw = json.loads(json_data)
        self.tag = self.dat('tag', '<?>')
        self.dat = self.dat('data', {})
        self.syn = []

        # XXX: below examples include syndics returning lists of minions expected to return
        #      incorporate that somehow

        # XXX: the examples below also show a re-written result, data-in-data is removed already
        #      what does state.event pretty do to refornicate the data??
        #      collected examples of syndication... looks like we receive the events multiple times
        #      the final form has the syndic info stripped off already

    @property
    def 

    @property
    def is_syndicated(self):
        return bool( self.syn )

### examples from experimental/no-urwid-events.py
# {
#   "tag": "20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:53.974017", 
#     "minions": []
#   }
# } 

# {
#   "tag": "salt/job/20170211093753973385/new", 
#   "data": {
#     "tgt_type": "glob", 
#     "jid": "20170211093753973385", 
#     "tgt": "host00.dc2", 
#     "_stamp": "2017-02-11T17:37:53.974437", 
#     "user": "sudo_jettero", 
#     "arg": [
#       "role"
#     ], 
#     "fun": "grains.get", 
#     "minions": []
#   }
# } 

# {
#   "tag": "20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:54.321302", 
#     "tag": "20170211093753973385", 
#     "data": {
#       "_stamp": "2017-02-11T17:37:54.249523", 
#       "minions": []
#     }
#   }
# } 

# {
#   "tag": "syndic/salt.stage.or1:b91edb59-f18c-9a7d-5af4-c28358f401fb/20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:54.321722", 
#     "minions": []
#   }
# } 

# {
#   "tag": "salt/job/20170211093753973385/new", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:54.322040", 
#     "tag": "salt/job/20170211093753973385/new", 
#     "data": {
#       "tgt_type": "glob", 
#       "jid": "20170211093753973385", 
#       "tgt": "host00.dc2", 
#       "_stamp": "2017-02-11T17:37:54.249680", 
#       "user": "sudo_jettero", 
#       "arg": [
#         "role"
#       ], 
#       "fun": "grains.get", 
#       "minions": []
#     }
#   }
# } 

# {
#   "tag": "syndic/salt.stage.or1:b91edb59-f18c-9a7d-5af4-c28358f401fb/salt/job/20170211093753973385/new", 
#   "data": {
#     "tgt_type": "glob", 
#     "jid": "20170211093753973385", 
#     "tgt": "host00.dc2", 
#     "_stamp": "2017-02-11T17:37:54.322445", 
#     "user": "sudo_jettero", 
#     "arg": [
#       "role"
#     ], 
#     "fun": "grains.get", 
#     "minions": []
#   }
# } 

# {
#   "tag": "20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.103770", 
#     "tag": "20170211093753973385", 
#     "data": {
#       "_stamp": "2017-02-11T17:37:54.396075", 
#       "minions": []
#     }
#   }
# } 

# {
#   "tag": "syndic/saltmaster.dc5/20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.104137", 
#     "minions": []
#   }
# } 

# {
#   "tag": "salt/job/20170211093753973385/new", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.104408", 
#     "tag": "salt/job/20170211093753973385/new", 
#     "data": {
#       "tgt_type": "glob", 
#       "jid": "20170211093753973385", 
#       "tgt": "host00.dc2", 
#       "_stamp": "2017-02-11T17:37:54.397843", 
#       "user": "sudo_jettero", 
#       "arg": [
#         "role"
#       ], 
#       "fun": "grains.get", 
#       "minions": []
#     }
#   }
# } 

# {
#   "tag": "syndic/saltmaster.dc5/salt/job/20170211093753973385/new", 
#   "data": {
#     "tgt_type": "glob", 
#     "jid": "20170211093753973385", 
#     "tgt": "host00.dc2", 
#     "_stamp": "2017-02-11T17:37:55.104706", 
#     "user": "sudo_jettero", 
#     "arg": [
#       "role"
#     ], 
#     "fun": "grains.get", 
#     "minions": []
#   }
# } 

# {
#   "tag": "20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.456486", 
#     "tag": "20170211093753973385", 
#     "data": {
#       "_stamp": "2017-02-11T17:37:54.357814", 
#       "minions": [
#         "host00.dc2""
#       ]
#     }
#   }
# } 

# {
#   "tag": "syndic/saltmaster.dc2/20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.456856", 
#     "minions": [
#       "host00.dc2""
#     ]
#   }
# } 

# {
#   "tag": "20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.456890", 
#     "tag": "20170211093753973385", 
#     "data": {
#       "_stamp": "2017-02-11T17:37:54.351020", 
#       "minions": []
#     }
#   }
# } 

# {
#   "tag": "salt/job/20170211093753973385/new", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.457123", 
#     "tag": "salt/job/20170211093753973385/new", 
#     "data": {
#       "tgt_type": "glob", 
#       "jid": "20170211093753973385", 
#       "tgt": "host00.dc2", 
#       "_stamp": "2017-02-11T17:37:54.358251", 
#       "user": "sudo_jettero", 
#       "arg": [
#         "role"
#       ], 
#       "fun": "grains.get", 
#       "minions": [
#         "host00.dc2""
#       ]
#     }
#   }
# } 

# {
#   "tag": "syndic/saltmaster.dc3/20170211093753973385", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.457289", 
#     "minions": []
#   }
# } 

# {
#   "tag": "syndic/saltmaster.dc2/salt/job/20170211093753973385/new", 
#   "data": {
#     "tgt_type": "glob", 
#     "jid": "20170211093753973385", 
#     "tgt": "host00.dc2", 
#     "_stamp": "2017-02-11T17:37:55.457439", 
#     "user": "sudo_jettero", 
#     "arg": [
#       "role"
#     ], 
#     "fun": "grains.get", 
#     "minions": [
#       "host00.dc2""
#     ]
#   }
# } 

# {
#   "tag": "salt/job/20170211093753973385/new", 
#   "data": {
#     "_stamp": "2017-02-11T17:37:55.457563", 
#     "tag": "salt/job/20170211093753973385/new", 
#     "data": {
#       "tgt_type": "glob", 
#       "jid": "20170211093753973385", 
#       "tgt": "host00.dc2", 
#       "_stamp": "2017-02-11T17:37:54.352037", 
#       "user": "sudo_jettero", 
#       "arg": [
#         "role"
#       ], 
#       "fun": "grains.get", 
#       "minions": []
#     }
#   }
# } 

### from salt-run state.event pretty=true, not how the data is really presented.
# Data really arrives with an outer wrapper dict with 'tag' and 'data' (which
# is pictured below) — e.g., { 'tag': 'salt/auth', 'data': {'_stamp': …, 'id': … …}}
#
# salt/auth	{
#     "_stamp": "2017-02-11T15:23:10.007126", 
#     "act": "accept", 
#     "id": "blarg.minion", 
#     "pub": "xXxPUBKEYxXx", 
#     "result": true
# }
# salt/job/20170211102312056408/ret/blarg.minion	{
#     "_stamp": "2017-02-11T15:23:12.057250", 
#     "arg": [], 
#     "cmd": "_return", 
#     "fun": "test.ping", 
#     "fun_args": [], 
#     "id": "blarg.minion", 
#     "jid": "20170211102312056408", 
#     "retcode": 0, 
#     "return": true, 
#     "tgt": "blarg.minion", 
#     "tgt_type": "glob"
# }
# salt/auth	{
#     "_stamp": "2017-02-11T15:23:14.038099", 
#     "act": "accept", 
#     "id": "blarg.minion", 
#     "pub": "xXxPUBKEYxXx", 
#     "result": true
# }
# salt/job/20170211102316011780/ret/blarg.minion	{
#     "_stamp": "2017-02-11T15:23:16.012546", 
#     "arg": [
#         "role"
#     ], 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "blarg.minion", 
#     "jid": "20170211102316011780", 
#     "retcode": 0, 
#     "return": [
#         "salt-minion", 
#         "unifi"
#     ], 
#     "tgt": "blarg.minion", 
#     "tgt_type": "glob"
# }

### another example from a syndicated environment
# 20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:07.942976", 
#     "minions": [
#         "host29.dc1", 
#         "host20.dc1", 
#         "host26.dc1", 
#         "host30.dc1", 
#         "host21.dc1", 
#         "host22.dc1", 
#         "host28.dc1", 
#         "host27.dc1", 
#         "host24.dc1", 
#         "host31.dc1", 
#         "host23.dc1", 
#         "host25.dc1"
#     ]
# }
# salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:07.943359", 
#     "arg": [
#         "role"
#     ], 
#     "fun": "grains.get", 
#     "jid": "20170211073107942342", 
#     "minions": [
#         "host29.dc1", 
#         "host20.dc1", 
#         "host26.dc1", 
#         "host30.dc1", 
#         "host21.dc1", 
#         "host22.dc1", 
#         "host28.dc1", 
#         "host27.dc1", 
#         "host24.dc1", 
#         "host31.dc1", 
#         "host23.dc1", 
#         "host25.dc1"
#     ], 
#     "tgt": "host*.dc1 or host*.dc2", 
#     "tgt_type": "compound", 
#     "user": "sudo_jettero"
# }
# salt/job/20170211073107942342/ret/host30.dc1	{
#     "_stamp": "2017-02-11T15:31:08.242188", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host30.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host21.dc1	{
#     "_stamp": "2017-02-11T15:31:08.245316", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host21.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host20.dc1	{
#     "_stamp": "2017-02-11T15:31:08.245463", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host20.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host28.dc1	{
#     "_stamp": "2017-02-11T15:31:08.247815", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host28.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host29.dc1	{
#     "_stamp": "2017-02-11T15:31:08.250420", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host29.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host25.dc1	{
#     "_stamp": "2017-02-11T15:31:08.261851", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host25.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host31.dc1	{
#     "_stamp": "2017-02-11T15:31:08.274349", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host31.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host24.dc1	{
#     "_stamp": "2017-02-11T15:31:08.279060", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host24.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host23.dc1	{
#     "_stamp": "2017-02-11T15:31:08.320691", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host23.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# 20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:08.321102", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.209046", 
#         "minions": []
#     }, 
#     "tag": "20170211073107942342"
# }
# salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:08.321796", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.209206", 
#         "arg": [
#             "role"
#         ], 
#         "fun": "grains.get", 
#         "jid": "20170211073107942342", 
#         "minions": [], 
#         "tgt": "host*.dc1 or host*.dc2", 
#         "tgt_type": "compound", 
#         "user": "sudo_jettero"
#     }, 
#     "tag": "salt/job/20170211073107942342/new"
# }
# salt/job/20170211073107942342/ret/host27.dc1	{
#     "_stamp": "2017-02-11T15:31:08.357965", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host27.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host22.dc1	{
#     "_stamp": "2017-02-11T15:31:08.360358", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host22.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# salt/job/20170211073107942342/ret/host26.dc1	{
#     "_stamp": "2017-02-11T15:31:08.387076", 
#     "cmd": "_return", 
#     "fun": "grains.get", 
#     "fun_args": [
#         "role"
#     ], 
#     "id": "host26.dc1", 
#     "jid": "20170211073107942342", 
#     "retcode": 0, 
#     "return": "prod", 
#     "success": true
# }
# 20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:09.077900", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.522528", 
#         "minions": []
#     }, 
#     "tag": "20170211073107942342"
# }
# syndic/saltmaster.dc3/20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:09.078256", 
#     "minions": []
# }
# salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:09.078519", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.525079", 
#         "arg": [
#             "role"
#         ], 
#         "fun": "grains.get", 
#         "jid": "20170211073107942342", 
#         "minions": [], 
#         "tgt": "host*.dc1 or host*.dc2", 
#         "tgt_type": "compound", 
#         "user": "sudo_jettero"
#     }, 
#     "tag": "salt/job/20170211073107942342/new"
# }
# syndic/saltmaster.dc3/salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:09.078812", 
#     "arg": [
#         "role"
#     ], 
#     "fun": "grains.get", 
#     "jid": "20170211073107942342", 
#     "minions": [], 
#     "tgt": "host*.dc1 or host*.dc2", 
#     "tgt_type": "compound", 
#     "user": "sudo_jettero"
# }
# 20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:09.390708", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.320270", 
#         "minions": []
#     }, 
#     "tag": "20170211073107942342"
# }
# salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:09.391356", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.325005", 
#         "arg": [
#             "role"
#         ], 
#         "fun": "grains.get", 
#         "jid": "20170211073107942342", 
#         "minions": [], 
#         "tgt": "host*.dc1 or host*.dc2", 
#         "tgt_type": "compound", 
#         "user": "sudo_jettero"
#     }, 
#     "tag": "salt/job/20170211073107942342/new"
# }
# 20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:09.422275", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.340493", 
#         "minions": [
#             "host06.dc2", 
#             "host13.dc2", 
#             "host10.dc2", 
#             "host11.dc2", 
#             "host12.dc2", 
#             "host09.dc2", 
#             "host07.dc2", 
#             "host01.dc2", 
#             "host08.dc2", 
#             "host02.dc2", 
#             "host03.dc2", 
#             "host05.dc2", 
#             "host00.dc2", 
#             "host04.dc2"
#         ]
#     }, 
#     "tag": "20170211073107942342"
# }
# syndic/saltmaster.dc2/20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:09.422792", 
#     "minions": [
#         "host06.dc2", 
#         "host13.dc2", 
#         "host10.dc2", 
#         "host11.dc2", 
#         "host12.dc2", 
#         "host09.dc2", 
#         "host07.dc2", 
#         "host01.dc2", 
#         "host08.dc2", 
#         "host02.dc2", 
#         "host03.dc2", 
#         "host05.dc2", 
#         "host00.dc2", 
#         "host04.dc2"
#     ]
# }
# salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:09.423175", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.341049", 
#         "arg": [
#             "role"
#         ], 
#         "fun": "grains.get", 
#         "jid": "20170211073107942342", 
#         "minions": [
#             "host06.dc2", 
#             "host13.dc2", 
#             "host10.dc2", 
#             "host11.dc2", 
#             "host12.dc2", 
#             "host09.dc2", 
#             "host07.dc2", 
#             "host01.dc2", 
#             "host08.dc2", 
#             "host02.dc2", 
#             "host03.dc2", 
#             "host05.dc2", 
#             "host00.dc2", 
#             "host04.dc2"
#         ], 
#         "tgt": "host*.dc1 or host*.dc2", 
#         "tgt_type": "compound", 
#         "user": "sudo_jettero"
#     }, 
#     "tag": "salt/job/20170211073107942342/new"
# }
# syndic/saltmaster.dc2/salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:09.423629", 
#     "arg": [
#         "role"
#     ], 
#     "fun": "grains.get", 
#     "jid": "20170211073107942342", 
#     "minions": [
#         "host06.dc2", 
#         "host13.dc2", 
#         "host10.dc2", 
#         "host11.dc2", 
#         "host12.dc2", 
#         "host09.dc2", 
#         "host07.dc2", 
#         "host01.dc2", 
#         "host08.dc2", 
#         "host02.dc2", 
#         "host03.dc2", 
#         "host05.dc2", 
#         "host00.dc2", 
#         "host04.dc2"
#     ], 
#     "tgt": "host*.dc1 or host*.dc2", 
#     "tgt_type": "compound", 
#     "user": "sudo_jettero"
# }
# 20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:09.456502", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.297019", 
#         "minions": []
#     }, 
#     "tag": "20170211073107942342"
# }
# syndic/saltmaster.dc4/20170211073107942342	{
#     "_stamp": "2017-02-11T15:31:09.456974", 
#     "minions": []
# }
# salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:09.457289", 
#     "data": {
#         "_stamp": "2017-02-11T15:31:08.297193", 
#         "arg": [
#             "role"
#         ], 
#         "fun": "grains.get", 
#         "jid": "20170211073107942342", 
#         "minions": [], 
#         "tgt": "host*.dc1 or host*.dc2", 
#         "tgt_type": "compound", 
#         "user": "sudo_jettero"
#     }, 
#     "tag": "salt/job/20170211073107942342/new"
# }
# syndic/saltmaster.dc4/salt/job/20170211073107942342/new	{
#     "_stamp": "2017-02-11T15:31:09.457660", 
#     "arg": [
#         "role"
#     ], 
#     "fun": "grains.get", 
#     "jid": "20170211073107942342", 
#     "minions": [], 
#     "tgt": "host*.dc1 or host*.dc2", 
#     "tgt_type": "compound", 
#     "user": "sudo_jettero"
# }
# salt/job/20170211073107942342/ret/host06.dc2	{
#     "_stamp": "2017-02-11T15:31:10.132189", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host06.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host13.dc2	{
#     "_stamp": "2017-02-11T15:31:10.134529", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host13.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host10.dc2	{
#     "_stamp": "2017-02-11T15:31:10.136938", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host10.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host11.dc2	{
#     "_stamp": "2017-02-11T15:31:10.139644", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host11.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host01.dc2	{
#     "_stamp": "2017-02-11T15:31:10.142688", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host01.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host04.dc2	{
#     "_stamp": "2017-02-11T15:31:10.145832", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host04.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host08.dc2	{
#     "_stamp": "2017-02-11T15:31:10.148256", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host08.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host12.dc2	{
#     "_stamp": "2017-02-11T15:31:10.150758", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host12.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host09.dc2	{
#     "_stamp": "2017-02-11T15:31:10.153952", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host09.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host02.dc2	{
#     "_stamp": "2017-02-11T15:31:10.157807", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host02.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host03.dc2	{
#     "_stamp": "2017-02-11T15:31:10.161189", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host03.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host05.dc2	{
#     "_stamp": "2017-02-11T15:31:10.164399", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host05.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host00.dc2	{
#     "_stamp": "2017-02-11T15:31:10.168359", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host00.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
# salt/job/20170211073107942342/ret/host07.dc2	{
#     "_stamp": "2017-02-11T15:31:10.173745", 
#     "fun": "grains.get", 
#     "fun_args": null, 
#     "id": "host07.dc2", 
#     "jid": "20170211073107942342", 
#     "return": "prod"
# }
