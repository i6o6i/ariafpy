import urllib.request
import base64
import asyncio
import websockets
import json
import argparse

class ariafrontpy:
    def __init__(self,path):
        self.afp={}
        with open(path,'r') as afpconfig:
            self.afp=json.load(afpconfig)
        self.options=self.afp['options'][0]

    def addtask(self,method,uri,options):
        for key,value in options.items():
            self.options[key]=value
        self.parse_json(method,uri,self.options)
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
    parser.add_argument('-m','--method',
            help="download via torrent file path or uris",default='u',
            choices=['torrent','uris','t','u'],type=str)
    parser.add_argument('-s','--save',
            help="save current profile of a task",
            nargs='?',const='./profile.json',
            metavar='profile path',type=str)
    parser.add_argument('-c','--conf',help="config file for ariafpy",
            metavar='config file path',nargs=1,type=str,
            default='./ariafpy.json')
    parser.add_argument('-p','--profile',nargs='?',type=str,
            help="task profile used to store info of a task",
            const='./profile.json')
    parser.add_argument('-u','--uris',metavar='torrent or uris',
            nargs='+',type=str,
            help="uris of file you want to download",)
    parser.add_argument('-a','--options',help="aria options",
            default={},nargs=argparse.REMAINDER)
    args=parser.parse_args()

    ariafpy=ariafrontpy(args.conf)
    if args.profile == None:
        method= 'uris'if args.method[0] == 'u' else 'torrent'
        uris=args.uris
        options={}
        it=iter(args.options)
        for i in it:
            options[i]=next(it)
        ariafpy.addtask(method,uris,options)
        if args.save != None:
            ajson={'method':method,'uris':uris,
                    'options':[options]}
            with open(args.save,'w') as afile:
                json.dump(ajson,afile,indent=4)
    else:
        with open(args.profile, 'r') as afile:
            profile=json.load(afile)
        ariafpy.addtask(profile['method'],profile['uris'],
                profile['options'][0])

if __name__ == "__main__":
    main()
