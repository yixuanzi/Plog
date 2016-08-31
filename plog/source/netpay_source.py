from plog.source.base import source_base
from plog.source.base import source_base
import os
import time
import sys
import re

class source(source_base):

    def __init__(self, source_dict):
        self.source_interval = int(source_dict["source_interval"])
        self.source_file = source_dict["source_file"]
        self.file_inode = 0
        self.fp=None
        self.ree=re.compile(source_dict['source_regex'])
                            
    def getlogs(self):
        if self.fp:
            for l in self.fp:
                yield l.decode('utf8')
        else:
            self.fp=open(self.source_file)
            for l in self.fp:
                yield l.decode('utf8')


    def yield_line(self):
        for line in self.getlogs():
            m=self.ree.match(line)
            if m:
                rs=m.groupdict()
                yield {'uid':rs['uid'],'utp':rs['utp'],'url':rs['url']}
                
       
                    

