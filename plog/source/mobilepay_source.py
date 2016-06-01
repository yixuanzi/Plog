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
        
    def getlogs(self):
        fs=os.listdir(self.source_file)
        for f in fs:
            if os.path.isfile(self.source_file+'/'+f) and re.match('(\d+\.){3}\d+',f):
                yield self.source_file+'/'+f
                
    def yield_line(self):
        for f in self.getlogs():
            fr=open(f)
            while True:
                line=fr.readline().decode('utf8')
                if not line:
                    break
                if line[32:41]==u'\u5ba2\u6237\u7aef\u8bf7\u6c42\u53c2\u6570\u5982\u4e0b':
                    url=line[58:-1]
                    line=fr.readline().decode('utf8')
                    if not line:
                        break            
                    if line[32]=='{':
                        args=line[32:-1]
                    else:
                        args="NOTSESSION"
                    try:
                        yield url,args
                    except Exception:
                        yield url,args.encode('utf8')       
                    

