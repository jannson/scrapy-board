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
