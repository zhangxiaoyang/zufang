#!/usr/bin/env python
# coding: utf-8

import time
import os
import datetime
import sys

from PageSpider import PageSpider
from Utils import Logger, DB

def diff_task(linkdb, output, pagelist):
    page_filenames = []
    #trick :)
    if os.path.exists(pagelist):
        Logger.info('Use pagelist indead of page files!')
        with open(pagelist, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    break
                filename = line
                page_filenames.append(filename)
    else:
        Logger.info('CANNOT find pagelist file: %s' % pagelist)

    tasks = {}
    sources = []
    with open(linkdb, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    hashurl, url, reply_time, source = line.split('\t')[:4]
                except: continue
                filename = '%s' % (hashurl)
                tasks.update({
                    filename:{
                        'url':url,
                        'source':source
                    }
                })
                sources.append(source)

    if not pagelist:
        for source in set(sources):
            source = os.path.join(output, source)
            if os.path.exists(source):
                filenames = os.listdir(source)
                for filename in filenames:
                    tasks.pop(filename) 
            else:
                os.mkdir(source)
    else:
        for source in set(sources):
            source = os.path.join(output, source)
            if not os.path.exists(source):
                os.mkdir(source)
        for filename in page_filenames:
            try:
                tasks.pop(filename) 
            except:
                print 'Skip', filename
    return tasks

def main(**args):
    modulepath = args['modulepath']
    linkdb = os.path.join(modulepath, '../data/link.db')
    path = os.path.join(modulepath, '../output/')
    pagelist = os.path.join(path, 'pagelist')

    pagespider = PageSpider()
    tasks = diff_task(linkdb, path, pagelist)

    db_pagelist = DB(pagelist)
    for filename in tasks:
        pagespider.crawl_to_file(
            url=tasks[filename]['url'],
            path=os.path.join(path, tasks[filename]['source']),
            filename=filename
        )
        db_pagelist.insert(filename)

if __name__ == '__main__':
    starttime = datetime.datetime.now()   
    run = sys.argv[0]
    modulepath = os.path.dirname(run)
    main(
        modulepath=modulepath
    )
    endtime = datetime.datetime.now()   
    Logger.info('done! %lds' % (endtime-starttime).seconds)
