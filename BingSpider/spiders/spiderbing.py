# encoding:utf-8
import scrapy
import re
from BingSpider.items import BingspiderItem
import urllib


class spiderbing(scrapy.Spider):
    name = "spiderbing"
    allowed_domains = ["cn.bing.com"]
    words = ["周奇"]
    start_urls = []
    for word in words:
        #url = 'http://cn.bing.com/search?q=%s&first=1&sc=8-0' % urllib.quote(word)
        url = urllib.quote('http://cn.bing.com/search?q=' + word, safe='/:?=')
        # print url
        start_urls.append(url)

    def __init__(self):
        self.count = 0

    def __get_url_query(self, url):
        m = re.search("q=([^&]*)", url).group(1)
        return m

    def parse(self, response):
        self.count += 1
        item = BingspiderItem()
        xx = u"[\u4e00-\u9fa5]+"
        pattern = re.compile(xx)
        query = urllib.unquote(self.__get_url_query(response.url))
        for i in response.xpath('//ol[@id="b_results"]/li[@class="b_algo"]'):
            item['title'] = (
                ''.join(''.join(i.xpath('.//h2/a//text()').extract()).split())).encode('utf-8')
            url = i.xpath('.//h2/a/@href').extract()[0].encode('utf-8')
            if url:
                if "http" in url:
                    item['url'] = url
                else:
                    item['url'] = "http://cn.bing.com" + url
            else:
                item['url'] = None
            item['content'] = (' '.join(pattern.findall(
                ''.join(i.xpath('.//p//text()').extract())))).encode('utf-8')
            item['word'] = query
            yield item

        # 寻找下一页链接
        url = response.xpath("//a[@class='sb_pagN']/@href").extract()
        if url and self.count <= 10:
            page = "http://cn.bing.com" + url[0]
            print page
            yield scrapy.Request(page, callback=self.parse)

    def closed_count(self):
        self.count = 0
