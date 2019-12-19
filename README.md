# RESTCONF-routing
This script runs a series of RESTCONF requests (using aiohttp) and produces a summary of the routing table in telegraf format.

## Installing
Clone this repository and creeate a virtual environment.  Note aiohttp requires python3.6 or greater.

```buildoutcfg
python3.6 -m venv env3
source env3/bin/activate
```
Then install the aiohttp module
```buildoutcfg
pip install -r requirements.txt
```

You then need to copy the samp-config.py file to config.py and edit it to update the username, password, and list 
of devices you want to monitor.

```buildoutcfg
USERNAME="user"
PASSWORD="pass"
DEVICES = ["10.10.10.10", "10.10.10.20"]
```

you can then run the script to test
````buildoutcfg
./async.py 
[{"ospfv2": 13, "direct": 7, "lisp": 2, "vrf": "default", "table": "ietf-routing:ipv4", "device": "10.10.10.10"}, 
{"direct": 1, "vrf": "default", "table": "ietf-routing:ipv6", "device": "10.10.10.10"}, 
{"static": 1, "direct": 2, "vrf": "Mgmt-vrf", "table": "ietf-routing:ipv4", "device": "10.10.10.10"}, 
{"direct": 1, "vrf": "Mgmt-vrf", "table": "ietf-routing:ipv6", "device": "10.10.10.10"}, 
{"direct": 2, "vrf": "Things", "table": "ietf-routing:ipv4", "device": "10..10.10.10"}, 
{"direct": 2, "vrf": "Guest", "table": "ietf-routing:ipv4", "device": "10..10.10.10"}, 
{"direct": 2, "lisp": 2, "vrf": "Enterprise", "table": "ietf-routing:ipv4", "device": "10..10.10.10"}, 
{"direct": 2, "vrf": "__Platform_iVRF:_ID00_", "table": "ietf-routing:ipv4", "device": "10..10.10.10"}, 
{"static": 1, "direct": 3, "vrf": "default", "table": "ietf-routing:ipv4", "device": "10..10.10.20"}, 
{"direct": 1, "vrf": "default", "table": "ietf-routing:ipv6", "device": "10..10.10.20"}, 
{"static": 1, "direct": 2, "vrf": "Mgmt-vrf", "table": "ietf-routing:ipv4", "device": "10..10.10.20"}, 
{"direct": 1, "vrf": "Mgmt-vrf", "table": "ietf-routing:ipv6", "device": "10..10.10.20"}, 
{"direct": 2, "vrf": "__Platform_iVRF:_ID00_", "table": "ietf-routing:ipv4", "device": "10..10.10.20"}, 
]
```

## Telegraf config

This is the config file for telegraf to run the script.  Notice the timeout has been extended from the default.
I have also defined device, vrf and table as tags
```
[[inputs.exec]]
 command = "/opt/git-repos/async/env3/bin/python /opt/git-repos/async/async.py"
 data_format = "json"
timeout = "100s"
 tag_keys = ["device", "vrf", "table"]
 name_suffix = "_route_metric"
 interval = "3m"