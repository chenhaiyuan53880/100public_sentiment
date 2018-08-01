# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_nanfrwzkItem
from yuqing100.pipelines import Panduan_nanfrwzk

class NanfrwzkSpider(scrapy.Spider):
    name = 'nanfrwzk_spider'
    start_urls = [
        'http://www.nfpeople.com/category/2',
        'http://www.nfpeople.com/category/3',
        'http://www.nfpeople.com/category/14',
        'http://www.nfpeople.com/category/9',
        'http://www.nfpeople.com/category/6',
        'http://www.nfpeople.com/category/5'
    ]
    headers = {
        "Host": "www.nfpeople.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath(
            '//div[@class="leftbox lists"]/dl/dt/a/@href').extract()
        urls = set()
        panduan = Panduan_nanfrwzk()
        db_url = panduan.panduan()
        for link in links:
            if link not in db_url:
                urls.add(link)
        for url in urls:
            print(url)
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'url':link},
                                args={'headers': self.headers, 'wait': 5},
                                encoding='utf-8')
    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title and 'Error' not in title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="mainContent"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_nanfrwzkItem({
                'AuthorID': '',
                'AuthorName': sele.xpath('//meta[contains(@name,"author")]/@content').extract(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//p[@class="source"]/text()').extract()[0].split('日期：')[1],
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
                'Labels': sele.xpath('//meta[contains(@name,"keywords")]/@content').extract(),
                'Type': '',
                'RewardCount': ''
            })

            yield item