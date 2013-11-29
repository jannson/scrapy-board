from scrapy_redis.spiders import RedisMixin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy_board.items import ScrapyBoardItem, parse_response

class BoardCrawler(CrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'board_crawler'
    # TODO more domains from database
    allowed_domains = ['36kr.com','aiweibang.com','cyz.org.cn','huxiu.com','zhihu.com']
    start_urls = ['http://www.36kr.com', 
            'http://www.aiweibang.com',
            'http://www.cyz.org.cn',
            'http://www.huxiu.com',
            'http://www.zhihu.com']

    #redis_key = 'boardcrawler:start_urls'

    rules = (
        # follow all links
        Rule(SgmlLinkExtractor(), callback='parse_page', follow=True),
    )

    #def set_crawler(self, crawler):
    #    CrawlSpider.set_crawler(self, crawler)
    #    RedisMixin.setup_redis(self)

    def parse_page(self, response):
        return parse_response(response)
