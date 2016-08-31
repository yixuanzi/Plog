from plog.channel.base import channel_base
from plog.channel.base import channel_base
import os
import time
import re

class channel(channel_base):

    def __init__(self,channel_dict,source_iter):
        self.channel_dict=channel_dict
        self.source_iter=source_iter
        self.interval=int(channel_dict['channel_interval'])
        self.kv=re.compile('(?P<key>"\S+?":"\S*?")')
        self.result={"NONE":{}}
      
    
    def act(self):
        url=""
        while True:
            dt=self.source_iter.yield_line()
            for d in dt:
                print d
                if d.has_key('url'):
                    url=d.get('url')
                elif d.has_key('paras'):
                    paras_dict=self.parse_paras(d.get('paras'))
                    if paras_dict.has_key('USR_ID') and url:
                        self.add_result({'uid':paras_dict['USR_ID'],'url':url})
                    elif url:
                        self.add_result({'uid':'','url':url})
                    url=""
            time.sleep(self.interval)
     
    
    
    def parse_paras(self,paras):
        rs=self.kv.findall(paras)
        pdict={}
        if rs:
            for kv in rs:
                (k,v)=kv.split(':')
                pdict[k[1:-1]]=v[1:-1]
        return pdict
    
    def securecheck(self):
        for key,value in result.iteritems():
            total=float()
            for url,numbers in value.iteritems():
                if key!="NONE" and numbers>threshold_login_nums:
                    mywaring("%s %s number:%d have abnormal" %(key,url,numbers))
                elif numbers>threshold_none_nums:
                    mywaring("%s %s number:%d have abnormal" %(key,url,numbers))
                total+=numbers
                
            if total>100:
                for url,numbers in value.iteritems():
                    if key!="NONE" and (numbers/total)>threshold_login_rate:
                        mywaring("%s %s number:%d total:%f have abnormal" %(key,url,numbers,total))
                    elif (numbers/total)>threshold_none_rate:
                        mywaring("%s %s number:%d total:%f have abnormal" %(key,url,numbers,total))    
      
    def add_result(self,value):
        if not value['uid']:
            value['uid']='NONE'
        if not self.result.get(value['uid']):
            self.result[value['uid']]={}
       
        if self.result[value['uid']].get(value['url']):
            self.result[value['uid']][value['url']]+=1
        else:
            self.result[value['uid']][value['url']]=1