#!/usr/bin/env python
# coding: utf-8

from Browser import Browser
from PageParser import PageParser
import json

from Utils import DB, Logger

class LinkSpider(object):
    
    def __init__(self, **args):
        self.baseurl = args['baseurl']
        self.db = args['db']
        
    def crawl(self, **args):
        source = args['source']
        ext = args['ext']
        reply_time = args['reply_time']
        br = Browser()
        page = br.open(self.baseurl)
        new_reply_time = reply_time
        while True:
            links = PageParser.parse(page, source)
            for i, link in enumerate(links):
                if reply_time < link.reply_time:
                    if i is 0:
                        new_reply_time = link.reply_time
                    self.db.insert('\t'.join([str(link), source, json.dumps(ext)]))
                else:
                    return new_reply_time
            try:
                page = br.follow_link(text='后页>')
            except:
                Logger.info('finished!')
                break
        return new_reply_time
