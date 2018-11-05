# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
# from yuqing100.items import Yuqing_QiushiItem
# from yuqing100.pipelines import Panduan_Qiushi

lua1 = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(5)
    splash:runjs("document.getElementsByClassName('foot')[0].scrollIntoView(true)")
    splash:wait(5)
    return splash:html()    
    end
 '''


class PiankeSpider(scrapy.Spider):
    name = 'Pianke_spider'
    start_urls = [
        'http://pianke.me/pages/read/readNote.html'
    ]
    headers = {
        "Host": "pianke.me"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          callback=self.parse_url,
                          dont_filter=True )

    def parse_url(self, response):
        url = response.url
        yield SplashRequest(url, endpoint='execute',
                            args={'lua_source': lua1,'headers': self.headers},
                            cache_args=['lua_source'])

    def parse(self, response):
        sele = Selector(response)
        urls = sele.xpath('//div[@class="article-title"]/a/@href').extract()
        # urls = set()
        # panduan = Panduan_Qiushi()
        # db_url = panduan.panduan()
        for url in urls:
            print(url)
            url = 'http://pianke.me/pages/read/' + url.replace('./','')
            # url = div.xpath('.//a/@href').extract()[0]
            # print(date_time)
            # print(author)
            # print(url)
            # if url not in urls:
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'date_time': date_time,"author":author},
                                # args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath('//div[@class="typo container"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = {
                'AuthorID': sele.xpath('//div[@class="article-others"]/a/@href').extract_first().split('uid=',1)[1],
                'AuthorName': sele.xpath('//div[@class="article-others"]/a/text()').extract_first(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//div[@class="article-others"]/span/text()').extract_first(),
                'Crawler': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'ReadCount': '',
                'CommentCount': '',
                'TransmitCount': '',
                'Content': Content,
                'comments': '',
                'AgreeCount': sele.xpath('//div[@class="article-others"]/span/text()').extract_first(),
                'DisagreeCount': '',
                'AskCount': '',
                'ParticipateCount': '',
                'CollectionCount': '',
                'Classification': '',
                'Labels': '',
                'Type': '',
                'RewardCount': ''
            }

            # yield item
            print(item)