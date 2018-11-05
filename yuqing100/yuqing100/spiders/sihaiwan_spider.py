# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_SihaiItem
from yuqing100.pipelines import Panduan_Sihai

class SihaiSpider(scrapy.Spider):
    name = 'Sihai_Spider'
    # allowed_domains = ['www.4hw.com.cn']
    start_urls = [
        'https://yule.4hw.com.cn/'
    ]
    headers = {
        "user-agent":"ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse,
                                args={'headers': self.headers,'wait': 10 , 'timeout':20})



    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//div[@class="text-pic"]/a/@href').extract()
        panduan = Panduan_Sihai()
        db_url = panduan.panduan()
        urls = set()
        for link in links:
            urls.add(link)
        print(urls)
        for url in urls:
            if url not in db_url:
                yield SplashRequest(url=url,
                                    callback=self.parse1,
                                    # meta={'data_time':data_time},
                                    args={'headers': self.headers, 'wait': 10,'timeout':20},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="art-text"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_SihaiItem({
                'AuthorID': '',
                'AuthorName': sele.xpath('//span[@class="author-mate"]/text()').extract_first(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//div[@class="fl"]/text()').extract_first(),
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