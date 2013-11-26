# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ScrapyBoardItem(Item):
    title = Field()
    url = Field()
    content = Field()
    preview = Field()
    hash = Field()
    tokens = Field()
