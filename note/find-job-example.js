
// salt host.dc1 saltutil.find_job 20170320113504719477

{
  "tag": "salt/job/20170320113601041969/new", 
  "data": {
    "tgt_type": "list", 
    "jid": "20170320113601041969", 
    "tgt": [
      "host.dc1"
    ], 
    "_stamp": "2017-03-20T15:36:01.043720", 
    "user": "sudo_jettero", 
    "arg": [
      "20170320113504719477"
    ], 
    "fun": "saltutil.find_job", 
    "minions": [
      "host.dc1"
    ]
  }, 
  "_evno": 25
}

// and the return (technically of a later query... don't compare the times)

{
  "tag": "salt/job/20170320113925697924/ret/host.dc1", 
  "data": {
    "fun_args": [
      "20170320113504719477"
    ], 
    "jid": "20170320113925697924", 
    "return": {}, 
    "retcode": 0, 
    "success": true, 
    "cmd": "_return", 
    "_stamp": "2017-03-20T15:39:26.152602", 
    "fun": "saltutil.find_job", 
    "id": "host.dc1"
  }, 
  "_evno": 2
}
