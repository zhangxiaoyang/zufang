#!/usr/bin/env python
# coding: utf-8

import re
from BeautifulSoup import BeautifulSoup

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
    def _clean(s):
        return re.sub('\s+', ' ', s).strip()
        
    @staticmethod
    def _parse_douban(page):
        if page.strip() == '':
            return {'error':'empty page'}
        soup = BeautifulSoup(page)
        ret = {}
        try:
            ret.update({
                'title2': PageParser._clean(soup.find('div', {'class':'topic-doc'})\
                    .find('table', {'class':'infobox'})\
                    .find('td', {'class':'tablecc'})\
                    .contents[1])
            })
        except:
            ret.update({'title2':None})
        try:
            content = soup.find('div', {'class':'topic-doc'})\
                    .find('div', {'id':'link-report'})
            text = content.findAll('p')
        except:
            text = []
        try:
            images = content.findAll('img')
        except:
            images = []
        try:
            links = reduce(lambda x,y:x+y, [[j['href'] for j in i.findAll('a')] for i in text])
        except:
            links = []
        try:
            avatar = soup.find('div', {'class':'article'})\
                .find('div', {'class':'user-face'})\
                .find('a')\
                .find('img')['src']
        except:
            avatar = None
        try:
            authorid = PageParser._clean(soup.find('div', {'class':'topic-doc'})\
                .find('h3')\
                .find('span', {'class':'from'})\
                .find('a')['href']\
                .replace('http://www.douban.com/group/people', '')\
                .replace('/', ''))
            authorname = PageParser._clean(soup.find('div', {'class':'topic-doc'})\
                .find('h3')\
                .find('span', {'class':'from'})\
                .find('a')\
                .contents[0])
        except:
            authorid = None
            authorname = None
        try:
            ret.update({
                'title':PageParser._clean(soup.find('div', {'id':'content'})\
                    .find('h1')\
                    .contents[0]),
                'text':PageParser._clean(' '.join([i.getText() for i in text])),
                'pub_time':PageParser._clean(soup.find('div', {'class':'topic-doc'})\
                    .find('h3')\
                    .find('span', {'class':'color-green'})\
                    .contents[0]),
                #json string below
                'author':{\
                    'id':authorid,
                    'name':authorname,
                    'avatar':avatar
                },
                'images':[[i['src'], i['alt']] for i in images],
                'links':[i for i in links],
            })
        except Exception, e:
            ret = {'error':str(e)}
        return ret

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
