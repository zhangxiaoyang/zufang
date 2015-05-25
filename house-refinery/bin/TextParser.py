#!/usr/bin/env python
# coding: utf-8

from Utils import Link, Logger
import re
import jieba
import jieba.posseg as pseg

jieba.load_userdict('dict/baidu.dict')
jieba.load_userdict('dict/sougou.dict')

class TextParser:
    
    @staticmethod
    def _jushi(text):
        def _norm(word):
            word_map = {
                u'1':u'一', u'2':u'二', u'3':u'三', u'4':u'四', u'5':u'五',\
                u'6':u'六', u'7':u'七', u'8':u'八', u'9':u'九', u'0':u'零',\
                u'两':u'二'
            }
            if word_map.has_key(word):
                return word_map[word]
            else:
                return word

        core = ur'([0-9一二两三四五六七八九])室([0-9一二两三四五六七八九])厅|([0-9一二两三四五六七八九])居[室]{0,1}'
        p = re.compile(core, re.UNICODE)
        matches =  p.findall(text)
        jushi = {}
        for i, j, k in matches:
            i = _norm(i)
            j = _norm(j)
            k = _norm(k)
            if i and j:
                if jushi.has_key(i):
                    if j not in jushi[i]:
                        jushi[i].add(j)
                else:
                    jushi[i] = set(j)
            if k: 
                if not jushi.has_key(k):
                    jushi[k] = set()
        ret = []
        for i in jushi:
            if jushi[i]:
                for j in jushi[i]:
                    ret.append(u'%s室%s厅' % (i, j))
            else:
                ret.append(u'%s居室' % (i))
        if ret: return u','.join(ret)
        else: return u''

    @staticmethod
    def _shouji(text):
        core = ur'(1[3|4|5|8]\d{9})|(1[3|4|5|8]\d[\- ]\d{3}[\- ]\d{5})|(1[3|4|5|8]\d[\- ]\d{4}[\- ]\d{4})'
        p = re.compile(core, re.UNICODE)
        matches =  p.findall(text)
        ret = set()
        for i in matches:
            for j in i:
                if j:
                    ret.add(re.sub(ur'\D', u'', j))
        if ret: return u','.join(ret)
        else: return u''

    @staticmethod
    def _zujin(text):
        core = ur'(\d{3,4}[元]?[/每]?月)|((价格|租金)\D?\d{3,4}\D)'
        p = re.compile(core, re.UNICODE)
        matches =  p.findall(text)
        ret = set()
        for i in matches:
            for j in i:
                j = re.sub(ur'\D', u'', j)
                if j:
                    ret.add(int(j))
        if len(ret) == 1:
            return u'%d元' % (ret.pop())
        elif len(ret) > 1:
            return u'%d-%d元' % (min(ret), max(ret))
        else: return u''

    @staticmethod
    def _dizhi(text):
        def find_place(text):
            ret = set()
            segs = pseg.cut(text)
            for i, seg in enumerate(segs):
                if seg.flag in ['bd', 'sg']:
                    ret.add(seg.word)
            return ret

        """
        core = ur'[0-9a-zA-Z\u4E00-\u9FA5]{2,}'
        p = re.compile(core, re.UNICODE)
        matches = p.findall(text)
        text = u''.join([ i for i in matches if len(i)>3])
        ret = set()
        for i in matches:
            if i:
                place = find_place(i)
                if place:
                    ret.add(place)
        return u'||'.join([ i for i in ret])
        """
        return u','.join(find_place(text))

    @staticmethod
    def _ditie(text):
        def _norm(word):
            word_map = {
                u'一':u'1', u'二':u'2', u'三':u'3', u'四':u'4', u'五':u'5',\
                u'六':u'6', u'七':u'7', u'八':u'8', u'九':u'9', u'十':u'10',\
                u'十一':u'11', u'十二':u'12', u'十三':u'13', u'十四':u'14', u'十五':u'15',
            }
            if word_map.has_key(word):
                return word_map[word]
            else:
                return word
        core = ur'(1|2|4|5|6|8|9|10|13|14|15|一|二|四|五|六|八|九|十|十三|十四|十五|十五)号线|(八通|昌平|亦庄|房山|机场)线'
        p = re.compile(core, re.UNICODE)
        matches =  p.findall(text)
        ret = set()
        for i, k in matches:
            if i: ret.add(u'%s号线' % _norm(i))
            if k: ret.add(u'%s线' % k)
        if ret: return u','.join(ret)
        else: return u''

    @staticmethod
    def parse(text):
        unicode_string = text.decode('utf-8')
        return {
            'jushi': TextParser._jushi(unicode_string).encode('utf-8'),
            'shouji': TextParser._shouji(unicode_string).encode('utf-8'),
            'zujin': TextParser._zujin(unicode_string).encode('utf-8'),
            'dizhi': TextParser._dizhi(unicode_string).encode('utf-8'),
            'ditie': TextParser._ditie(unicode_string).encode('utf-8'),
        }

    @staticmethod
    def _parse_shuimu(text):
        pass
 
    @staticmethod
    def _parse_ganji(text):
        pass
    
    @staticmethod
    def _parse_soufun(text):
        pass

    @staticmethod
    def _parse_58(text):
        pass
