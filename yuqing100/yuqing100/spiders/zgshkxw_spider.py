# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZgshkxwItem
from yuqing100.pipelines import Panduan_Zgshkxw


class ZgshkxwSpider(scrapy.Spider):
    name = 'Zgshkxw_spider'
    start_urls = [
        'http://orig.cssn.cn/sf/'
    ]
    headers = {
        "Referer": "http://www.cssn.cn/",
        "Host":"orig.cssn.cn",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        urls = sele.xpath('.//div[@class="f-main-leftMain-content clear"]//a/@href').extract()
        panduan = Panduan_Zgshkxw()
        db_url = panduan.panduan()
        for url in urls:
            if 'http://www.cssn.cn/' in url:
                if url not in db_url:
                    print(url)
                    yield SplashRequest(url=url,
                                        callback=self.parse1,
                                        args={'headers': self.headers, 'wait': 10,"timeout":60},
                                        encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath('.//div[@class="TRS_Editor"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZgshkxwItem({
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