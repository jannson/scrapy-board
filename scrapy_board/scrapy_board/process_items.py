#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re
import json
import redis
import zerorpc
import traceback

from simhash import hash_token
from cppjiebapy import Tokenize

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

CORPUS_LEN = 512

def load_hashes(hashm):
    for obj in HtmlContent.objects.filter(status__lte=2).filter(~Q(content='')):
        hashm.insert(obj.hash)

def find_duplicate(hashm, hash):
    sims = hashm.find_first(hash)
    return sims[0][1]

def get_title(title):
    return re.split(r'[-_|]', title)[0]

def main():
    hashm = zerorpc.Client('tcp://yaha.v-find.com:5678')
    #load_hashes(hashm)
    sim_server = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))
    sim_server.set_autosession(True)
    r = redis.Redis()
    corpus = []

    while True:
        try:
            # process queue as FIFO, change `blpop` to `brpop` to process as LIFO
            source, data = r.blpop(["groud_crawler:items", "board_crawler:items"], timeout=20)
        except KeyboardInterrupt:
            print 'Exit'
            break
        except:
            #print 'No blpop', len(corpus)
            if len(corpus) > 0:
                #sim_server.set_autosession(False)
                #sim_server.open_session()
                sim_server.index(corpus)
                sim_server.commit()
                #sim_server.set_autosession(True)
                corpus = []
            continue
        try:
            item = json.loads(data)
        except:
            print 'Load json error'
            continue
        url = item['url']
        try:
            html = HtmlContent.objects.get(url=url)
            #Ignore the exists item, TODO use bloomfilter to ignore
            if html.status != 2:
                continue
        except:
            html = HtmlContent(url=url)
        try:
            tokens = [s for s in Tokenize(item['content'])]
            html.title = item['title']
            html.hash = hash_token(tokens)
            if HtmlContent.objects.filter(hash=html.hash).filter(status__gt=2).count() > 0:
                #Already exists
                html.status = 5
                html.save()
                continue
            html.content = item['content']
            html.tags,html.summerize = summarize(html.content)
            html.summerize = html.summerize[0:399]
            html.preview = item['preview']

            if find_duplicate(hashm, html.hash) != 0:
                #Mark as duplicate
                html.status = 1
            else:
                html.status = 0

            html.save()
            hashm.insert(html.hash)
            if html.status == 0:
                corpus.append({'id':'html_%d' % html.id, 'tokens': tokens})
                #print 'Append corpus', len(corpus), corpus[-1]['id']
                if len(corpus) >= CORPUS_LEN:
                    #sim_server.set_autosession(False)
                    #sim_server.open_session()
                    sim_server.index(corpus)
                    sim_server.commit()
                    #sim_server.set_autosession(True)
                    corpus = []

            #print 'Saved url %s' % html.url
        except:
            tb = traceback.format_exc()
            print 'Load json error', html.url, tb

if __name__ == '__main__':
    main()
