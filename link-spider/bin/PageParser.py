#!/usr/bin/env python
# coding: utf-8

from BeautifulSoup import BeautifulSoup
import time
import hashlib

from Utils import Link, Logger

class PageParser:
    
    @staticmethod
    def parse(page, source):
        return {
            'douban':PageParser._parse_douban,
            'shuimu':PageParser._parse_shuimu,
            'ganji':PageParser._parse_ganji,
            'soufun':PageParser._parse_soufun,
            '58':PageParser._parse_58,
        }[source](page)


    @staticmethod
    def _clean(soup):
        new_list = []
        for i in soup:
            if str(i).strip():
                new_list.append(i)
        return new_list

    @staticmethod
    def _parse_douban(page):
        soup = BeautifulSoup(page)
        ret = []
        try:
            table = soup.findAll('table', {'class':'olt'})[0]
            '''
            nexturl = soup.findAll('div', {'class':'paginator'})[0]\
                .findAll('span', {'class':'next'})[0]
            try:
                nexturl = nexturl.findAll('link')[0]['href']
            except:
                nexturl = ''
            '''
            for row in PageParser._clean(table)[1:]: #skip table header
                try:
                    url, _, _, reply_time = PageParser._clean(row)
                except:
                    continue
                url = PageParser._clean(url)[0]['href'].strip()
                reply_time = PageParser._clean(reply_time)[0].strip()
                if ':' in reply_time:
                    year = time.strftime('%Y-',time.localtime(time.time()))
                    reply_time = time.strptime(year+reply_time, '%Y-%m-%d %H:%M')
                else:
                    reply_time = time.strptime(reply_time, '%Y-%m-%d')
                reply_time = int(time.mktime(reply_time))
                hashurl = hashlib.md5(url).hexdigest()
                ret.append(Link(
                    hashurl=hashurl,
                    url=url,
                    reply_time=reply_time
                ))
        except IndexError:
            Logger.error('index error!')
        return ret #, nexturl

    @staticmethod
    def _parse_shuimu(page):
        pass
 
    @staticmethod
    def _parse_ganji(page):
        pass
    
    @staticmethod
    def _parse_soufun(page):
        pass

    @staticmethod
    def _parse_58(page):
        pass
