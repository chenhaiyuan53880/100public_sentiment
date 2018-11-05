# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_QiushiItem
from yuqing100.pipelines import Panduan_Qiushi


class QiushiSpider(scrapy.Spider):
    name = 'Qiushi_spider'
    start_urls = [
        'http://www.qstheory.cn/economy/ggfz.htm',
        'http://www.qstheory.cn/economy/jjgc.htm',
        'http://www.qstheory.cn/economy/cyzh.htm',
        'http://www.qstheory.cn/economy/qyjj.htm',
        'http://www.qstheory.cn/economy/hqsy.htm',
        'http://www.qstheory.cn/economy/xrsd.htm',
        'http://www.qstheory.cn/politics/ggts.htm',
        'http://www.qstheory.cn/politics/yfzg.htm',
        'http://www.qstheory.cn/politics/mzzz.htm',
        'http://www.qstheory.cn/politics/shgc.htm',
        'http://www.qstheory.cn/politics/gcsk.htm',
        'http://www.qstheory.cn/politics/wwtj.htm',
        'http://www.qstheory.cn/culture/whqg.htm',
        'http://www.qstheory.cn/culture/hxjz.htm',
        'http://www.qstheory.cn/culture/whcy.htm',
        'http://www.qstheory.cn/culture/whsy.htm',
        'http://www.qstheory.cn/culture/wypl.htm',
        'http://www.qstheory.cn/culture/whgc.htm',
        'http://www.qstheory.cn/society/shgl.htm',
        'http://www.qstheory.cn/society/shbz.htm',
        'http://www.qstheory.cn/society/cxfz.htm',
        'http://www.qstheory.cn/society/msjs.htm',
        'http://www.qstheory.cn/society/rkgz.htm',
        'http://www.qstheory.cn/cpc/djyj.htm',
        'http://www.qstheory.cn/cpc/ffcl.htm',
        'http://www.qstheory.cn/cpc/gcsk.htm',
        'http://www.qstheory.cn/cpc/dsbl.htm',
        'http://www.qstheory.cn/cpc/jcdj.htm',
        'http://www.qstheory.cn/zoology/stwm.htm',
        'http://www.qstheory.cn/zoology/nyzy.htm',
        'http://www.qstheory.cn/zoology/hjbh.htm',
        'http://www.qstheory.cn/zoology/dfst.htm',
        'http://www.qstheory.cn/defense/v7_pdlist_sxzz.html',
        'http://www.qstheory.cn/defense/v7_pdlist_gfjs.html',
        'http://www.qstheory.cn/defense/v7_pdlist_jsll.html',
        'http://www.qstheory.cn/defense/v7_pdlist_jsbk.html',
        'http://www.qstheory.cn/books/xstj.htm',
        'http://www.qstheory.cn/books/tszx.htm',
        'http://www.qstheory.cn/books/rdsp.htm',
        'http://www.qstheory.cn/qslgxd/lltt.htm',
        'http://www.qstheory.cn/qslgxd/ggsj.htm',
        'http://www.qstheory.cn/qslgxd/ssrp.htm',
        'http://www.qstheory.cn/qslgxd/wyxy.htm',
        'http://www.qstheory.cn/qszq/qsdd/index.htm',
        'http://www.qstheory.cn/qswp.htm',
        'http://www.qstheory.cn/qszq/xxbj/index.htm'
    ]
    headers = {
        "Host": "www.qstheory.cn"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        divs = sele.xpath('//div[@class="qs_gailan01"]//li')
        # urls = set()
        panduan = Panduan_Qiushi()
        db_url = panduan.panduan()
        for div in divs:
            date_time = div.xpath('.//span/text()').extract()[0]
            author = div.xpath('.//span/text()').extract()[1]
            url = div.xpath('.//a/@href').extract()[0]
            # print(date_time)
            # print(author)
            # print(url)
            if url not in db_url:
                yield SplashRequest(url=url,
                                    callback=self.parse1,
                                    meta={'date_time': date_time,"author":author},
                                    # args={'headers': self.headers, 'wait': 2},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath('//div[@class="highlight"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_QiushiItem({
                'AuthorID': '',
                'AuthorName': response.meta['author'],
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': response.meta['date_time'],
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