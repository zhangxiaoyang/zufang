#coding: utf-8
from mongoengine import *

class House(Document):
    hashurl  = StringField(max_length=32)
    title    = StringField()
    author   = DictField()
    images   = ListField()
    links    = ListField()
    text     = StringField()
    pub_time = StringField(max_length=19)
    jushi    = StringField()
    shouji   = StringField(max_length=20)
    zujin    = StringField()
    dizhi    = StringField()
    ditie    = StringField()
    url      = StringField()
    crawl_time = IntField()
    source  = StringField()
    ext     = DictField()
    sim     = ListField()
    # hashurl  title  author  images  links  text  pub_time
    # 1        2      3       4       5      6     7
    # jushi  shouji  zujin  dizhi  ditie  url  crawl_time  source  ext   sim
    # 8      9       10     11     12     13   14          15      16    17
