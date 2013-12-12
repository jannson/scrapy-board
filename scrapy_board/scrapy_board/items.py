# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
import extract as tex

from scrapy_board.dupefilter import bloom_filter_add
from scrapy.item import Item, Field

html_remove = re.compile(r'\s*<.*?>\s*',re.I|re.U|re.S)

class ScrapyBoardItem(Item):
    title = Field()
    url = Field()
    content = Field()
    preview = Field()

def parse_response(response):
    url = response.url
    body = response.body
    #For redis error

    if not isinstance(body, unicode):
        try:
            body = body.decode('utf-8')
        except:
            body = body.decode('gbk', 'ignore').encode('utf-8', 'replace').decode('utf-8')

    #if isinstance(body, unicode):
    #    body = body.encode('utf-8', 'replace')

    item = ScrapyBoardItem()
    item['url'] = url

    tx = tex.TextExtract(body)
    item['title'] = tx.title
    item['content'] = tx.content.strip()
    if tx.content != '':
        if len(html_remove.sub('', tx.preview)) < 250:
            item['preview'] = tex.TextToHtml(tx.content)
        else:
            item['preview'] = tx.preview
        #TODo for using bloom_filter
        #bloom_filter_add(url)
        return item
    else:
        return None
