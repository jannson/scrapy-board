
from scrapy.utils.misc import load_object
from scrapy_redis.scheduler import Scheduler
from scrapy_board.dupefilter import RFPDupeFilter


class BloomScheduler(Scheduler):
    def open(self, spider):
        self.spider = spider
        self.queue = self.queue_cls(self.server, spider, self.queue_key)
        self.df = RFPDupeFilter(self.server, self.dupefilter_key % {'spider': spider.name})
        if self.idle_before_close < 0:
            self.idle_before_close = 0
        # notice if there are requests already in the queue to resume the crawl
        if len(self.queue):
            spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))
