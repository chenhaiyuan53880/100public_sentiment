# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZhongguolishiItem
from yuqing100.pipelines import Panduan_Zhongguolishi



class ZhongguolishiSpider(scrapy.Spider):
    name = 'Zhongguolishi_spider'
    start_urls = [
        'http://www.zgdsw.com/news.asp?typenumber=0005',
        'http://www.zgdsw.com/news.asp?typenumber=0006',
        'http://www.zgdsw.com/news.asp?typenumber=0007',
        'http://www.zgdsw.com/news.asp?typenumber=0008',
        'http://www.zgdsw.com/news.asp?typenumber=0009',
        'http://www.zgdsw.com/news.asp?typenumber=0011',
        'http://www.zgdsw.com/news.asp?typenumber=0010',
        'http://www.zgdsw.com/news.asp?typenumber=0021',
        'http://www.zgdsw.com/news.asp?typenumber=0016',
        'http://www.zgdsw.com/news.asp?typenumber=0017',
        'http://www.zgdsw.com/news.asp?typenumber=0018',
        'http://www.zgdsw.com/news.asp?typenumber=0019'
    ]
    headers = {
        "Host": "www.zgdsw.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        divs = sele.xpath('//div[@class="nnewslb"]')
        urls = set()
        panduan = Panduan_Zhongguolishi()
        db_url = panduan.panduan()
        for div in divs:
            date_time = div.xpath('.//h2/text()').extract_first()
            if date_time:
                url = div.xpath('.//a/@href').extract_first()
                url = 'http://www.zgdsw.com/' + url
                if url not in db_url:
                    yield SplashRequest(url=url,
                                        callback=self.parse1,
                                        meta={'date_time': date_time},
                                        args={'headers': self.headers, 'wait': 2},
                                        encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath('//div[@id="xxcontent"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZhongguolishiItem({
                'AuthorID': '',
                'AuthorName': '',
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