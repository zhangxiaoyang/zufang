#!/usr/bin/env python
# coding: utf-8

import time
import os
import datetime
import sys

from HouseRefinery import HouseRefinery
from Utils import Logger, DB, backup

def diff_task(taskfile, donefile):
    alltask = []
    donetask = []
    with open(taskfile, 'r') as f:
        for line in f:
            if not line:
                break
            hashurl = line.split('\t')[0]
            alltask.append(hashurl)
    with open(donefile, 'r') as f:
        for line in f:
            if not line:
                break
            hashurl = line.split('\t')[0]
            donetask.append(hashurl)
    
    exclude = set(donetask)
    return [task for task in alltask if task not in exclude]

def process(contentdb, housedb):
    hr = HouseRefinery(
        db=DB(housedb)
    )
    hashurls = diff_task(contentdb, housedb)
    with open(contentdb, 'r') as f:
        for line in f:
            if not line:
                break
            hashurl, title, _, _, _, text = line.split('\t')[:6]
            if hashurl in hashurls:
                hr.parse(
                    hashurl=hashurl,
                    title=title,
                    text=text
                )
                hashurls.remove(hashurl)

def main(**args):
    modulepath = args['modulepath']
    contentdb = os.path.join(modulepath, '../data/content.db')
    housedb = os.path.join(modulepath, '../output/house.db')
    backup(housedb)
    process(contentdb, housedb)

if __name__ == '__main__':
    starttime = datetime.datetime.now()   
    run = sys.argv[0]
    modulepath = os.path.dirname(run)
    main(
        modulepath=modulepath
    )
    endtime = datetime.datetime.now()   
    Logger.info('done! %lds' % (endtime-starttime).seconds)
