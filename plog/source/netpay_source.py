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
        self.filter_regex=re.compile(source_dict['source_regex'].decode('utf8'))
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
            try:
                line=line.decode('utf8')
            except Exception:
                line="DEBUG: Codeing Error"
            if not line:
                continue
            m=self.filter_regex.match(line)
            if m:
                yield m.groupdict()

                    

