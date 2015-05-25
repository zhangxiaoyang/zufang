#coding: utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('app.views',
    url(r'^$', 'index'),
    url(r'download/$', 'download'),
    
    url(r'^apis/update/$', 'update'),
    url(r'^apis/search/(.*?)/(\d+)/$', 'search'),
    url(r'^apis/search/(.*?)/$', 'search'),
)
if settings.DEBUG == False:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
