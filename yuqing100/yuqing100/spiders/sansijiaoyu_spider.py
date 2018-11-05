# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_sansijiaoyuItem
from yuqing100.pipelines import Panduan_sansijiaoyu



class SansijiaoyuSpider(scrapy.Spider):
    name = 'sansijiaoyu_spider'
    start_urls = [
        'http://www.srssn.com/czpd/page_1.html',
        'http://www.srssn.com/gzpd/',
        'http://www.srssn.com/xxiao/',
        'http://www.srssn.com/xlks/',
        'http://www.srssn.com/wyl/',
        'http://www.srssn.com/gwy/',
        'http://www.srssn.com/zgl/',
        'http://www.srssn.com/gcl/',
        'http://www.srssn.com/yxl/',
        'http://www.srssn.com/hjl/',
        'http://www.srssn.com/jrl/',
        'http://www.srssn.com/jsj/',
        'http://www.srssn.com/gk/',
        'http://www.srssn.com/zkao/',
        'http://www.srssn.com/xxpd/'
    ]
    headers = {
        "Host": "www.srssn.com"
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
            '//ul[@class="cate-cont-list"]/li/a/@href').extract()
        urls = set()
        panduan = Panduan_sansijiaoyu()
        db_url = panduan.panduan()
        for link in links:
            link = 'http://www.srssn.com' + link
            if link not in db_url:
                urls.add(link)
        for url in urls:

            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'url':link},
                                args={'headers': self.headers, 'wait': 5},
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title and '页面未找到' not in title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="art-cont"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_sansijiaoyuItem({
                'AuthorID': '',
                'AuthorName': '',
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//div[@class="head-cont"]/span[2]/text()').extract()[0].replace('更新时间：',''),
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


