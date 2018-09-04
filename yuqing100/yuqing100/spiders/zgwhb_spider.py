# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZgwhbItem
from yuqing100.pipelines import Panduan_Zgwhbshi


class ZgwhbSpider(scrapy.Spider):
    name = 'Zgwhb_spider'
    start_urls = [
        'http://epaper.ccdy.cn'
    ]
    headers = {
        "Referer": "http://epaper.ccdy.cn/"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        urls = sele.xpath('//div[@class="paper_div"]//a[contains(@href,"content")]/@href').extract()
        url1 = 'http://epaper.ccdy.cn/html/' + time.strftime("%Y-%m", time.localtime()) + '/' + time.strftime("%d", time.localtime()) + '/'
        panduan = Panduan_Zgwhbshi()
        db_url = panduan.panduan()
        for url in urls:
            url = url1 + url
            if url not in db_url:
                yield SplashRequest(url=url,
                                    callback=self.parse1,
                                    args={'headers': self.headers, 'wait': 2},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath('//div[@id="ozoom"]//p/text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZgwhbItem({
                'AuthorID': '',
                'AuthorName': '',
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': time.strftime("%Y-%m-%d", time.localtime()),
                'Crawler': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'ReadCount': '',
                'CommentCount': '',
                'TransmitCount': '',
                'Content': Content,
                'comments': '',
                'AgreeCount': '',
                'DisagreeCount': '',
                'AskCount': '',
                'ParticipateCount': '',
                'CollectionCount': '',
                'Classification': '',
                'Labels': '',
                'Type': '',
                'RewardCount': ''
            })

            yield item
            # print(item)