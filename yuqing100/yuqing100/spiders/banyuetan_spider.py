# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_banyuetanItem
from yuqing100.pipelines import Panduan_banyuetan


lua1 = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementsByClassName('list-refresh-msg')[0].scrollIntoView(true)")
    splash:wait(2)
    return splash:html()
    end
 '''

lua2 = '''
function main(splash)
    splash:go(splash.args.url)
    splash:runjs("document.getElementsByClassName('c-load-more')[0].click()")
    splash:wait(2)
    return splash:html()
    end
 '''


class BanyuetanSpider(scrapy.Spider):
    name = 'banyuetan_spider'
    start_urls = [
        'http://www.banyuetan.org/byt/jinritan/index.html',
        'http://www.banyuetan.org/byt/shizhengjiangjie/index.html',
        'http://www.banyuetan.org/byt/banyuetanpinglun/index.html',
        'http://www.banyuetan.org/byt/jicengzhili/index.html',
        'http://www.banyuetan.org/byt/wenhua/index.html',
        'http://www.banyuetan.org/byt/jiaoyu/index.html',
        'http://www.banyuetan.org/byt/jingji/index.html',
        'http://www.banyuetan.org/byt/renwu/index.html',
        'http://www.banyuetan.org/byt/junshi/index.html',
        'http://www.banyuetan.org/byt/lvyou/index.html',
        'http://www.banyuetan.org/byt/sixiang/index.html',
        'http://www.banyuetan.org/byt/difangguancha/index.html',
        'http://www.banyuetan.org/byt/jiemachengshi/index.html',
        'http://www.banyuetan.org/byt/guoji/index.html',
        'http://www.banyuetan.org/byt/keji/index.html   ',
        'http://www.banyuetan.org/byt/shengtai/index.html',
        'http://www.banyuetan.org/byt/huodong/index.html',
        'http://www.banyuetan.org/byt/jiankang/index.html',
        'http://www.banyuetan.org/byt/minshenghuati/index.html'
    ]
    headers = {
        "Host": "www.banyuetan.org"
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
            '//a[contains(@href, "http://www.banyuetan.org")][contains(@href, "detail")]/@href').extract()
        urls = set()
        panduan = Panduan_banyuetan()
        db_url = panduan.panduan()
        for link in links:
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
        title = sele.xpath('//meta[contains(@property,"og:title")]/@content').extract_first()
        if title:
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[contains(@id,"detail_content")]//text()').extract()
            for body in Contents:
                Content = Content + str(body)
            item = Yuqing_banyuetanItem({
                'AuthorID': '',
                'AuthorName': sele.xpath('//meta[contains(@name,"author")]/@content').extract(),
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': sele.xpath('//meta[contains(@name,"publishdate")]/@content').extract(),
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
                'Classification': sele.xpath('//meta[contains(@property,"og:type")]/@content').extract(),
                'Labels': sele.xpath('//meta[contains(@name,"keywords")]/@content').extract(),
                'Type': '',
                'RewardCount': ''
            })

            yield item

