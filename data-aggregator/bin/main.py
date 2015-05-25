#!/usr/bin/env python
# coding: utf-8

import time
import os
import datetime
import json
import sys

from Utils import Logger, DB, backup

def gen_house(finaldb_cut, jsondb, simdb):
    reject_list = []
    sim = {}
    with open(simdb, 'r') as f:
        for line in f:
            if not line:
                break
            array = line.rstrip('\r\n').split('\t')
            hashurl, json_objects = array[0], json.loads(array[1])
            sim[hashurl] = json_objects
            reject_list += [i[0] for i in json_objects]
    reject_list = set(reject_list)
            
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
            author=json.loads(array[2])     #json
            images=json.loads(array[3])      #json
            links=json.loads(array[4])       #json
            text=array[5]        #string
            pub_time=array[6]    #datetime
            jushi=array[7]       #string
            shouji=array[8]      #string
            zujin=array[9]       #string
            dizhi=array[10]      #string
            ditie=array[11]      #string
            url=array[12]        #string 
            crawl_time=array[13] #string
            source=array[14]     #string
            ext=array[15]        #json

            if hashurl in reject_list:
                reject_list.remove(hashurl)
                print 'skip', hashurl
                continue #skip

            new_line = {
                "hashurl": hashurl,
                "title": title,
                "author": author,
                "images": images,
                "links": links,
                "text": text,
                "pub_time": pub_time,
                "jushi": jushi,
                "shouji": shouji,
                "zujin": zujin,
                "dizhi": dizhi,
                "ditie": ditie,
                "url": url,
                "crawl_time": crawl_time,
                "source": source,
                "ext": ext,
                "sim": sim[hashurl] if sim.has_key(hashurl) else [],
            }
            jsondb.insert(json.dumps(new_line))

def main(**args):
    modulepath = args['modulepath']
    finaldb_cut = os.path.join(modulepath, '../output/final.db.2')
    jsondb_house = os.path.join(modulepath, '../output/zufang.house.json')
    simdb = os.path.join(modulepath, '../output/sim.db')
    if os.path.exists(jsondb_house):
        backup(jsondb_house)
        os.remove(jsondb_house)
    gen_house(finaldb_cut, DB(jsondb_house), simdb)

if __name__ == '__main__':
    starttime = datetime.datetime.now()   
    run = sys.argv[0]
    modulepath = os.path.dirname(run)
    main(
        modulepath=modulepath
    )
    endtime = datetime.datetime.now()   
    Logger.info('done! %lds' % (endtime-starttime).seconds)
