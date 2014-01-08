#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re

import json
import redis

def main():
    r = redis.Redis()

    while True:
        try:
            # process queue as FIFO, change `blpop` to `brpop` to process as LIFO
            source, data = r.blpop(["groud_crawler:items", "followall:items"], timeout=20)
        except KeyboardInterrupt:
            print 'Exit'
            break
        except:
            print 'Timeout'
            continue
        try:
            #print source, type(data)
            item = json.loads(data)
            print 'Process url %s' % item['url']
        except:
            tb = traceback.format_exc()
            print 'Load json error', html.url, tb

if __name__ == '__main__':
    main()
