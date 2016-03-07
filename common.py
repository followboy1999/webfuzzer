# encoding: utf-8
# 全局函数文件
# codebyzzt

from config import *
import re
import lib.requests as requests
import lib.requests as __requests__

if allow_http_session:
	requests = requests.Session()

def http_request_get(url,body_content_workflow=False, allow_redirects=allow_redirects):
	try:
		result = requests.get(url,
			stream=body_content_workflow, 
			headers=headers, 
			timeout=timeout, 
			proxies=proxies,
			allow_redirects=allow_redirects,
			verify=allow_ssl_verify)
		return result
	except Exception, e:
		# 返回空的requests结果对象
		return __requests__.models.Response()

def http_request_get0(url,headers,body_content_workflow=False, allow_redirects=allow_redirects):
	try:
		result = requests.get(url, 
			stream=body_content_workflow, 
			headers=headers, 
			timeout=timeout, 
			proxies=proxies,
			allow_redirects=allow_redirects,
			verify=allow_ssl_verify)
		return result
	except Exception, e:
		# 返回空的requests结果对象
		return __requests__.models.Response()

def http_request_get1(url,payload,body_content_workflow=False, allow_redirects=allow_redirects):
	try:
		result = requests.get(url, 
			params = payload,
			stream=body_content_workflow, 
			headers=headers, 
			timeout=timeout, 
			proxies=proxies,
			allow_redirects=allow_redirects,
			verify=allow_ssl_verify)
		return result
	except Exception, e:
		# 返回空的requests结果对象
		return __requests__.models.Response()

def http_request_post(url, payload, body_content_workflow=False, allow_redirects=allow_redirects):
	"""
		payload = {'key1': 'value1', 'key2': 'value2'}
	"""
	try:
		result = requests.post(url, 
			data=payload, 
			headers=headers, 
			stream=body_content_workflow, 
			timeout=timeout, 
			proxies=proxies,
			allow_redirects=allow_redirects,
			verify=allow_ssl_verify)
		return result
	except Exception, e:
		# 返回空的requests结果对象
		return __requests__.models.Response()

def checksite_isalive(siteurl):
	result = http_request_get(siteurl, allow_redirects=False)
	regex = re.compile(page_not_found_reg)
	if regex.findall(result.text):
		return False
	else:
		return True
	'''
	if result.status_code in exclude_status: # 存在状态码
		return True
	else:
		return False
	'''