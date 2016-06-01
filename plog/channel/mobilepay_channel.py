from plog.channel.base import channel_base
from plog.channel.base import channel_base
import os
import time
import re

class channel(channel_base):

    def __init__(self,channel_dict,source_iter,dict_queue):
        self.channel_dict=channel_dict
        self.source_iter=source_iter
        self.dict_queue= dict_queue
        self.dts={"NONE":{}}
      
    
    def parse_line(self):
        #"data":\{.*?\}
        
        for url,args in self.source_iter:
            self.actargs(url,args)
        return self.dts

    def actargs(self,url,args):
        dt=self.parseargs(args)
        if dt and dt.get('USRID'):
            if not self.dts.get(dt['USRID']):
                self.dts[dt['USRID']]={}
            usr=self.dts[dt['USRID']]
            if usr.get(url):
                usr[url]+=1
            else:
                usr[url]=1
        else:
            usr=self.dts["NONE"]
            if usr.get(url):
                usr[url]+=1
            else:
                usr[url]=1            
                           
            
    def parseargs(self,args):
        m=re.search(r'"data":(\{.*?\})',args)
        if m:
            ss=m.groups()[0]
            dt=eval(ss)
            return dt

    def filterargs(self,args):
        pass
        
        
