# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_DanjianyanjiuItem
from yuqing100.pipelines import Panduan_Danjianyanjiu




class DanjianyanjiuSpider(scrapy.Spider):
    name = 'Danjianyanjiu_spider'
    start_urls = [
        'http://www.djyj.cn/GB/408265/index.html',
        'http://www.djyj.cn/GB/412780/index.html',
        'http://www.djyj.cn/GB/415738/index.html',
        'http://www.djyj.cn/GB/415351/index.html',
        'http://www.djyj.cn/GB/408268/index.html',
        'http://www.djyj.cn/GB/408215/index.html',
        'http://www.djyj.cn/GB/408269/index.html',
        'http://www.djyj.cn/GB/408273/index.html',
        'http://www.djyj.cn/GB/408270/index.html',
        'http://www.djyj.cn/GB/408271/index.html',
        'http://www.djyj.cn/GB/408274/index.html',
        'http://www.djyj.cn/GB/408276/index.html',
        'http://www.djyj.cn/GB/408275/index.html',
        'http://www.djyj.cn/GB/408277/index.html'
    ]
    headers = {
        "Host": "www.djyj.cn/",
        "Referer":"http://www.djyj.cn/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }



    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//div[contains(@class, "p2j_list_lt")]//li/a/@href').extract()
        urls = set()
        panduan = Panduan_Danjianyanjiu()
        db_url = panduan.panduan()
        for link in links:
            link = "http://www.djyj.cn" + link
            if link not in db_url:
                urls.add(link)
        for url in urls:
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="text_con clearfix"]//p/text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_DanjianyanjiuItem({
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
                'Labels': sele.xpath('//meta[@name="keywords"]/@content').extract_first(),
                'Type': '',
                'RewardCount': ''
            })

            yield item
