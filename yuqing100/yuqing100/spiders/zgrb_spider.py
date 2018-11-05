# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZgrbItem
from yuqing100.pipelines import Panduan_Zgrb



class ZgrbSpider(scrapy.Spider):
    name = 'Zgrb_Spider'
    allowed_domains = ['www.chinadaily.com.cn']
    start_urls = [
        'http://www.chinadaily.com.cn/china/governmentandpolicy'
    ]
    headers = {
        "Host": "www.chinadaily.com.cn"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2})



    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//div[@class="mb10 tw3_01_2"]')
        panduan = Panduan_Zgrb()
        db_url = panduan.panduan()
        for link in links:
            url = link.xpath('.//h4/a/@href').extract_first()
            url = url.replace('//', 'http://')
            if url not in db_url:
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
                '//div[@id="Content"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZgrbItem({
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