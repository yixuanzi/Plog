from plog.sink.base import sink_base
import os
import time

class sink(sink_base):
    def __init__(self, sink_dict):
        pass
        #self.service = sink_dict['sink_service']
  
    def deal_sink(self,result):
        for uid,dt in result.items():
            for url,nums in dt.items():
                print uid,'\t',url,'\t',nums
