# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZgdzgbltItem
from yuqing100.pipelines import Panduan_Zgdzgblt


class ZgdzgbltSpider(scrapy.Spider):
    name = 'Zgdzgblt_spider'
    start_urls = [
        'http://www.zgdzgblt.com/'
    ]
    headers = {
        "Host": "www.zgdzgblt.com",
        "Cookie":"UM_distinctid=165562b7db20-094598c41de32-9393265-1fa400-165562b7db4191; PHPSESSID=3u0dmtk3emenki0lejl5upnra1; CNZZDATA5740866=cnzz_eid%3D1782750184-1534744699-null%26ntime%3D1540254056",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Referer":"https://www.baidu.com/link?url=NBjAZ9j-FVtlbV2sE3-k3SHv-k2mO8qbUNxNTX_7cFq3okP25tgTUi3naTCURIzq&wd=&eqid=b8cf681e00040f4f000000035bce74dd"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'wait': 20,'timeout':60},
                                encoding='utf-8',
                                dont_filter=True)

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath(
            '//ul[@class="list"]//a/@href').extract()
        urls = set()
        panduan = Panduan_Zgdzgblt()
        db_url = panduan.panduan()
        for link in links:
            link = 'http://www.zgdzgblt.com' + link
            if link not in db_url:
                urls.add(link)
        for url in urls:
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                args={'headers': self.headers, 'wait': 20,'timeout':60},
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//p[contains(@align,"left")]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZgdzgbltItem({
                'AuthorID': '',
                'AuthorName': '',
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//strong[@id="todayTime"]/text()').extract_first(),
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