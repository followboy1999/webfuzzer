#encoding: utf-8
#传递一个queue队列，判断是否该队列内URL的HTTP请求状态，是否符合config内定义的exclude_status状态码
#email: ringzero@0x557.org
#some code hacked 
import sys
from config import *
import threading
import Queue
import re

class FuzzEnginer2(object):
	"""docstring for FuzzEnginer"""
	def __init__(self, url,passwords):
		super(FuzzEnginer2, self).__init__()
		self.url = url
		self.passwords = passwords

	class FuzzWorker(threading.Thread):
		def __init__(self, queue):
			threading.Thread.__init__(self)
			self.queue = queue

		def run(self):
			while True:
				if self.queue.empty():
					break
				try: # 用hack方法，no_timeout读取Queue队列，直接异常退出线程避免阻塞
					url = self.queue.get_nowait()
					results = http_request_get(url)
					# print "[%s] %s => %s" % (results.status_code, url, results.url) # 客户端调试信息
					if results.status_code in exclude_status:
						print "[%s] %s => %s" % (results.status_code, url, results.url) # 客户端调试信息
						# 加入是否为备份文件结尾判断
						if results.headers.get('content-length'): # 存在content-length属性
							is_redirect = True if len(results.history) > 0 else False
							if not is_redirect: # 未发生url跳转
								# 如果返回了content-length属性，同时大小<100KB，加入404错误定义检测 1000 = 1k, 100kb = 100000
								if int(results.headers.get('content-length')) < 20000:
									regex = re.compile(page_not_found_reg)
									if not regex.findall(results.text): # print '找到错误定义，成功返回404信息'
										resources[results.status_code][url] = {'is_redirect':is_redirect,'history':results.history,'request':results.url}
						else:
							is_redirect = True if len(results.history) > 0 else False
							resources[results.status_code][url] = {'is_redirect':is_redirect,'history':results.history,'request':results.url}
				except Exception, e: # 队列阻塞
					# print e
					break

	def start(self):

		global resources
		resources = {}

		queue = Queue.Queue()
		for password in self.passwords: # 生成任务队列
			queue.put(password)
		for status_code in exclude_status: # 初始化全局状态码数据
			resources[status_code] = {}
		threads = [] # 初始化线程组
		for i in xrange(threads_count):
			threads.append(self.FuzzWorker(queue))
		for t in threads: # 启动线程
			t.start()
		for t in threads: # 等待线程执行结束后，回到主线程中
			t.join()
		return resources

