Aria with python front
---
A front end written in python to control remote aria

### Support
- [x] websoket rpc
- [x] http-post rpc
- [x] user specified aria options

### Install

Requirement  
`pip install websoket`

Help  
`python aria.py -h`

### Quick Start

change the download path in ```ariafpy.json```  
1. Download file to `~/Downloads` by http  
`python aria.py -u http://example/file -a dir ~/Downloads`  
Or by torrent file  
`python aria.py -t path/to/torrent/file`  
2. Save download profile  
`python aria.py -s profile.json -u http://example/file -a dir ~/Downloads`  
3. Load download profile  
`python aria.py -p profile.json`  

### Configuration

Config file for remote aria : ```ariafpy.json```

the ***options*** keyword in config file is the default aria options to control the aria
