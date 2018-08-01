# -*- coding: utf-8 -*-
import scrapy
import re
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Kepu_tupian
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


class KepuchinaSpider(scrapy.Spider):
    name = 'kepuchina_tuwen_spider'
    start_urls = [
        'http://www.kepuchina.cn/tech/'
    ]
    headers = {
        "Host": "www.kepuchina.cn"
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
            '//div[contains(@class, "dialog")]/a/@href').extract()
        urls = set()
        for link in links:
            urls.add(link.replace('./','http://www.kepuchina.cn/tech/'))
        for url in urls:
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'url':link},
                                args={'headers': self.headers, 'wait': 5},
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title//text()').extract_first()
        if title:
            PublishTime = sele.xpath('//p[contains(@class,"tips")]/span/text()').extract()[1]
            Contents = sele.xpath('//div[contains(@class,"content_detail")]').extract()[0]
            url = response.url
            img_urls = sele.xpath('//div[contains(@class,"content_detail")]//img/@src').extract()
            if len(img_urls) < 1:
                img_urls = ''
            item = Kepu_tupian({
                    'Title':title,
                    'PublishTime' : PublishTime,
                    'Content' : self.replace_two(Contents).replace(')','').replace('(','').replace('\u3000',''),
                    'url' : url,
                    'img_url' : img_urls,
                    'img_path' : ''
            })
            yield item

    def replace_two(self,m):
        """
        #过滤掉页面中除了<p></p>和<img>以外所有的标签
        """
        all = re.findall(r'</?.*?>', m)
        save = re.findall(r'</?(?:img).*?>', m)

        for e in all:
            if e not in save:
                m1 = m.replace(e, '')
                m = m1
        return m