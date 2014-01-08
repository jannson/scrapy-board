#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import inspect

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import CrawlerSettings
from scrapy import log

from scrapy_board import settings
from scrapy_board.spiders.followall import FollowAllSpider
from plugins import SpiderPlugin

def import_plugins(name = 'plugins'):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(curr_dir, name)
    lst = os.listdir(path)
    insts = []

    for d in lst:
        s = os.path.join(path, d)
        if os.path.isfile(s) and d != "__init__.py" and s.endswith(".py"):
            py = d[:-3]
            mod = __import__("%s.%s" % (name, py), fromlist=[py])
            classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
            for cls in classes:
                if cls != SpiderPlugin and issubclass(cls, SpiderPlugin):
                    insts.append(cls())
    return insts

def setup_spider(inst):
    spider = FollowAllSpider(inst)
    crawler = Crawler(CrawlerSettings(settings))
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

insts = import_plugins()
for inst in insts:
    setup_spider(inst)

log.start()
reactor.run()

