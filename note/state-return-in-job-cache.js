// salt-run jobs.print_job 20170311185217297069 --out=json
{
    "20170311185217297069": {
        "Function": "state.sls", 
        "Result": {
            "blah.dc1": {
                "return": {
                    "file_|-/etc/dhcpcd.conf_|-/etc/dhcpcd.conf_|-append": {
                        "comment": "File /etc/dhcpcd.conf is in correct state", 
                        "pchanges": {}, 
                        "name": "/etc/dhcpcd.conf", 
                        "start_time": "18:52:20.100654", 
                        "result": true, 
                        "duration": 328.362, 
                        "__run_num__": 1, 
                        "changes": {}, 
                        "__id__": "/etc/dhcpcd.conf"
                    }, 
                    "cmd_|-fuck-you-resolv-conf_|-rm -v /etc/resolv.conf_|-run": {
                        "comment": "onlyif execution failed", 
                        "name": "rm -v /etc/resolv.conf", 
                        "start_time": "18:52:20.451205", 
                        "skip_watch": true, 
                        "__id__": "fuck-you-resolv-conf", 
                        "duration": 5.088, 
                        "__run_num__": 6, 
                        "changes": {}, 
                        "result": true
                    }, 
                    "file_|-/etc/dhcp/dhclient.conf_|-/etc/dhcp/dhclient.conf_|-managed": {
                        "comment": "File /etc/dhcp/dhclient.conf is in the correct state", 
                        "pchanges": {}, 
                        "name": "/etc/dhcp/dhclient.conf", 
                        "start_time": "18:52:20.430400", 
                        "result": true, 
                        "duration": 13.306, 
                        "__run_num__": 3, 
                        "changes": {}, 
                        "__id__": "/etc/dhcp/dhclient.conf"
                    }, 
                    "pkg_|-resolvconf_|-resolvconf_|-purged": {
                        "comment": "All specified packages are already absent", 
                        "name": "resolvconf", 
                        "start_time": "18:52:20.052271", 
                        "result": true, 
                        "duration": 46.003, 
                        "__run_num__": 0, 
                        "changes": {}, 
                        "__id__": "resolvconf"
                    }, 
                    "module_|-/etc/dhcp/dhclient.conf_|-service.restart_|-wait": {
                        "comment": "", 
                        "name": "service.restart", 
                        "start_time": "18:52:20.444425", 
                        "result": true, 
                        "duration": 0.586, 
                        "__run_num__": 4, 
                        "changes": {}, 
                        "__id__": "/etc/dhcp/dhclient.conf"
                    }, 
                    "file_|-/etc/resolv.conf_|-/etc/resolv.conf_|-managed": {
                        "comment": "File /etc/resolv.conf is in the correct state", 
                        "pchanges": {}, 
                        "name": "/etc/resolv.conf", 
                        "start_time": "18:52:20.456837", 
                        "result": true, 
                        "duration": 1.257, 
                        "__run_num__": 7, 
                        "changes": {}, 
                        "__id__": "/etc/resolv.conf"
                    }, 
                    "module_|-/etc/dhcpcd.conf_|-service.restart_|-wait": {
                        "comment": "", 
                        "name": "service.restart", 
                        "start_time": "18:52:20.429576", 
                        "result": true, 
                        "duration": 0.624, 
                        "__run_num__": 2, 
                        "changes": {}, 
                        "__id__": "/etc/dhcpcd.conf"
                    }, 
                    "cmd_|-remove-resolv-conf-chattr_|-chattr -i /etc/resolv.conf_|-run": {
                        "comment": "onlyif execution failed", 
                        "name": "chattr -i /etc/resolv.conf", 
                        "start_time": "18:52:20.445183", 
                        "skip_watch": true, 
                        "__id__": "remove-resolv-conf-chattr", 
                        "duration": 5.809, 
                        "__run_num__": 5, 
                        "changes": {}, 
                        "result": true
                    }
                }, 
                "out": "highstate"
            }
        }, 
        "Target": "blah.dc1", 
        "Target-type": "glob", 
        "User": "sudo_jettero", 
        "StartTime": "2017, Mar 11 18:52:17.297069", 
        "Minions": [
            "blah.dc1"
        ], 
        "Arguments": [
            "resolv.conf"
        ]
    }
}
