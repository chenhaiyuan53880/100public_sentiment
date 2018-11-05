# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_ZywxyjsItem
from yuqing100.pipelines import Panduan_Zywxyjs


class ZywxyjsSpider(scrapy.Spider):
    name = 'Zywxyjs_spider'
    start_urls = [
        'https://www.wxyjs.org.cn/zyldrhd_547/'
    ]
    headers = {
        "Host": "www.wxyjs.org.cn",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Referer":"https://www.wxyjs.org.cn/zyldrhd_547/"
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
            '//table[@class="center gl_list1"]//a/@href').extract()
        panduan = Panduan_Zywxyjs()
        db_url = panduan.panduan()
        for link in links:
            link = 'https://www.wxyjs.org.cn/zyldrhd_547/' + link
            link = link.replace('/./','/')
            # print(link)
            if link not in db_url:
                yield SplashRequest(url=link,
                                    callback=self.parse1,
                                    args={'headers': self.headers, 'wait': 10,'timeout':60},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="TRS_PreAppend"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_ZywxyjsItem({
                'AuthorID': '',
                'AuthorName': '',
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//table[@class="sp_lm2"]/tbody/tr/td[3]/span/text()').extract_first(),
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