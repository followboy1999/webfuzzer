#encoding: utf-8
##codebyzzt
import datetime
from config import *
from PassParser import PassParser
from TomcatFuzz import FuzzEnginer1
from JbossFuzz import FuzzEnginer2
from WeblogicFuzz import FuzzEnginer3
from BesFuzz import FuzzEnginer4
from Axis2Fuzz import FuzzEnginer5

def start_brute(httpurl,webserver):
	start_time = datetime.datetime.now()
	#initailze dic and fuzz
	if webserver == 'tomcat':
		fuzz_tomcat = PassParser(tomcat_dict).parser()
		http_result,count = FuzzEnginer1(httpurl,fuzz_tomcat).start()
	elif webserver == 'jboss':
		fuzz_jboss = PassParser(jboss_dict).parser()
		http_result,count = FuzzEnginer2(httpurl,fuzz_tomcat).start()
	elif webserver == 'weblogic':
		fuzz_weblogic = PassParser(weblogic_dict).parser()
		http_result,count = FuzzEnginer3(httpurl,fuzz_weblogic).start()
	elif webserver == 'axis2':
		fuzz_axis2 = PassParser(axis2_dict).parser()
		http_result,count = FuzzEnginer5(httpurl,fuzz_axis2).start()
	else:#bes
		fuzz_bes = PassParser(bes_dict).parser()
		http_result,count = FuzzEnginer4(httpurl,fuzz_bes).start()

	stop_time = datetime.datetime.now()
	print "Try %d passwords " % count + "and run %s seconds" % (stop_time - start_time).seconds
	return http_result


