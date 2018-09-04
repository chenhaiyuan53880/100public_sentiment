# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_QiushiItem
from yuqing100.pipelines import Panduan_Qiushi


class QiushiSpider(scrapy.Spider):
    name = 'Qiushi_spider'
    start_urls = [
        'http://www.qstheory.cn/economy/ggfz.htm'
    ]
    headers = {
        "Host": "www.qstheory.cn"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        divs = sele.xpath('//div[@class="qs_gailan01"]//li')
        # urls = set()
        panduan = Panduan_Qiushi()
        db_url = panduan.panduan()
        for div in divs:
            date_time = div.xpath('.//span/text()').extract()[0]
            author = div.xpath('.//span/text()').extract()[1]
            url = div.xpath('.//a/@href').extract()[0]
            # print(date_time)
            # print(author)
            # print(url)
            if url not in db_url:
                yield SplashRequest(url=url,
                                    callback=self.parse1,
                                    meta={'date_time': date_time,"author":author},
                                    # args={'headers': self.headers, 'wait': 2},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath('//div[@class="highlight"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_QiushiItem({
                'AuthorID': '',
                'AuthorName': response.meta['author'],
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': response.meta['date_time'],
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