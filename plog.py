from plog import run
from optparse import OptionParser
import os,sys
import signal

def signal_handler(sig, frame):
    pid=os.getpid()
    os.kill(pid, signal.SIGQUIT)

if __name__ == "__main__":


    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = OptionParser() 
    parser.add_option("-c", "--config", dest="config_filename",
                            help="config file for parse log")
    parser.add_option("-s", "--source", dest="source_file",
                                help="source file from log")    
    (options, args) = parser.parse_args()
    
    
    if options.config_filename is None :
        print "config  file is none"
        sys.exit(1)
    else :
        try:
            if not os.path.exists(sys.path[0]+'/conf/'+options.config_filename):
                print "there is not config file:%s,you should creat_cfg first,refer to https://github.com/CNSRE/Plog" %config_filename
                sys.exit(1)
            else:
                config_file = sys.path[0]+'/conf/'+options.config_filename
        except:
            print "read config error,check it exists or not,refer to https://github.com/CNSRE/Plog"
            sys.exit(1)

    run(config_file = config_file, options=options ,args=args,debug=False)
