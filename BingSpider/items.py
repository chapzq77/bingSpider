# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BingspiderItem(scrapy.Item):
    # 输入人名返回的title
    title = scrapy.Field()
    # 返回的content
    content = scrapy.Field()
    # title中的url
    url = scrapy.Field()
    # 查询的词
    word = scrapy.Field()
