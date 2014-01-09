#coding:utf-8
from . import SpiderPlugin
from scrapy import log

class AiWeiBang(SpiderPlugin):
    name = 'aiweibang'
    domains = ['aiweibang.com',]
    start_urls = ['http://www.aiweibang.com/',]
    rules = [r'/yuedu/([^/]+)/(\d+)\.html$',]

    def __init__(self):
        return super(AiWeiBang, self).__init__()

    def parse(self, response):
        return super(AiWeiBang, self).parse(response)


#The others
class CyzOrgCn(SpiderPlugin):
    name = 'cyz_org_cn'
    domains = ['cyz.org.cn',]
    start_urls = ['http://www.cyz.org.cn/',]
    rules = [r'/(\d+)/(\d+)/(\d+)\.html$',]

class HuXiu(SpiderPlugin):
    name = 'huxiu_com'
    domains = ['huxiu.com',]
    start_urls = ['http://www.huxiu.com/',]
    rules = [r'/article/(\d+)/(\d+)\.html$',]

class CNetNews(SpiderPlugin):
    name = 'cnetnewsn_com_cn'
    domains = ['cnetnews.com.cn',]
    start_urls = ['http://www.cnetnews.com.cn/',]
    rules = [r'/(\d+)/(\d+)/(\d+)\.shtml',]

class CnBeta(SpiderPlugin):
    name = 'cnbeta_com'
    domains = ['cnbeta.com',]
    start_urls = ['http://www.cnbeta.com',]
    rules = [r'/articles/(\d+).htm',]

'''
class IFeng(SpiderPlugin):
    name = 'ifeng_com'
    domains = ['ifeng.com',]
    start_urls = ['http://www.ifeng.com/',]
    rules = [r'/(\w+/)+detail[A-Za-z0-9_]+\.shtml/',]
'''
