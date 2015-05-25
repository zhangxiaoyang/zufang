#!/usr/bin/env python
# coding: utf-8

import time
import os
import datetime
import json
import sys

import simhash
from simhash import Simhash, SimhashIndex

from Utils import Logger, DB, backup

def sim_merge(finaldb_cut, simdb):
    d = {}
    index_list = []
    hashurl2sim = {}
    max_distance = 10
    with open(finaldb_cut, 'r') as f:
        for line in f:
            if not line:
                break
            # hashurl  title  author  images  links  text  pub_time
            # 1        2      3       4       5      6     7
            # jushi  shouji  zujin  dizhi  ditie  url  crawl_time  source  ext
            # 8      9       10     11     12     13   14          15      16
            array = line.rstrip('\r\n').split('\t')
            hashurl=array[0]     #string,key
            title=array[1]       #string
            text=array[5]        #string
            pub_time=array[6]    #string 
            url=array[12]        #string 

            s = Simhash((title+text).decode('utf-8'))
            d.update({
                hashurl:(title, url, pub_time)
            })
            sim = Simhash((title+text).decode('utf-8'))
            index_list.append((hashurl, sim))
            hashurl2sim.update({hashurl:sim})

    index = SimhashIndex(index_list, k=max_distance)
    merged = {}
    while d:
        hashurl, (title, url, pub_time) = d.popitem()
        merged[hashurl] = (title, url, pub_time)
        sim_list = index.get_near_dups(hashurl2sim[hashurl])
        buf_list = []
        for h in sim_list:
            if h != hashurl:
                if d.has_key(h):
                    title2, url2, pub_time2 = d.pop(h)
                    merged[h] = (title2, url2, pub_time2)
                else:
                    title2, url2, pub_time2 = merged[h]
            else:
                title2, url2, pub_time2 = title, url, pub_time
            buf_list.append((h, title2, url2, pub_time2))
        if len(buf_list) > 1:
            buf_list = sorted(buf_list, key=lambda i:i[3], reverse=True)
            simdb.insert('\t'.join(
                [buf_list[0][0], json.dumps(buf_list[1:])]
            ))
     
def main(**args):
    modulepath = args['modulepath']
    finaldb_cut = os.path.join(modulepath, '../output/final.db.2')
    simdb = os.path.join(modulepath, '../output/sim.db')
    if os.path.exists(simdb):
        backup(simdb)
        os.remove(simdb)
    sim_merge(finaldb_cut, DB(simdb))

if __name__ == '__main__':
    starttime = datetime.datetime.now()   
    run = sys.argv[0]
    modulepath = os.path.dirname(run)
    main(
        modulepath=modulepath
    )
    endtime = datetime.datetime.now()   
    Logger.info('done! %lds' % (endtime-starttime).seconds)
