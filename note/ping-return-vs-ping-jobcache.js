
// actual return event
{
  "tag": "salt/job/20170311175224317476/ret/blah.dc1", 
  "data": {
    "fun_args": [], 
    "jid": "20170311175224317476", 
    "return": true, 
    "retcode": 0, 
    "success": true, 
    "cmd": "_return", 
    "_stamp": "2017-03-11T22:52:24.420542", 
    "fun": "test.ping", 
    "id": "blah.dc1"
  },
  "_evno": 16
},

// load = get_load(jid)
// with load['ret'] = get_jid(jid)
{
  "tgt_type": "glob", 
  "jid": "20170311175224317476", 
  "tgt": "blah.dc1", 
  "cmd": "publish", 
  "ret": {
    "blah.dc1": {
      "return": true
    }
  }, 
  "to": 30, 
  "user": "sudo_jettero", 
  "_evno": 2, 
  "kwargs": {
    "delimiter": ":", 
    "show_timeout": true, 
    "show_jid": true
  }, 
  "fun": "test.ping", 
  "arg": [], 
  "Minions": [
    "blah.dc1"
  ]
}

// salt-run jobs.print_job 20170311175224317476 --out=json
{
    "20170311175224317476": {
        "Function": "test.ping", 
        "Result": {
            "blah.dc1": {
                "return": true
            }
        }, 
        "Target": "blah.dc1", 
        "Target-type": "glob", 
        "User": "sudo_jettero", 
        "StartTime": "2017, Mar 11 17:52:24.317476", 
        "Minions": [
            "blah.dc1"
        ], 
        "Arguments": []
    }
}
