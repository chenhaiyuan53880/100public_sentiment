# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_GuokeItem
from yuqing100.pipelines import Panduan_Guoke


class GuokeSpider(scrapy.Spider):
    name = 'Guoke_Spider'
    allowed_domains = ['www.guokr.com']
    start_urls = [
        'https://www.guokr.com/scientific/'
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
        panduan = Panduan_Guoke()
        db_url = panduan.panduan()
        urls = set()
        for link in links:
            urls.add(link)
        for url in links:
            if url not in db_url:
                yield SplashRequest(url=url,
                                    callback=self.parse1,
                                    # meta={'data_time':data_time},
                                    args={'headers': self.headers, 'wait': 10,'timeout':60},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # AuthorID
            # 文章作者ID
            try:
                AuthorID = sele.xpath('//div[@class="content-th-info"]/a/@href').extract_first().split('/i/',1)[1].replace('/','')
            except:
                AuthorID = ''

            # AuthorName
            # 文章作者名称
            AuthorName = sele.xpath('//meta[@property="article:author"]/@content').extract_first()

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
            PublishTime = sele.xpath('//meta[@property="article:published_time"]/@content').extract_first().split(':',1)[0]

            # Crawler
            # 文章爬取时间
            Crawler = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # ReadCount
            # 文章阅读数量
            ReadCount = ''

            # CommentCount
            # 文章回复数量
            CommentCount = sele.xpath('//div[@class="gfl"]/text()').extract_first().replace('全部评论(','').replace(')','')

            # TransmitCount
            # 文章转发数量
            TransmitCount = ''

            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="document"]//text()').extract()
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
            Labels = sele.xpath('//meta[contains(@name, "Keywords")]/@content').extract_first()

            # RewardCount
            # 打赏次数
            RewardCount = ''

            # comments
            # 评论总字段

            comments_list = []
            lis = sele.xpath('//ul[@class="cmts-list cmts-all cmts-hide"]//li')
            for li in lis:
                comments = {}
                # commentPublishTime
                # 评论时间
                # 时间格式YYYY - MM - DD
                # HH: mm:ss
                commentPublishTime = li.xpath('.//span[@class="cmt-info"]/text()').extract_first()
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
                commentArticleID = URL.split('/article/',1)[1].replace('/','')
                comments['commentArticleID'] = commentArticleID

                # commentAuthorID
                # 评论者ID
                commentAuthorID = li.xpath('.//a[@class="cmt-author cmtAuthor"]/@href').extract_first().split('/i/',1)[1].replace('/','')
                comments['commentAuthorID'] = commentAuthorID

                # commentAuthorName
                # 评论者名称
                commentAuthorName = li.xpath('.//a[@class="cmt-author cmtAuthor"]/text()').extract_first()
                comments['commentAuthorName'] = commentAuthorName

                # commentContent
                # 评论内容
                commentContents = li.xpath('.//div[@class="cmt-content gbbcode-content cmtContent"]//text()').extract()
                commentContent = ''
                for body in commentContents:
                    commentContent = commentContent + str(body)
                comments['commentContent'] = commentContent

                # commentAgreeCount
                # 赞同数
                commentAgreeCount = li.xpath('.//span[@class="cmt-do-num"]/text()').extract_first()
                comments['commentAgreeCount'] = str(
                    commentAgreeCount).replace('\xa0', '')

                # commentDisagreeCount
                # 反对数
                commentDisagreeCount = ''
                comments['commentDisagreeCount'] = str(
                    commentDisagreeCount).replace('\xa0', '')

                comments_list.append(comments)
            item = Yuqing_GuokeItem({
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