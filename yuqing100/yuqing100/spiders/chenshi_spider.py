# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
# from yuqing100.items import Yuqing_ZgrbItem
# from yuqing100.pipelines import Panduan_Zgrb



class ChenshiSpider(scrapy.Spider):
    name = 'Chenshi_Spider'
    allowed_domains = ['www.cutv.com']
    start_urls = [
        'http://www.cutv.com/guonei/',
        'http://www.cutv.com/guoji/'
    ]
    headers = {
        "Host": "www.cutv.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 10})



    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//h2/a/@href').extract()
        # panduan = Panduan_Zgrb()
        # db_url = panduan.panduan()
        for link in links:
            url = 'http://www.cutv.com' +link
            # url = url.replace('//', 'http://')
            # if url not in db_url:
            # try:
            #     data_time = link.xpath('.//span[@class="tw3_01_2_t"]//b/text()').extract_first()
            # except:
            #     data_time = '0'
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'data_time':data_time},
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@id="full"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = {
                'AuthorID': '',
                'AuthorName': '',
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//ins/text()').extract_first(),
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
                'Type': sele.xpath('//meta[contains(@name,"keywords")]/@content').extract(),
                'RewardCount': ''
            }

            # yield item
            print(item)