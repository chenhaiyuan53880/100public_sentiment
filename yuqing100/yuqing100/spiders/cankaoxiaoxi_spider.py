# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
from scrapy import Selector
from scrapy_splash import SplashRequest


class CankaoxiaoxiSpider(scrapy.Spider):
    name = 'Cankaoxiaoxi_Spider'
    allowed_domains = ['http://www.cankaoxiaoxi.com']
    start_urls = [
        'http://www.cankaoxiaoxi.com/mil/gjjq/'
    ]
    headers = {
        "authority": "http://www.cankaoxiaoxi.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//div[contains(@class, "inner")]//a/@href').extract()
        print(links)

