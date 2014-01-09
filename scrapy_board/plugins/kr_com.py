#coding:utf-8
from . import SpiderPlugin

class Kr36Com(SpiderPlugin):
    name = 'kr36_com'
    domains = ['36kr.com',]
    start_urls = ['http://www.36kr.com',]
    #rules = [r'/(p|topics)/(\d+)\.html',]
    rules = [r'/([^/]+)/(\d+)\.html$',]

    def __init__(self):
        return super(Kr36Com, self).__init__()

    def parse(self, response):
        return super(Kr36Com, self).parse(response)
