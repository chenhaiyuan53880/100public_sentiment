# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_JRTTItem
from yuqing100.pipelines import Panduan_JRTT


lua1 = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(5)
    splash:runjs("document.getElementsByClassName('list-refresh-msg')[0].scrollIntoView(true)")
    splash:wait(5)
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


class Jrtt01SpiderSpider(scrapy.Spider):
    name = 'JRTT_01_Spider'
    allowed_domains = ['www.toutiao.com']
    start_urls = [
        'https://www.toutiao.com/ch/news_hot/',
        'https://www.toutiao.com/ch/news_tech/',
        'https://www.toutiao.com/ch/internet/',
        'https://www.toutiao.com/ch/software/',
        'https://www.toutiao.com/ch/smart_home/',
        'https://www.toutiao.com/ch/news_entertainment/',
        'https://www.toutiao.com/ch/movie/',
        'https://www.toutiao.com/ch/teleplay/',
        'https://www.toutiao.com/ch/shows/',
        'https://www.toutiao.com/ch/gossip/',
        'https://www.toutiao.com/ch/env_protection/',
        'https://www.toutiao.com/ch/news_sports/',
        'https://www.toutiao.com/ch/nba/',
        'https://www.toutiao.com/ch/cba/',
        'https://www.toutiao.com/ch/csl/',
        'https://www.toutiao.com/ch/football_italy/',
        'https://www.toutiao.com/ch/news_car/',
        'https://www.toutiao.com/ch/car_new_arrival/',
        'https://www.toutiao.com/ch/suv/',
        'https://www.toutiao.com/ch/car_guide/',
        'https://www.toutiao.com/ch/car_usage/',
        'https://www.toutiao.com/ch/news_finance/',
        'https://www.toutiao.com/ch/investment/',
        'https://www.toutiao.com/ch/stock_channel/',
        'https://www.toutiao.com/ch/finance_management/',
        'https://www.toutiao.com/ch/macro_economic/',
        'https://www.toutiao.com/ch/funny/',
        'https://www.toutiao.com/ch/news_military/',
        'https://www.toutiao.com/ch/military_china/',
        'https://www.toutiao.com/ch/weaponry/',
        'https://www.toutiao.com/ch/military_world/',
        'https://www.toutiao.com/ch/news_world/',
        'https://www.toutiao.com/ch/news_fashion/',
        'https://www.toutiao.com/ch/fashion/',
        'https://www.toutiao.com/ch/body_shaping/',
        'https://www.toutiao.com/ch/watch/',
        'https://www.toutiao.com/ch/jewelry/',
        'https://www.toutiao.com/ch/news_travel/',
        'https://www.toutiao.com/ch/news_discovery/',
        'https://www.toutiao.com/ch/news_baby/',
        'https://www.toutiao.com/ch/news_regimen/',
        'https://www.toutiao.com/ch/news_essay/',
        'https://www.toutiao.com/ch/news_history/',
        'https://www.toutiao.com/ch/news_food/'
    ]
    headers = {
        "authority": "www.toutiao.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        url = response.url
        yield SplashRequest(url, endpoint='execute', args={'lua_source': lua1},
                            cache_args=['lua_source'])

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//div[contains(@class,"feedBox")]').xpath(
            '//a[contains(@href, "group")][contains(@class, "title")]/@href').extract()
        urls = set()
        panduan = Panduan_JRTT()
        db_url = panduan.panduan()
        for link in links:
            link_ = 'https://www.toutiao.com' + link
            if link_ not in db_url:
                urls.add(link_)
            else:
                print(link_, '--重复')
        for url in urls:
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'url':link},
                                args={
                                    'lua_source': lua2,
                                    'headers': self.headers,
                                    'wait': 2},
                                encoding='utf-8', cache_args=['lua_source'], endpoint='execute')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath(
            '/html/body/div/div[2]/div[2]/div[1]/h1/text()').extract_first()
        if title:
            # AuthorID
            # 文章作者ID
            AuthorID = ''

            # AuthorName
            # 文章作者名称
            AuthorName = sele.xpath(
                '/html/body/div/div[2]/div[2]/div[1]/div[1]/span[1]/text()').extract_first()

            # ArticleTitle
            # 文章标题
            ArticleTitle = title

            # SourceArticleURL
            # 原文章链接
            SourceArticleURL = response.url

            # URL
            # 文章链接
            URL = SourceArticleURL

            # PublishTime
            # 文章发表时间
            PublishTime = sele.xpath(
                '/html/body/div/div[2]/div[2]/div[1]/div[1]/span[2]/text()').extract_first()
            if '2018' not in PublishTime:
                PublishTime = sele.xpath(
                    '/html/body/div/div[2]/div[2]/div[1]/div[1]/span[3]/text()').extract_first()
            # Crawler
            # 文章爬取时间
            Crawler = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # ReadCount
            # 文章阅读数量
            ReadCount = ''

            # CommentCount
            # 文章回复数量
            CommentCount = sele.xpath(
                '/html/body/div/div[2]/div[1]/div/a/span/text()').extract_first()

            # TransmitCount
            # 文章转发数量
            TransmitCount = ''

            # Content
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[contains(@class,"article-content")]//p/text()').extract()
            for body in Contents:
                Content = Content + str(body)

            # AgreeCount
            # 赞同人数
            AgreeCount = ''

            # DisagreeCount
            # 反对人数
            DisagreeCount = ''

            # AskCount
            # 提问人数
            AskCount = ''

            # ParticipateCount
            # 参与人数
            ParticipateCount = ''

            # CollectionCount
            # 收藏数
            CollectionCount = ''

            # Classification
            # 文章分类
            Classification = sele.xpath(
                '/html/body/div/div[1]/div[2]/div/div[2]/a[2]/text()').extract_first()

            # Labels
            # 文章标签
            Labels = sele.xpath(
                '//li[contains(@class, "tag-item")]/a/text()').extract_first()

            # RewardCount
            # 打赏次数
            RewardCount = ''

            # comments
            # 评论总字段

            comments_list = []
            comments_sele = sele.xpath('//*[@id="comment"]')
            comments_sele_list = comments_sele.xpath(
                '//li[contains(@class, "c-item")]')
            for i in range(len(comments_sele_list)):
                comments = {}
                # commentPublishTime
                # 评论时间
                # 时间格式YYYY - MM - DD
                # HH: mm:ss
                commentPublishTime = comments_sele_list.xpath(
                    '//span[contains(@class, "c-create-time")]/text()')[i].extract()
                comments['commentPublishTime'] = commentPublishTime

                # commentReplyTargetType
                # 评论对象的类型
                # 正文
                # 或者
                # 回复
                commentReplyTargetType = '正文'
                comments['commentReplyTargetType'] = commentReplyTargetType

                # commentArticleID
                # 评论所属文章ID
                commentArticleID = URL.split('group/')[1].replace('/', '')
                comments['commentArticleID'] = commentArticleID

                # commentAuthorID
                # 评论者ID
                commentAuthorID = comments_sele_list.xpath(
                    '//a[contains(@class, "c-user-name")]/@href')[i].extract().split('user/')[1].replace('/', '')
                comments['commentAuthorID'] = commentAuthorID

                # commentAuthorName
                # 评论者名称
                commentAuthorName = comments_sele_list.xpath(
                    '//a[contains(@class, "c-user-name")]/text()')[i].extract()
                comments['commentAuthorName'] = commentAuthorName

                # commentContent
                # 评论内容
                commentContent = comments_sele_list.xpath(
                    '//div[contains(@class, "c-content")]/p/text()')[i].extract()
                comments['commentContent'] = commentContent

                # commentAgreeCount
                # 赞同数
                commentAgreeCount = comments_sele_list.xpath(
                    '//span[contains(@title, "点赞")]/text()')[i].extract()
                comments['commentAgreeCount'] = str(
                    commentAgreeCount).replace('\xa0', '')

                # commentDisagreeCount
                # 反对数
                commentDisagreeCount = comments_sele_list.xpath(
                    '//span[contains(@title, "举报")]/text()').extract()
                comments['commentDisagreeCount'] = str(
                    commentDisagreeCount).replace('\xa0', '')

                comments_list.append(comments)
            item = Yuqing_JRTTItem({
                'AuthorID': AuthorID,
                'AuthorName': AuthorName,
                'ArticleTitle': title,
                'SourceArticleURL': response.url,
                'URL': response.url,
                'PublishTime': PublishTime,
                'Crawler': Crawler,
                'ReadCount': ReadCount,
                'CommentCount': CommentCount,
                'TransmitCount': TransmitCount,
                'Content': Content,
                'comments': str(comments_list),
                'AgreeCount': AgreeCount,
                'DisagreeCount': DisagreeCount,
                'AskCount': AskCount,
                'ParticipateCount': ParticipateCount,
                'CollectionCount': CollectionCount,
                'Classification': Classification,
                'Labels': Labels,
                'Type': '',
                'RewardCount': ''
            })

            yield item
