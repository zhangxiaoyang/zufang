#coding: utf-8
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from models import House
from mongoengine import *
import operator
import re
import os
from ui.settings import BASE_DIR

def index(request):
    return render(request, 'index.html', locals())

def download(request):
    apks = os.listdir(os.path.join(BASE_DIR, 'static/apks'))
    latest_apk = sorted(apks)[-1]
    latest_version = re.sub(r'\.\w+$', '', latest_apk.split('_')[-1])
    return HttpResponseRedirect('/static/apks/' + latest_apk)

def update(request):
    apks = os.listdir(os.path.join(BASE_DIR, 'static/apks'))
    latest_apk = sorted(apks)[-1]
    latest_version = re.sub(r'\.\w+$', '', latest_apk.split('_')[-1])
    return HttpResponse(latest_version)

def make_query(query):
    querys = re.split(r'\s+', query)
    new_query = []
    count = 1
    for i in querys:
        if len(i) > 1:
            if count > 3:
                break
            core = ur'[0-9a-zA-Z\u4E00-\u9FA5]{2,}'
            p = re.compile(core, re.UNICODE)
            query = ''.join(re.findall(p, i))
            if new_query:
                new_query.append(Q(title__contains=query))
                new_query.append(Q(text__contains=query))
            else:
                new_query = [Q(title__contains=query), Q(text__contains=query)]
            count += 1
    return reduce(operator.or_, new_query)

def search(request, query, page_num=1):
    new_query = make_query(query)
    if not new_query:
        return JsonResponse({'error':'Invalid query'})

    page_size = 5
    page_num = int(page_num)
    if page_num < 1:
        return JsonResponse({'error':'Invalid page_num'})
    
    house_model = House.objects.filter(new_query).order_by('-pub_time')
    count = house_model.count()
    page_count = count/page_size+1 if count%page_size else count/page_size
    page_next = page_num+1 if page_num < page_count else -1
    page_prev = page_num-1 if page_num > 1 else -1
    houses = house_model.skip((page_num-1)*page_size).limit(page_size)

    ret = []
    for h in houses:
        images = []
        for i in h.images:
            image_src, image_alt = i
            if image_src:
                images.append(('/static/imgdir/'+image_src.split('/')[-1], image_alt))
        dizhi = [i for i in h.dizhi.split(',') if i]
        ditie = [i for i in h.ditie.split(',') if i]

        ret.append({
            "hashurl":h.hashurl,
            "title":h.title,
            "author":h.author,
            "images":images,
            "links":h.links,
            "text":h.text,
            "pub_time":h.pub_time,
            "jushi":h.jushi,
            "shouji":h.shouji,
            "zujin":h.zujin,
            "dizhi":dizhi,
            "ditie":ditie,
            "url":h.url,
            "crawl_time":h.crawl_time,
            "source":h.source,
            "ext":h.ext,
            "sim":h.sim,
        })

    return JsonResponse({
        'result':ret,
        'page_num':page_num,
        'page_count':page_count,
        'page_prev':page_prev,
        'page_next':page_next,
        'query':query,
    })
