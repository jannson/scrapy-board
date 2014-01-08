#coding:utf-8

from scrapy_board.items import parse_response

class SpiderPlugin(object):
    def __init__(self):
        pass

    def __str__(self):
        return ''.join(self.domains)

    #TODO implement exeption and attributes?
    def get_domains(self):
        return self.domains

    def get_rules(self):
        return self.rules

    def get_start_urls(self):
        return self.start_urls

    def parse(self, response):
        return parse_response(response)
