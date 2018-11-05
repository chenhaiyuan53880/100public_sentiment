# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_LieyunItem
from yuqing100.pipelines import Panduan_Lieyun

class LieyunSpider(scrapy.Spider):
    name = 'Lieyun_Spider'
    allowed_domains = ['www.lieyunwang.com']
    start_urls = [
        'https://www.lieyunwang.com/'
    ]
    headers = {
        "user-agent":"ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse,
                                args={'headers': self.headers,'wait': 10 , 'timeout':30})



    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//a[@class="lyw-article-title"]/@href').extract()
        panduan = Panduan_Lieyun()
        db_url = panduan.panduan()
        urls = set()
        for link in links:
            link = 'https://www.lieyunwang.com' + link
            urls.add(link)
        for url in urls:
            # if url not in db_url:
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'data_time':data_time},
                                args={'headers': self.headers, 'wait': 10,'timeout':60},
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="main-text"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_LieyunItem({
                'AuthorID': sele.xpath('//a[@class="author-name open_reporter_box"]/@href').extract_first().replace('/space/',''),
                'AuthorName': sele.xpath('//meta[contains(@name,"author")]/@content').extract_first(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//span[@class="time"]/text()').extract_first(),
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
                'Labels': sele.xpath('//meta[@name="keywords"]/@content').extract_first(),
                'Type': '',
                'RewardCount': ''
            })

            yield item
            # print(item)