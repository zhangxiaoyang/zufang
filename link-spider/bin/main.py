#!/usr/bin/env python
# coding: utf-8

import time
import os
import datetime
import json
import sys

from LinkSpider import LinkSpider
from Utils import Logger, DB, Meta, backup

def run_linkspider(db, meta):
    source = 'douban'
    baseurls = [
        'http://www.douban.com/group/beijingzufang/discussion',
        'http://www.douban.com/group/fangzi/discussion',
        'http://www.douban.com/group/262626/discussion',
        'http://www.douban.com/group/276176/discussion',
        'http://www.douban.com/group/26926/discussion',
        'http://www.douban.com/group/sweethome/discussion',
        'http://www.douban.com/group/242806/discussion',
        'http://www.douban.com/group/257523/discussion',
        'http://www.douban.com/group/279962/discussion',
        'http://www.douban.com/group/334449/discussion',
    ]

    for baseurl in baseurls:
        Logger.info('start '+baseurl)        
        groupid = baseurl\
            .replace('http://www.douban.com/group/', '')\
            .replace('/discussion', '')
        reply_time = 0
        if meta.has(source, groupid)\
            and meta.get(source, groupid).has_key('reply_time'):
            reply_time = meta.get(source, groupid)['reply_time']
        linkspider = LinkSpider(
            baseurl=baseurl,
            db=db,
        )
        reply_time = linkspider.crawl(
            source=source,
            reply_time=reply_time,
            ext={
                'groupid':groupid
            }
        )
        meta.set(source, groupid, {
            'reply_time':reply_time
        })
    meta.write()

def main(**args):
    modulepath = args['modulepath']
    linkdb = os.path.join(modulepath, '../output/link.db')
    backup(linkdb)

    linkmeta = os.path.join(modulepath, '../output/link.meta')
    backup(linkmeta)
    run_linkspider(DB(linkdb), Meta(linkmeta))

if __name__ == '__main__':
    starttime = datetime.datetime.now()   
    run = sys.argv[0]
    modulepath = os.path.dirname(run)
    main(
        modulepath=modulepath
    )
    endtime = datetime.datetime.now()   
    Logger.info('done! %lds' % (endtime-starttime).seconds)
