#!/usr/bin/env python
#encoding: utf-8
#codebyzzt

import sys
import json
import lib.requests as requests
#import lib.requests as requests
from HttpBrute import start_brute

if __name__ == "__main__":
    if len(sys.argv) == 3 :
        print json.dumps(start_brute(sys.argv[1],sys.argv[2]), indent=2)
        sys.exit(0)

    elif len(sys.argv) == 4:
        print json.dumps(start_brute(sys.argv[1],sys.argv[2]), indent=2)
        sys.exit(0)
    else:
        print ("web server brute, support by tomcat(include other Basic Authorization) jboss weblogic axis2 bes")
        print ("usage: %s http://example.org:9090/ tomcat /manager/html(optional)" % sys.argv[0])
        sys.exit(-1)
