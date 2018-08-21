# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_CankaoxiaoxiItem
from yuqing100.pipelines import Panduan_Cankaoxiaoxi


class CankaoxiaoxiSpider(scrapy.Spider):
    name = 'Cankaoxiaoxi_Spider'
    #还有两个栏目列表也有区别以后跟新
    start_urls = [
        'http://www.cankaoxiaoxi.com/mil/jsgd/',
        'http://www.cankaoxiaoxi.com/mil/gjjq/',
        'http://www.cankaoxiaoxi.com/mil/zgjq/',
        'http://www.cankaoxiaoxi.com/mil/wqzb/',
        'http://www.cankaoxiaoxi.com/china/szyw/',
        'http://www.cankaoxiaoxi.com/china/zgwj/',
        'http://www.cankaoxiaoxi.com/china/shwx/',
        'http://www.cankaoxiaoxi.com/china/gacz/',
        'http://www.cankaoxiaoxi.com/world/qtdq/',
        'http://www.cankaoxiaoxi.com/world/ytxw/',
        'http://www.cankaoxiaoxi.com/world/omxw/',
        'http://www.cankaoxiaoxi.com/world/hqbl/',
        'http://www.cankaoxiaoxi.com/finance/zgcj/',
        'http://www.cankaoxiaoxi.com/finance/gjcj/',
        'http://www.cankaoxiaoxi.com/finance/sygs/',
        'http://www.cankaoxiaoxi.com/finance/jrsc/'
    ]
    headers = {
        "authority": "http://www.cankaoxiaoxi.com"
    }
    headers1 = {
        "Hsot": "http://www.cankaoxiaoxi.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//div[contains(@class, "inner")]/ul//li/a/@href').extract()
        # if len(links) < 1:
        #     links = sele.xpath('//div[@class="elem ov"]/a/@href').extract()
        urls = set()
        panduan = Panduan_Cankaoxiaoxi()
        db_url = panduan.panduan()
        for link in links:
            if link not in db_url:
                urls.add(link)
            else:
                print(link, '--重复')
        for url in urls:
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'url':link},
                                args={'headers': self.headers1, 'wait': 5},
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Content_urls = sele.xpath('//ul[@class="ov"]//a/@href').extract()
            Content_urls_list = []
            for Content_url in Content_urls:
                if 'http://www.cankaoxiaoxi.com' in Content_url:
                    Content_urls_list.append(Content_url)
            for url in Content_urls_list:
                response1 = requests.get(url)
                soup = Selector(text=response1.text)
                bodys = soup.xpath('//div[@id="ctrlfscont"]//p/text()').extract()
                for body in bodys:
                    Content = Content + str(body)
                time.sleep(4)
            if len(Content) < 10:
                bodys = sele.xpath('//div[@id="ctrlfscont"]//p/text()').extract()
                for body in bodys:
                    Content = Content + str(body)
            try:
                AgreeCount = sele.xpath('//p[@class="emoji-num"]/text()').extract()[3]
            except:
                AgreeCount = ''
            try:
                DisagreeCount = sele.xpath('//p[@class="emoji-num"]/text()').extract()[0]
            except:
                DisagreeCount = ''
            item = Yuqing_CankaoxiaoxiItem({
                'AuthorID': '',
                'AuthorName': sele.xpath('//span[@id="editor_baidu"]/text()').extract_first(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//span[@id="pubtime_baidu"]/text()').extract_first(),
                'Crawler': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'ReadCount': '',
                'CommentCount': '',
                'TransmitCount': '',
                'Content': Content,
                'comments': '',
                'AgreeCount': AgreeCount,
                'DisagreeCount': DisagreeCount,
                'AskCount': '',
                'ParticipateCount': '',
                'CollectionCount': '',
                'Classification': sele.xpath('//div[@class="crumb"]/a/text()').extract()[1],
                'Labels': sele.xpath('//meta[@name="keywords"]/@content').extract_first(),
                'Type': '',
                'RewardCount': ''
            })
            yield item









if __name__ == '__main__':
    response = requests.get('http://www.cankaoxiaoxi.com/mil/20180814/2310386_2.shtml')
    soup = Selector(text=response.text)
    body = soup.xpath('//div[@id="ctrlfscont"]//p/text()').extract()
    print(body)
