import re
from hashes.simhash import simhash as simhashpy
from cppjiebapy import Tokenize

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
    allowed_domains = ['36kr.com','aiweibang.com','cyz.org.cn','huxiu.com','zhihu.com']
    start_urls = ['http://www.36kr.com', 
            'http://www.aiweibang.com',
            'http://www.cyz.org.cn',
            'http://www.huxiu.com',
            'http://www.zhihu.com']

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
        body = response.body
        if not isinstance(body, unicode):
            try:
                body = body.decode('utf-8')
            except:
                body = body.decode('gbk', 'ignore').encode('utf-8', 'replace').decode('utf-8')

        item = ScrapyBoardItem()
        item['url'] = url

        tx = tex.TextExtract(body)
        item['title'] = tx.title
        item['content'] = tx.content.strip()
        if tx.content != '':
            item['tokens'] = list(Tokenize(tx.content))
            item['hash'] = long(simhashpy(item['tokens'], 64))
            if len(html_remove.sub('', tx.preview)) < 250:
                item['preview'] = tex.TextToHtml(tx.content)
            else:
                item['preview'] = tx.preview
            bloom_filter_add(url)
            return item
