#!/usr/bin/env python
# coding: utf-8

import mechanize
import cookielib
import urllib2
import time
import random

from Utils import Logger

class NoHistory(object):
    def add(self, *a, **k):pass
    def clear(self):pass

class Interval:
    _interval = 0
    @staticmethod
    def val():
        Interval._interval += 1
        if Interval._interval*Interval._interval > 1000:
            return 1000
        else:
            return Interval._interval*Interval._interval
    @staticmethod
    def reset():
        Interval._interval = 0

class Agent:
    _agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0'
    ]
    @staticmethod
    def random_agent():
        return random.choice(Agent._agents)

class Browser(object):
    _interval = 1
    def __init__(self, **args):
        if args.has_key('history') and args['history']:
            self.br = mechanize.Browser()
        else:
            self.br = mechanize.Browser(history=NoHistory())
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.set_cookiejar(mechanize.CookieJar())
        self.br.addheaders = [(
            'User-Agent',
            #'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
            Agent.random_agent()
        )]

    def open(self, url, delay=0.1):
        response = None
        try:
            response = self.br.open(url, timeout=20.0)
        except urllib2.HTTPError, e:
            while e.code != 404:
                interval = Interval.val()
                time.sleep(interval)
                Logger.info('sleep %ds error %d %s' % (interval, e.code, url))
                try:
                    response = self.br.open(url, timeout=20.0)
                    Logger.info('skip 403 ' + url)
                    break
                except urllib2.HTTPError, e:
                    if e.code != 404:
                        continue
                except:
                    Logger.info('cannot handle browser error!')
                    break
            Interval.reset()
        except:
            pass
        time.sleep(delay)
        if response:
            page = response.read()
        else:
            page = ''
        return page

    def close(self):
        return self.br.close()

    def follow_link(self, **args):
        text = args['text']
        return self.br.follow_link(text=text)
