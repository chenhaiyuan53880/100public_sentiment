# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_DgbItem
from yuqing100.pipelines import Panduan_Dgb



class DgbSpider(scrapy.Spider):
    name = 'Dgb_Spider'
    # allowed_domains = ['www.takungpao.com.cn']
    start_urls = [
        'http://www.takungpao.com/news/232108/index.html'
    ]
    headers = {
        "Host": "www.takungpao.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2})



    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//dl[@class="item clearfix"]')
        panduan = Panduan_Dgb()
        db_url = panduan.panduan()
        for link in links:
            url = link.xpath('.//dd[@class="intro"]/a/@href').extract_first()
            if url not in db_url:
            # try:
            #     data_time = link.xpath('.//span[@class="tw3_01_2_t"]//b/text()').extract_first()
            # except:
            #     data_time = '0'
            # print(url)
                yield SplashRequest(url=url,
                                    callback=self.parse1,
                                    # meta={'data_time':data_time},
                                    args={'headers': self.headers, 'wait': 2},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="tkp_content"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_DgbItem({
                'AuthorID': '',
                'AuthorName': '',
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//*[@class="tkp_con_author"]//span/text()').extract_first(),
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