#!/usr/bin/env python
# coding: utf-8

import time
import os
import datetime
import sys

from ContentExtractor import ContentExtractor
from Utils import Logger, DB, backup

def diff_task(alltask, donefile):
    donetask = []
    with open(donefile, 'r') as f:
        for line in f:
            if not line:
                break
            hashurl = line.split('\t')[0]
            donetask.append(hashurl)

    exclude = set(donetask)
    return [task for task in alltask if task not in exclude]

def process(pagedirs, contentdb):
    sources = os.listdir(pagedirs)
    ce = ContentExtractor(
        db=DB(contentdb)
    )
    for source in sources:
        sourcedir = os.path.join(pagedirs, source)
        if not os.path.isdir(sourcedir):
            continue
        pagenames = os.listdir(sourcedir)
        pagenames = diff_task(pagenames, contentdb)
        for pagename in pagenames:
            hashurl = pagename
            pagename = os.path.join(sourcedir, pagename)
            with open(pagename, 'r') as f:
                ce.parse(
                    page=f.read(),
                    source=source,
                    hashurl=hashurl
                )

def main(**args):
    modulepath = args['modulepath']
    pagedirs = os.path.join(modulepath, '../data/')
    contentdb = os.path.join(modulepath, '../output/content.db')
    backup(contentdb)
    process(pagedirs, contentdb)

if __name__ == '__main__':
    starttime = datetime.datetime.now()   
    run = sys.argv[0]
    modulepath = os.path.dirname(run)
    main(
        modulepath=modulepath
    )
    endtime = datetime.datetime.now()   
    Logger.info('done! %lds' % (endtime-starttime).seconds)
