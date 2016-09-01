from plog.channel.base import channel_base
from plog.channel.base import channel_base
import os
import time
import re

class channel(channel_base):

    def __init__(self,channel_dict,source_iter,sink_control):
        self.channel_dict=channel_dict
        self.source_iter=source_iter
        self.sink_control=sink_control
        self.interval=int(channel_dict['channel_interval'])
        self.kv=re.compile('(?P<key>"\w+?":"\S*?")') 
        self.threshold_login_nums=int(channel_dict['threshold_login_nums'])
        self.threshold_none_nums=int(channel_dict['threshold_none_nums'])
        self.threshold_login_rate=float(channel_dict['threshold_login_rate'])
        self.threshold_none_rate=float(channel_dict['threshold_none_rate'])
        self.result={"NONE":{}}
      
    
    def act(self):
        url=""
        while True:
            dt=self.source_iter.yield_line()
            for d in dt:
                #print d
                if d.has_key('url'):
                    url=d.get('url')
                elif d.has_key('paras'):
                    paras_dict=self.parse_paras(d.get('paras'))
                    if paras_dict.has_key('USR_ID') and url:
                        self.add_result({'uid':paras_dict['USR_ID'],'url':url})
                    elif url:
                        self.add_result({'uid':'','url':url})
                    url=""
            #self.print_result()
            #break
            time.sleep(self.interval)
     
    
    
    def parse_paras(self,paras):
        rs=self.kv.findall(paras)
        pdict={}
        if rs:
            for kv in rs:
                (k,v)=kv.split(':',1)
                pdict[k[1:-1]]=v[1:-1]
        return pdict
    
    def securecheck(self,key,url):
        numbers=self.result[key][url]
        total=float(self.result[key]['sum'])
        if key!="NONE" and numbers>self.threshold_login_nums:
            self.sink_control.deal_sink("%s %s number:%d have abnormal" %(key,url,numbers))
        elif numbers>self.threshold_none_nums:
            self.sink_control.deal_sink("%s %s number:%d have abnormal" %(key,url,numbers))

        if numbers>100:   
            if key!="NONE" and (numbers/total)>self.threshold_login_rate:
                self.sink_control.deal_sink("%s %s number:%d total:%f have abnormal" %(key,url,numbers,total))
            elif (numbers/total)>self.threshold_none_rate:
                self.sink_control.deal_sink("%s %s number:%d total:%f have abnormal" %(key,url,numbers,total))
        
    def add_result(self,value):
        if not value['uid']:
            value['uid']='NONE'
        if not self.result.get(value['uid']):
            self.result[value['uid']]={'sum':0}
       
        if self.result[value['uid']].get(value['url']):
            self.result[value['uid']][value['url']]+=1
            self.result[value['uid']]['sum']+=1
        else:
            self.result[value['uid']][value['url']]=1
            self.result[value['uid']]['sum']+=1
        self.securecheck(value['uid'],value['url'])
    
    def print_result(self):
        for uid,values in self.result.iteritems():
            for key,num in values.iteritems():
                print uid,key,num