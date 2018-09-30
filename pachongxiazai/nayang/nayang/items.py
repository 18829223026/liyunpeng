# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NayangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class BizhiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
class XiaoshuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type_ = scrapy.Field()
    number = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    chpter_name = scrapy.Field()
    chpter_content = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
class NayangJobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    education = scrapy.Field()
    money = scrapy.Field()
    discript = scrapy.Field()
    job_addr = scrapy.Field()