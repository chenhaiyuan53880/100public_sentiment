# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZggcdlswItem
from yuqing100.pipelines import Panduan_Zggcdlsw


class ZggcdlswSpider(scrapy.Spider):
    name = 'Zggcdlsw_spider'
    start_urls = [
        'http://www.zgdsw.org.cn/GB/218999/',
        'http://www.zgdsw.org.cn/GB/349473/index.html'
    ]
    headers = {
        "Host": "www.zgdsw.org.cn",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }



    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'wait': 10,'timeout':20},
                                encoding='utf-8',
                                dont_filter=True)

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath(
            '//div[@class="d2_left fl"]//li/a/@href').extract()
        # urls = set()
        panduan = Panduan_Zggcdlsw()
        db_url = panduan.panduan()
        for link in links:
            link = 'http://www.zgdsw.org.cn' + link
            if link not in db_url:
                yield SplashRequest(url=link,
                                    callback=self.parse1,
                                    args={'headers': self.headers, 'wait': 2,'timeout':6},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="p2_right wb_right fr"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZggcdlswItem({
                'AuthorID': '',
                'AuthorName': '',
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