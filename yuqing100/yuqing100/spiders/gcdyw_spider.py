# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_GcdywItem
from yuqing100.pipelines import Panduan_Gcdyw
from yuqing100.models import datefilter

class GcdywSpider(scrapy.Spider):
    name = 'Gcdyw_spider'
    start_urls = [
        'http://www.12371.cn/zxfb/'
    ]
    headers = {
        "Host": "www.12371.cn"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 10,'timeout':30},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath(
            '//div[@class="zxyw_R"]//a/@href').extract()
        urls = set()
        panduan = Panduan_Gcdyw()
        db_url = panduan.panduan()
        for link in links:
            if link not in db_url:
                urls.add(link)
        for url in urls:
            print(url)
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'url':link},
                                args={'headers': self.headers, 'wait': 10},
                                encoding='utf-8')
    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title and 'Error' not in title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="font_area_mid"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_GcdywItem({
                'AuthorID': '',
                'AuthorName': '',
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': datefilter('2018年' + sele.xpath('//i[@class="time"]/text()').extract_first().split('2018年',1)[1].split('日',1)[0] + '日',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
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
                'Labels': sele.xpath('//meta[contains(@name,"keywords")]/@content').extract_first(),
                'Type': '',
                'RewardCount': ''
            })

            yield item
            # print(item)