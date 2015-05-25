#!/usr/bin/env python
# coding: utf-8

from PageParser import PageParser
from Utils import Logger, DB
import json

class ContentExtractor(object):
    
    def __init__(self, **args):
        self._db = args['db']

    def parse(self, **args):
        page = args['page']
        source = args['source']
        hashurl = args['hashurl']
        ret = PageParser.parse(page, source)
        if ret.has_key('error'):
            Logger.info(hashurl+' '+ret['error'])
            return
        record = '\t'.join([
            hashurl,
            ret['title2'] if ret['title2']\
                else ret['title'],
            json.dumps(ret['author']),
            json.dumps(ret['images']),
            json.dumps(ret['links']),
            ret['text'],
            ret['pub_time'],
        ]).encode('utf-8')
        self._db.insert(record)
