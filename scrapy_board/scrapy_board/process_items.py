#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import json
import redis
import zerorpc
import traceback

import gensim
from gensim import models, corpora, similarities, matutils
from gensim.corpora import Dictionary

import Pyro4
from simserver import SessionServer

#django_path = os.path.dirname(os.path.abspath(__file__))
#django_path = '/home/gan/project/source/testgit/Similar'
django_path = '/opt/projects/git_source/Similar'
sys.path.insert(13, django_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'pull.settings'

from django.db.models import Count
from django.db.models import Q
from pull.models import *
from pull.summ import summarize

import logging

logging.basicConfig(level=logging.ERROR)

def find_duplicate(hashm, hash):
    sims = hashm.find_first(hash)
    return sims[0][1]

def main():
    hashm = zerorpc.Client('tcp://yaha.v-find.com:5678')
    #sim_server = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))
    r = redis.Redis()
    corpus = []

    while True:
        # process queue as FIFO, change `blpop` to `brpop` to process as LIFO
        source, data = r.blpop(["groud_crawler:items", "board_crawler:items"])
        try:
            item = json.loads(data)
        except:
            print 'Load json error'
            continue
        url = item['url']
        try:
            html = HtmlContent.objects.get(url=url)
            #Ignore the exists item, TODO use bloomfilter to ignore
            if html.content !='' and html.status <= 1:
                continue
        except:
            html = HtmlContent(url=url)
        try:
            html.title = item['title']
            html.content = item['content']
            html.tags,html.summerize = summarize(html.content)
            html.summerize = html.summerize[0:399]
            html.preview = item['preview']
            html.hash = item['hash']

            if find_duplicate(hashm, item['hash']) != 0:
                html.status = 1
            else:
                html.status = 0

            html.save()
            hashm.insert(html.hash)

            '''
            corpus.append({'id':'html_%d' % html.id, 'tokens': item['tokens']})
            if len(corpus) >= 256:
                sim_server.index(corpus)
                corpus = []
            '''
            #print 'Saved url %s' % html.url
        except:
            tb = traceback.format_exc()
            print 'Load json error', html.url, tb

if __name__ == '__main__':
    main()
