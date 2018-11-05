# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ChuanyebanItem
from yuqing100.pipelines import Panduan_Chuanyeban
from yuqing100.models import datefilter

class ChuanyebanSpider(scrapy.Spider):
    name = 'Chuanyeban_spider'
    start_urls = [
        'https://www.cyzone.cn/'
    ]
    headers = {
        "Host": "www.cyzone.cn"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 10,'timeout':20},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath(
            '//div[@class="article-item clearfix"]/div[@class="item-intro"]/a/@href').extract()
        urls = set()
        panduan = Panduan_Chuanyeban()
        db_url = panduan.panduan()
        for link in links:
            if 'https' not in link:
                link = link.replace('//www','https://www').replace('http:','')
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
                '//div[@class="single-item"]/div[@class="article-content"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            try:
                PublishTime = datefilter(sele.xpath('//span[@class="date-time"]/text()').extract()[1],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            except:
                PublishTime = datefilter(sele.xpath('//span[@class="date-time"]/text()').extract()[0],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            item = Yuqing_ChuanyebanItem({
                'AuthorID': '',
                'AuthorName': sele.xpath('//span[@class="name"]/text()').extract_first(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': PublishTime,
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