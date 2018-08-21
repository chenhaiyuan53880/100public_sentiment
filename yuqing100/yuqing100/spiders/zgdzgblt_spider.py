# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZgdzgbltItem
from yuqing100.pipelines import Panduan_Zgdzgblt


class ZgdzgbltSpider(scrapy.Spider):
    name = 'Zgdzgblt_spider'
    start_urls = [
        'http://www.zgdzgblt.com/'
    ]
    headers = {
        "Host": "www.zgdzgblt.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath(
            '//ul[@class="list"]//a/@href').extract()
        urls = set()
        panduan = Panduan_Zgdzgblt()
        db_url = panduan.panduan()
        for link in links:
            link = 'http://www.zgdzgblt.com' + link
            if link not in db_url:
                urls.add(link)
        for url in urls:
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
            Contents = sele.xpath(
                '//p[contains(@align,"left")]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZgdzgbltItem({
                'AuthorID': '',
                'AuthorName': sele.xpath('//p[@class="author2"]/text()').extract_first().split('来源')[0],
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//strong[@id="todayTime"]/text()').extract_first(),
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