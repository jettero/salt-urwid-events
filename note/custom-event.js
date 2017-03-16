
// eg: salt-call event.send tag='shit/post' data='{blah: true}'

{
  "tag": "shit/post", 
  "data": {
    "_stamp": "2017-03-16T14:58:55.393940", 
    "cmd": "_minion_event", 
    "data": {
      "__pub_fun": "event.send", 
      "__pub_jid": "20170316105855385995", 
      "__pub_pid": 12454, 
      "__pub_tgt": "salt-call",
      "blah": true
    }, 
    "id": "blarg.host",
    "tag": "shit/post"
  }, 
  "_evno": 31
}
