# -*- coding: utf-8 -*-
import sys, os
import json
import redis

#django_path = os.path.dirname(os.path.abspath(__file__))
django_path = '/home/gan/project/source/testgit/Similar'
sys.path.insert(13, django_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'pull.settings'

from django.db.models import Count
from django.db.models import Q
from pull.models import *
def main():
    r = redis.Redis()
    while True:
        # process queue as FIFO, change `blpop` to `brpop` to process as LIFO
        source, data = r.blpop(["board_crawler:items"])
        item = json.loads(data)
        try:
            url = item['url']
            try:
                html = ScrapyContent.objects.get(url=url)
            except:
                html = ScrapyContent(url=url)

            html.title = item['title']
            html.content = item['content']
            html.preview = item['preview']
            html.hash = item['hash']
            html.save()

        except:
            print u"Error procesing: %r" % item['url']


if __name__ == '__main__':
    main()
