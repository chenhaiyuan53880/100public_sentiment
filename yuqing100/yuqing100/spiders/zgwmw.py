# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZgwmwItem
from yuqing100.pipelines import Panduan_Zgwmw

class ZgwmwSpider(scrapy.Spider):
    name = 'Zgwmw_spider'
    start_urls = [
        'http://www.wenming.cn/bwzx/jj/',
        'http://www.wenming.cn/ziliao/rsrm/',
        'http://www.wenming.cn/a2/fbt/',
        'http://www.wenming.cn/a/yw/',
        'http://www.wenming.cn/bwzx/dt/',
        'http://www.wenming.cn/ldhd/'
    ]
    headers = {
        "Host": "www.wenming.cn"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        urls = set()
        panduan = Panduan_Zgwmw()
        db_url = panduan.panduan()
        div_urls = sele.xpath('//div[@class="fbt-p"]/a/@href').extract()
        for url in div_urls:
            if 'http://www.wenming.cn' not in url:
                url = response.url + url.replace('./','/')
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
            Contents = sele.xpath('//div[@class="Custom_UnionStyle"]//text()').extract()
            if len(Contents) < 10:
                Contents = sele.xpath('//div[@class="TRS_Editor"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZgwmwItem({
                'AuthorID': '',
                'AuthorName': sele.xpath('//meta[@name="author"]/@content').extract_first(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//meta[@name="publishdate"]/@content').extract_first(),
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