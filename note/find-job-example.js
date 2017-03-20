
// salt host.dc1 saltutil.find_job 20170320113504719477

{
  "tag": "20170320122537669665", 
  "data": {
    "_stamp": "2017-03-20T16:25:37.669916", 
    "minions": [
      "host.dc1"
    ]
  }, 
  "_evno": 0
}

{
  "tag": "salt/job/20170320122537669665/new", 
  "data": {
    "tgt_type": "glob", 
    "jid": "20170320122537669665", 
    "tgt": "host.dc1", 
    "_stamp": "2017-03-20T16:25:37.670350", 
    "user": "sudo_jettero", 
    "arg": [
      "20170320113504719477"
    ], 
    "fun": "saltutil.find_job", 
    "minions": [
      "host.dc1"
    ]
  }, 
  "_evno": 1
}

{
  "tag": "salt/job/20170320122537669665/ret/host.dc1", 
  "data": {
    "fun_args": [
      "20170320113504719477"
    ], 
    "jid": "20170320122537669665", 
    "return": {}, 
    "retcode": 0, 
    "success": true, 
    "cmd": "_return", 
    "_stamp": "2017-03-20T16:25:38.057041", 
    "fun": "saltutil.find_job", 
    "id": "host.dc1"
  }, 
  "_evno": 2
}
