# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoshuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class bizhiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()


class YqxsItem(scrapy.Item):#运行XS
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field()
    type_ = scrapy.Field()
    anthor = scrapy.Field()
    num_zishu = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class tongchengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    car_name = scrapy.Field()
    price = scrapy.Field()
    lucheng = scrapy.Field()
    guige = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()