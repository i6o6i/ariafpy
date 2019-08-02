import urllib.request
import base64
import asyncio
import websockets
import json
import argparse
from pprint import pprint


class ariafrontpy:
    def __init__(self,path):
        self.afp={}
        with open(path,'r') as afpconfig:
            self.afp=json.load(afpconfig)
        self.options=self.afp['defaultoptions'][0]

    def addtask(self,method,uri,options):
        for (key,value) in options:
            self.options[key]=value
        pprint(self.options)
        self.parse_json(method,uri,self.options)
        pprint(self.jsondata)
        if self.afp['rpcaddr'].split('://')[0] == 'ws':
            asyncio.get_event_loop().run_until_complete(self.sendviaws(self.jsondata))
        elif self.afp['rpcaddr'].split('://')[0] == 'http': 
            self.sendviapost(self.jsondata)
        print('complete addtask')

    def parse_json(self,method,uri,options):
        """
        the param uri might be uri or torrent file path
        :param options: aria options
        :type options: object
        """
        token=self.afp['token']
        dljson={'json':'2.0','id':'whatisidfor'}
        if method == "torrent":
            dljson['method']='aria2.addTorrent'
            dljson['params']=['token:'+token,base64.b64encode(open(uri).read()) ,options]
        elif method == "uris":
            dljson['method']='aria2.addUri'
            dljson['params']=['token:'+token,uri,options]
        self.jsondata=json.dumps(dljson).encode('utf-8')

    async def sendviaws(self,jsondata):
        rpcaddr=self.afp['rpcaddr']
        async with websockets.connect(rpcaddr) as ws:
            await ws.send(jsondata)
    def sendviapost(self,jsondata):
        rpcaddr=self.afp['rpcaddr']
        req=urllib.request.Request(rpcaddr)
        req.add_header('Content-Type', 'application/json;charset=utf-8')
        req.add_header('Content-Length',len(jsondata))
        print(jsondata)
        res=urllib.request.urlopen(req,jsondata)
        res.read()

def main():
    parser=argparse.ArgumentParser(description="python aria front")
    parser.add_argument('-t','--type',help="download via torrent file path or uris",choices=['torrent','uris','t','u'],default='u',type=str)
    parser.add_argument('-c','--conf',help="config file for ariafpy",nargs=1,default='./ariafpy.json',type=str)
    parser.add_argument('-u','--uris',metavar='torrent or uris',help="uris of file you want to download",nargs='+',type=str)
    parser.add_argument('-a','--options',help="aria options",default={},nargs=argparse.REMAINDER)
    args=parser.parse_args()
    print(args)
    options={}
    it=iter(args.options)
    for i in it:
        options[i]=next(i)

    ariafpy=ariafrontpy(args.conf)
    if args.type[0] == 'u':
        ariafpy.addtask('uris',args.uris,options)
    elif args.type[0] == 't':
        ariafpy.addtask('torrent',args.uris,options)

if __name__ == "__main__":
    main()
