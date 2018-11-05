# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_AfItem
from yuqing100.pipelines import Panduan_Af


class AfSpider(scrapy.Spider):
    name = 'Af_Spider'
    allowed_domains = ['www.ifanr.com']
    start_urls = [
        'https://www.ifanr.com/app?page=1&pajax=1&post_id__lt=&show_type=list'
    ]
    headers = {
        "user-agent":"ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse,
                                args={'headers': self.headers,'wait': 5 , 'timeout':10})



    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//h3/a/@href').extract()
        panduan = Panduan_Af()
        db_url = panduan.panduan()
        urls = set()
        for link in links:
            urls.add(link)
        for url in urls:
            if url not in db_url:
                yield SplashRequest(url=url,
                                    callback=self.parse1,
                                    # meta={'data_time':data_time},
                                    args={'headers': self.headers, 'wait': 20,'timeout':60},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # AuthorID
            # 文章作者ID
            AuthorID = ''

            # AuthorName
            # 文章作者名称
            AuthorName = sele.xpath('//p[@class="c-card-author__name"]/text()').extract_first()

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
            PublishTime = sele.xpath('//meta[contains(@name, "article:create_at")]/@content').extract_first()

            # Crawler
            # 文章爬取时间
            Crawler = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # ReadCount
            # 文章阅读数量
            ReadCount = ''

            # CommentCount
            # 文章回复数量
            CommentCount = sele.xpath('//p[@class="js-placeholder-comments-counter"]/text()').extract_first()

            # TransmitCount
            # 文章转发数量
            TransmitCount = ''

            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//article[@class="o-single-content__body__content c-article-content s-single-article js-article"]//text()').extract()
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
            Classification = ''

            # Labels
            # 文章标签
            Labels = sele.xpath('//meta[contains(@name, "keywords")]/@content').extract_first()

            # RewardCount
            # 打赏次数
            RewardCount = ''

            # comments
            # 评论总字段

            comments_list = []
            lis = sele.xpath('//li[@class="c-article-comments-item"]')
            for li in lis:
                comments = {}
                # commentPublishTime
                # 评论时间
                # 时间格式YYYY - MM - DD
                # HH: mm:ss
                commentPublishTime = li.xpath('.//div[@class="c-article-comments-item__meta"]/text()').extract_first()
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
                commentArticleID = ''
                comments['commentArticleID'] = commentArticleID

                # commentAuthorID
                # 评论者ID
                commentAuthorID = URL.replace('https://www.ifanr.com/','')
                comments['commentAuthorID'] = commentAuthorID

                # commentAuthorName
                # 评论者名称
                commentAuthorName = li.xpath('.//span[@class="c-article-comments-item__name"]/text()').extract_first()
                comments['commentAuthorName'] = commentAuthorName

                # commentContent
                # 评论内容
                commentContents = li.xpath('.//div[@class="c-article-comments-item__content"]//text()').extract()
                commentContent = ''
                for body in commentContents:
                    commentContent = commentContent + str(body)
                comments['commentContent'] = commentContent

                # commentAgreeCount
                # 赞同数
                commentAgreeCount = li.xpath('.//button[@class="c-article-comments-item-voting c-article-comments-item-voting--up js-vote-up "]/text()').extract_first()
                comments['commentAgreeCount'] = str(
                    commentAgreeCount).replace('\xa0', '')

                # commentDisagreeCount
                # 反对数
                commentDisagreeCount = li.xpath('.//button[@class="c-article-comments-item-voting c-article-comments-item-voting--down js-vote-down "]/text()').extract_first()
                comments['commentDisagreeCount'] = str(
                    commentDisagreeCount).replace('\xa0', '')

                comments_list.append(comments)
            item = Yuqing_AfItem({
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
            # print(item)