#!/usr/bin/python
#-*-coding:utf-8-*-

import os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

#django_path = os.path.dirname(os.path.abspath(__file__))
#django_path = '/home/gan/project/source/testgit/Similar'
django_path = '/opt/projects/git_source/Similar'
sys.path.insert(13, django_path)

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'scrapy_board'

SPIDER_MODULES = ['scrapy_board.spiders']
NEWSPIDER_MODULE = 'scrapy_board.spiders'

COOKIES_ENABLED = False
RETRY_ENABLED = False
#DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 15
REDIRECT_ENABLED = False
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 32
#CONCURRENT_REQUESTS = 100
#The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0
DEPTH_LIMIT = 6
DEPTH_PRIORITY = 1
DNSCACHE_ENABLED = True

USER_AGENT = ''
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy_board.downloadmiddleware.rotate_useragent.RotateUserAgentMiddleware':400,
}

ITEM_PIPELINES = [
    'scrapy_redis.pipelines.RedisPipeline',
]

LOG_LEVEL = 'ERROR'
#LOG_FILE = "logs/scrapy.log"

#DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
#SCHEDULER = 'scrapy.core.scheduler.Scheduler'
#DUPEFILTER_CLASS = 'scrapy_board.duperfilter.RFPDupeFilter'
SCHEDULER = "scrapy_board.scheduler.BloomScheduler"
SCHEDULER_PERSIST = False
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

os.environ['DJANGO_SETTINGS_MODULE'] = 'pull.settings'
