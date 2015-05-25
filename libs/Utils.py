#!/usr/bin/env python
# coding: utf-8

import time
import json
import re
import shutil
import os

def backup(filename):
    newfile = filename+'.bak'
    if os.path.exists(filename):
        if os.path.isfile(filename):
            try: os.remove(newfile)
            except: pass
            shutil.copy(filename, newfile)
        elif os.path.isdir(filename):
            try: shutil.rmtree(newfile) 
            except: pass
            shutil.copytree(filename, newfile)

class Logger:
    
    @staticmethod
    def warn(msg):
        status = 'WARN'
        Logger.printf(msg, status)
 
    @staticmethod
    def error(msg):
        status = 'ERROR'
        Logger.printf(msg, status)

    @staticmethod
    def info(msg):
        status = 'INFO'
        Logger.printf(msg, status)

    @staticmethod
    def printf(msg, status):
        print '[%s] %s %s' % (
            status,
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            msg
        )

class Link(object):
    hashurl = ''
    url     = ''
    reply_time = 0

    def __init__(self, **args):
        self.hashurl = args['hashurl']
        self.url = args['url']
        self.reply_time = args['reply_time']

    def __str__(self):
        return '\t'.join([
            self.hashurl,
            self.url,
            str(self.reply_time)
        ])
            

class DB(object):
    _dbstream = None
    _NEWLINE = '\n'

    def __init__(self, dbname):
        if type(dbname) == str:
            self.dbname = dbname
            self._dbstream = open(dbname, 'a', 0)
        elif type(dbname) == DB:
            db = dbname
            self.dbname = db.dbname
            self._dbstream = open(db.dbname, 'r')

    def __del__(self):
        self._dbstream.close()

    def insert(self, record):
        self._dbstream.write(record+self._NEWLINE)

    def fetchone(self):
        line = self._dbstream.readline()
        return re.sub(self._NEWLINE+'$', '', line)

class Meta(object):
    _meta = {}

    def __init__(self, metaname):
        self.metaname = metaname
        self.load(metaname)

    def load(self, metaname):
        try:
            with open(metaname, 'r') as f:
                data = json.loads(f.read())
                if type(data) == dict and len(data) > 0:
                    self._meta = data
                    return True
        except:
            return False

    def set(self, *argv):
        self._meta[':'.join(argv[:-1])] = argv[-1]

    def get(self, *argv):
        key = ':'.join(argv)
        try:
            return self._meta[key]
        except:
            return None

    def has(self, *argv):
        key = ':'.join(argv)
        if self._meta.has_key(key):
            return True
        else:
            return False

    def write(self, metaname=None):
        if not metaname:
            metaname = self.metaname
        with open(metaname, 'w', 0) as f:
            f.write(json.dumps(self._meta))
