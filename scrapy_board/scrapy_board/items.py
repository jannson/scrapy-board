# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
from hashes.simhash import simhash as simhashpy
from simash import hash_token
from cppjiebapy import Tokenize
import extract as tex

from scrapy_board.dupefilter import bloom_filter_add
from scrapy.item import Item, Field

html_remove = re.compile(r'\s*<.*?>\s*',re.I|re.U|re.S)

class ScrapyBoardItem(Item):
    title = Field()
    url = Field()
    content = Field()
    preview = Field()
    hash = Field()
    tokens = Field()

def parse_response(response):
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
        #item['hash'] = long(simhashpy(item['tokens'], 64))
        item['hash'] = hash_token(item['tokens'])
        if len(html_remove.sub('', tx.preview)) < 250:
            item['preview'] = tex.TextToHtml(tx.content)
        else:
            item['preview'] = tx.preview
        #TODo for using bloom_filter
        #bloom_filter_add(url)
        return item
