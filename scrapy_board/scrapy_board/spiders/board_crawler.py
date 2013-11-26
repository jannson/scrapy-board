import re
from scrapy_redis.spiders import RedisMixin

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy_board.items import ScrapyBoardItem
from scrapy_board.dupefilter import bloom_filter_add
import extract as tex

html_remove = re.compile(r'\s*<.*?>\s*',re.I|re.U|re.S)

class BoardCrawler(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'board_crawler'
    redis_key = 'boardcrawler:start_urls'

    rules = (
        # follow all links
        Rule(SgmlLinkExtractor(), callback='parse_page', follow=True),
    )

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse_page(self, response):
        url = response.url

        item = ScrapyBoardItem()
        item['url'] = url

        tx = tex.TextExtract(response.body)
        item['title'] = tx.title
        item['content'] = tx.content.strip()
        if tx.content != '':
            if len(html_remove.sub('', tx.preview)) < 250:
                item['preview'] = TextToHtml(tx.content)
            else:
                item['preview'] = tx.preview
            print 'add ', url
            bloom_filter_add(url)
            return item
