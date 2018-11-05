# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_heimawangItem
from yuqing100.pipelines import Panduan_heimawang




class HeimawangSpider(scrapy.Spider):
    name = 'heimawang_spider'
    start_urls = [
        'http://www.iheima.com/'
    ]
    headers = {
        "Host": "www.iheima.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }



    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                # args={'headers': self.headers, 'wait': 10},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath(
            '//a[contains(@class, "title")]/@href').extract()
        urls = set()
        panduan = Panduan_heimawang()
        db_url = panduan.panduan()
        for link in links:
            link = 'http://www.iheima.com' + link
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
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="main-content"]/p/text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_heimawangItem({
                'AuthorID': '',
                'AuthorName': sele.xpath('//meta[@name="author"]//@content').extract_first(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//span[@class="time fl"]/text()').extract()[1],
                'Crawler': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'ReadCount': sele.xpath('//span[@id="pv-num"]/text()').extract_first(),
                'CommentCount': '',
                'TransmitCount': '',
                'Content': Content,
                'comments': '',
                'AgreeCount': sele.xpath('//span[@id="zan-num"]/text()').extract_first(),
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