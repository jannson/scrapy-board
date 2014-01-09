#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import inspect

import signal

from twisted.internet import reactor, defer

from scrapy.resolver import CachingThreadedResolver
from scrapy.utils.ossignal import install_shutdown_handlers, signal_names
from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.settings import CrawlerSettings

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

class CrawlerProcess(object):
    """ A class to run multiple scrapy crawlers in a process sequentially"""

    def __init__(self, settings):
        install_shutdown_handlers(self._signal_shutdown)
        self.settings = settings
        self.crawlers = {}
        self.plugins = {}
        self.stopping = False
        self._started = None

    def from_plugins(self, insts):
        for inst in insts:
            if inst.name and inst.name not in self.crawlers:
                self.crawlers[inst.name] = Crawler(self.settings)
                self.plugins[inst.name] = inst

    def start(self):
        if self.start_crawling():
            self.start_reactor()

    @defer.inlineCallbacks
    def stop(self):
        self.stopping = True
        if self._active_crawler:
            yield self._active_crawler.stop()

    def _signal_shutdown(self, signum, _):
        install_shutdown_handlers(self._signal_kill)
        signame = signal_names[signum]
        log.msg(format="Received %(signame)s, shutting down gracefully. Send again to force ",
                                level=log.INFO, signame=signame)
        reactor.callFromThread(self.stop)

    def _signal_kill(self, signum, _):
        install_shutdown_handlers(signal.SIG_IGN)
        signame = signal_names[signum]
        log.msg(format='Received %(signame)s twice, forcing unclean shutdown',
                                level=log.INFO, signame=signame)
        reactor.callFromThread(self._stop_reactor)

    # ------------------------------------------------------------------------#
    # The following public methods can't be considered stable and may change at
    # any moment.
    #
    # start_crawling and start_reactor are called from scrapy.commands.shell
    # They are splitted because reactor is started on a different thread than IPython shell.
    #
    def start_crawling(self):
        log.scrapy_info(self.settings)
        return self._start_crawler() is not None

    def start_reactor(self):
        if self.settings.getbool('DNSCACHE_ENABLED'):
                                reactor.installResolver(CachingThreadedResolver(reactor))
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False)  # blocking call

    def _start_crawler(self):
        if not self.crawlers or self.stopping:
            return

        name, crawler = self.crawlers.popitem()
        self._active_crawler = crawler
        sflo = log.start_from_crawler(crawler)
        spider = FollowAllSpider(self.plugins[name])
        crawler.configure()
        crawler.crawl(spider)
        crawler.install()
        crawler.signals.connect(crawler.uninstall, signals.engine_stopped)
        if sflo:
            crawler.signals.connect(sflo.stop, signals.engine_stopped)
        crawler.signals.connect(self._check_done, signals.engine_stopped)
        crawler.start()
        return name, crawler

    def _check_done(self, **kwargs):
        if not self._start_crawler():
            self._stop_reactor()

    def _stop_reactor(self, _=None):
        try:
            reactor.stop()
        except RuntimeError:  # raised if already stopped or in shutdown stage
            pass

def setup_spider(inst):
    spider = FollowAllSpider(inst)
    crawler = Crawler(CrawlerSettings(settings))
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

insts = import_plugins()
crawler_process = CrawlerProcess(CrawlerSettings(settings))
crawler_process.from_plugins(insts)
crawler_process.start()

#for inst in insts:
#    setup_spider(inst)
#log.start()
#reactor.run()

