from scrapy_redis.spiders import RedisMixin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy_redis import connection
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.http import Request

from scrapy_board.items import ScrapyBoardItem, parse_response

from pull.models import *

def parse_error(response):
    try:
        url = response.meta['origin_url']
    except:
        url = response.url
    try:
        html = HtmlContent.objects.get(url=url)
        html.status = 3
    except:
        pass

class GroudCrawler(RedisMixin, CrawlSpider):
    name = 'groud_crawler'

    redis_key = 'groud_crawler:start_urls'
    handle_httpstatus_list = [404]

    rules = (
        Rule(SgmlLinkExtractor(), callback='parse_page', follow=False),
    )

    def setup_redis(self):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if not self.redis_key:
            self.redis_key = '%s:start_urls' % self.name

        self.server = connection.from_settings(self.crawler.settings)
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        self.log("Reading URLs from redis list '%s'" % self.redis_key)

    def next_request(self):
        """Returns a request to be scheduled or none."""
        url = self.server.lpop(self.redis_key)
        if url:
            #return self.make_requests_from_url(url)
            return Request(url, callback='parse_page', dont_filter=True, meta={'origin_url':url})

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        req = self.next_request()
        if req:
            self.crawler.engine.crawl(req, spider=self)
        raise DontCloseSpider

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        self.setup_redis()

    def parse_page(self, response):
        item = parse_response(response)
        if item:
            try:
                item['url'] = response.meta['origin_url']
            except:
                pass
            return item
        else:
            parse_error(response)

    def process_exception(self, response, exception, spider):
        parse_error(response)

    def parse(self, response):
        if response.status == 404:
            parse_error(response)
