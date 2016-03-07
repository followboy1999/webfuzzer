#edcoding: utf-8
#referer to  http://github.com/ring04h/weakfilescan 

import sys
import random

# 字典来自文件列表
tomcat_dict = './dict/tomcat.lst'
jboss_dict = './dict/jboss.lst'
weblogic_dict = './dict/weblogic.lst'
bes_dict = './dict/bes.lst'
axis2_dict = './dict/axis2.lst'

#uri参数
tomcat_uri = "/manager/html"
jboss_uri = ""
weblogic_uri = "/console/j_security_check"
bes_uri = "/console/j_security_check"
axis2_uri = "/axis2/axis2-admin/login"

# 判断文件或目录存在的状态码，多个以逗号隔开
# exclude_status = [200,403]
exclude_status = [200,401,403]
success_status = [200]
redirect_status = [302]

# 判断文件是否存在正则，如果页面存在如下定义的内容，将url从结果中剔除
page_not_found_reg = r'404|[nN]ot [fF]ound|不存在|未找到|Error'

# 是否开启https服务器的证书校验
allow_ssl_verify = False


# 线程数
threads_count = 20

# -------------------------------------------------
# requests 配置项
# -------------------------------------------------

# 超时时间
timeout = 10

payload = ""

# 是否允许URL重定向
#allow_redirects = True
allow_redirects = False

# 是否允许继承http Request类的Session支持，在发出的所有请求之间保持cookies。
allow_http_session = True

# 是否允许随机User-Agent
allow_random_useragent = True

# 是否允许随机X-Forwarded-For
allow_random_x_forward = True

# 代理配置
proxies = {
}

# 随机HTTP头
USER_AGENTS = [
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# 随机生成User-Agent
def random_useragent(condition=False):
	if condition:
		return random.choice(USER_AGENTS)
	else:
		return USER_AGENTS[0]

# 随机X-Forwarded-For，动态IP
def random_x_forwarded_for(condition=False):
	if condition:
		return '%d.%d.%d.%d' % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254))
	else:
		return '8.8.8.8'


# HTTP 头设置
if 'tomcat' not in sys.argv:
	headers = {
		'User-Agent': random_useragent(allow_random_useragent),
		'X_FORWARDED_FOR': random_x_forwarded_for(allow_random_x_forward),
		# 'Referer' : 'http://www.google.com',
		# 'Cookie': 'whoami=wyscan_dirfuzz',
	}


