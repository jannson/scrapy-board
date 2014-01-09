from urlparse import urlparse
from scrapy.http import Request, HtmlResponse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy import log

class FollowAllSpider(CrawlSpider):

    name = 'followall'
    max_count = 0

    def __init__(self, inst, craw_max=2000):
        self.plugin = inst
        #self.name = inst.name or 'followall'
        self.allowed_domains = inst.get_domains()
        self.start_urls = inst.get_start_urls()
        self.rules = tuple([Rule(SgmlLinkExtractor(rule), callback='parse_page', follow=True) for rule in inst.get_rules()])
        self.craw_max = craw_max
        print self.start_urls, self.allowed_domains
        super(FollowAllSpider, self).__init__(domain=inst.get_domains())

    def parse_page(self, response):
        #log.msg('test hear', level=log.ERROR)

        item = self.plugin.parse(response)
        
        if item:
            self.max_count += 1

            #crawl limit page per date
            if self.max_count > self.craw_max:
                raise CloseSpider('page exceeded')

        return item
