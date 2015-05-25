#!/usr/bin/env python
# coding: utf-8

import os

from Browser import Browser
from Utils import Logger

class PageSpider(object):
    
    def __init__(self, **args):
        pass
         
    def crawl(self, **args):
        url = args['url']
        br = Browser()
        return br.open(url, 0.9)
    
    def crawl_to_file(self, **args):
        url = args['url']
        path = args['path']
        filename = args['filename']
        with open(os.path.join(path, filename), 'w') as f:
            page = self.crawl(url=url)
            f.write(page)
