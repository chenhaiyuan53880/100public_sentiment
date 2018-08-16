# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_lianhezaobaoItem
from yuqing100.pipelines import Panduan_lianhezaobao

class LianhezaobaoSpider(scrapy.Spider):
    name = 'lianhezaobao_spider'
    start_urls = [
        'http://www.zaobao.com/realtime/china',
        'http://www.zaobao.com/realtime/world',
        'http://www.zaobao.com/realtime/singapore',
        'http://www.zaobao.com/news/china',
        'http://www.zaobao.com/news/world',
        'http://www.zaobao.com/news/singapore',
        'http://www.zaobao.com/news/sea',
        'http://www.zaobao.com/finance/realtime',
        'http://www.zaobao.com/finance/china',
        'http://www.zaobao.com/finance/world',
        'http://www.zaobao.com/finance/singapore',
        'http://www.zaobao.com/finance/invest',
        'http://www.zaobao.com/finance/comment',
        'http://www.zaobao.com/finance/people',
        'http://www.zaobao.com/finance/sme',
        'http://www.zaobao.com/forum/editorial',
        'http://www.zaobao.com/forum/bilingual',
        'http://www.zaobao.com/forum/paradigm',
        'http://www.zaobao.com/forum/comic',
        'http://www.zaobao.com/wencui/politic',
        'http://www.zaobao.com/wencui/social',
        'http://www.zaobao.com/wencui/entertainment',
        'http://www.zaobao.com/wencui/technology',
        'http://www.zaobao.com/sea/politic',
        'http://www.zaobao.com/sea/exchange',
        'http://www.zaobao.com/sea/custom',
        'http://www.zaobao.com/special/report/politic/cnpol',
        'http://www.zaobao.com/zentertainment/celebs'
    ]
    headers = {
        "Host": "www.zaobao.com",
        "Referer":"http://www.zaobao.com/realtime",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
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
            '//div[contains(@class,"row list")]/div/a/@href').extract()
        urls = set()
        panduan = Panduan_lianhezaobao()
        db_url = panduan.panduan()
        for link in links:
            link = 'http://www.zaobao.com' + link
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
        title = sele.xpath('//meta[@property="og:title"]//@content').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@id="FineDining"]/p/text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_lianhezaobaoItem({
                'AuthorID': '',
                'AuthorName': '',
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//meta[@property="article:published_time"]//@content').extract_first().split('T')[0],
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
                'Labels': sele.xpath('//meta[@property="keywords"]/@content').extract_first(),
                'Type': '',
                'RewardCount': ''
            })

            yield item