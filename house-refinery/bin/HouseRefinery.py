#!/usr/bin/env python
# coding: utf-8

from TextParser import TextParser
from Utils import Logger, DB

class HouseRefinery(object):
    
    def __init__(self, **args):
        self._db = args['db']

    def parse(self, **args):
        hashurl = args['hashurl']
        title = args['title']
        text = args['text']
        ret = TextParser.parse(title+' '+text)
        if ret.has_key('error'):
            Logger.info(hashurl+' '+ret['error'])
            return
        record = '\t'.join([
            hashurl,
            title,
            text,
            ret['jushi'],
            ret['shouji'],
            ret['zujin'],
            ret['dizhi'],
            ret['ditie'],
        ])
        self._db.insert(record)
