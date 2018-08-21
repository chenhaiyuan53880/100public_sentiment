# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_DoubanItem
from yuqing100.pipelines import Panduan_Douban


class DoubanSpider(scrapy.Spider):
    name = 'Douban_spider'
    start_urls = [
        'https://www.douban.com/group/explore/culture',
        'https://www.douban.com/group/explore/travel',
        'https://www.douban.com/group/explore/ent',
        'https://www.douban.com/group/explore/fashion',
        'https://www.douban.com/group/explore/life',
        'https://www.douban.com/group/explore/tech'
    ]
    headers = {
        "Host": "www.douban.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 4},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        sele_first = sele.xpath('//*[@id="content"]/div/div[1]')
        sele_divs = sele_first.xpath('.//div[@class="channel-item"]')
        panduan = Panduan_Douban()
        db_url = panduan.panduan()
        for sele_div in sele_divs:
            url = sele_div.xpath('.//h3/a/@href').extract_first()
            like = sele_div.xpath('.//div[@class="likes"]/text()').extract_first()
            if url not in db_url:
                yield SplashRequest(url=url,
                                callback=self.parse1,
                                meta={'like':like},
                                args={'headers': self.headers, 'wait': 5},
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
            AuthorName = sele.xpath(
                '//div[@class="topic-doc"]//a/text()').extract_first()

            # ArticleTitle
            # 文章标题
            ArticleTitle = title.replace('\n','')

            # SourceArticleURL
            # 原文章链接
            SourceArticleURL = response.url

            # URL
            # 文章链接
            URL = SourceArticleURL

            # PublishTime
            # 文章发表时间
            PublishTime = sele.xpath(
                '//*[@id="content"]//div[@class="article"]//h3/span[2]/text()').extract_first()
            # if '2018' not in PublishTime:
            #     PublishTime = sele.xpath(
            #         '/html/body/div/div[2]/div[2]/div[1]/div[1]/span[3]/text()').extract_first()
            # Crawler
            # 文章爬取时间
            Crawler = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # ReadCount
            # 文章阅读数量
            ReadCount = ''



            # TransmitCount
            # 文章转发数量
            TransmitCount = ''

            # Content
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[contains(@class,"topic-richtext")]//p/text()').extract()
            for body in Contents:
                Content = Content + str(body)

            # AgreeCount
            # 赞同人数
            AgreeCount = response.meta['like']

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
            Labels = ''

            # RewardCount
            # 打赏次数
            RewardCount = ''

            # comments
            # 评论总字段
            comments_list = []
            comments_sele = sele.xpath('//*[@id="comments"]')
            comments_sele_lists = comments_sele.xpath(
                '//li[contains(@class, "comment-item")]')

            # CommentCount
            # 文章回复数量
            CommentCount = str(len(comments_sele_lists))


            for comments_sele_list in comments_sele_lists:
                comments = {}
                # commentPublishTime
                # 评论时间
                # 时间格式YYYY - MM - DD
                # HH: mm:ss
                commentPublishTime = comments_sele_list.xpath(
                    './/span[contains(@class, "pubtime")]/text()').extract_first()
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
                commentAuthorID = comments_sele_list.xpath(
                    './/h4/a/@href').extract_first().split('people/')[1].replace('/', '')
                comments['commentAuthorID'] = commentAuthorID

                # commentAuthorName
                # 评论者名称
                commentAuthorName = comments_sele_list.xpath(
                    './/h4/a/text()').extract_first()
                comments['commentAuthorName'] = commentAuthorName

                # commentContent
                # 评论内容
                commentContent = comments_sele_list.xpath(
                    './/p/text()').extract_first()
                comments['commentContent'] = commentContent

                # commentAgreeCount
                # 赞同数
                commentAgreeCount = comments_sele_list.xpath(
                    './/a[contains(@class, "comment-vote")]/text()').extract()
                comments['commentAgreeCount'] = str(
                    commentAgreeCount).replace('赞', '').replace('(', '').replace(')', '')

                # commentDisagreeCount
                # 反对数
                commentDisagreeCount = ''
                comments['commentDisagreeCount'] = str(
                    commentDisagreeCount).replace('\xa0', '')

                comments_list.append(comments)
            item = Yuqing_DoubanItem({
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