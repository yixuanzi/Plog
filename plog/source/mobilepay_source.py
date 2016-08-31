from plog.source.base import source_base
from plog.source.base import source_base
import os
import time
import sys
import re

class source(source_base):

    def __init__(self, source_dict):
        self.source_file = source_dict["source_file"]
        #self.file_inode = 0
        self.filter_url=re.compile(source_dict['source_filter_url'].decode('gbk'))
        self.filter_paras=re.compile(source_dict['source_filter_paras'].decode('gbk'))
        self.fp=None
        
    def getlineiter(self):
        #fs=os.listdir(self.source_file)
        if not self.fp:
            self.fp=open(self.source_file)
            return self.fp
        else:
            return self.fp.readlines()
            
    def yield_line(self):
        for line in self.getlineiter():
            line=line.decode('utf8')
            if not line:
                continue
            m=self.filter_url.match(line)
            if m:
                yield m.groupdict()
                continue
            m=self.filter_paras.match(line)
            if m: 
                yield m.groupdict()

                    

