from scrapy_redis.spiders import RedisMixin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import CloseSpider

from scrapy_board.items import ScrapyBoardItem, parse_response

class BoardCrawler(CrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'board_crawler'
    max_count = 0
    # TODO more domains from database
    allowed_domains = ['36kr.com','aiweibang.com','cyz.org.cn','huxiu.com','ifeng.com','cnetnews.com.cn']
    start_urls = ['http://www.36kr.com', 
            'http://www.aiweibang.com',
            'http://www.cyz.org.cn',
            'http://www.huxiu.com',
            'http://www.ifeng.com/',
            'http://www.cnetnews.com.cn/',
            ]

    #redis_key = 'boardcrawler:start_urls'

    rules = (
        # follow all links
        Rule(SgmlLinkExtractor(), callback='parse_page', follow=True),
    )

    #def set_crawler(self, crawler):
    #    CrawlSpider.set_crawler(self, crawler)
    #    RedisMixin.setup_redis(self)

    def parse_page(self, response):
        self.max_count += 1
        #crawl max_count page per date
        if self.max_count > 5000:
            raise CloseSpider('url_exceeded')
        return parse_response(response)
