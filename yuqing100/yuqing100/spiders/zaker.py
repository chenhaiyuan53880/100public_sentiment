# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.models import datefilter
from yuqing100.items import Yuqing_ZakerItem
from yuqing100.pipelines import Panduan_Zaker

class ZakerSpider(scrapy.Spider):
    name = 'Zaker_Spider'
    allowed_domains = ['www.myzaker.com']
    start_urls = [
        'http://www.myzaker.com/channel/9'
    ]
    headers = {
        "Host": "www.myzaker.com",
        "Referer":"http://www.myzaker.com/channel/660",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2})



    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//div[@class="figure flex-block"]')
        panduan = Panduan_Zaker()
        db_url = panduan.panduan()
        for link in links:
            url = link.xpath('.//h2[@class="figcaption"]/a/@href').extract_first()
            url = url.replace('//','http://')
            if url not  in db_url:
                try:
                    num = link.xpath('.//div[@class="subtitle"]//span/text()').extract()[2]
                except:
                    num = '0'
                yield SplashRequest(url=url,
                                    callback=self.parse1,
                                    meta={'num':num},
                                    args={'headers': self.headers, 'wait': 2},
                                    encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # AuthorID
            # 文章作者ID
            AuthorID = sele.xpath('//div[@class="article_tips"]/a/@href').extract_first().split('source/')[1]

            # AuthorName
            # 文章作者名称
            AuthorName = sele.xpath('//span[@class="auther"]/text()').extract_first()

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
            PublishTime = sele.xpath('//span[@class="time"]/text()').extract_first()

            # if '2018' not in PublishTime:
            #     PublishTime = sele.xpath(
            #         '/html/body/div/div[2]/div[2]/div[1]/div[1]/span[3]/text()').extract_first()
            # Crawler
            # 文章爬取时间
            Crawler = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            PublishTime = datefilter(PublishTime,Crawler)
            # ReadCount
            # 文章阅读数量
            ReadCount = ''

            # CommentCount
            # 文章回复数量
            CommentCount = response.meta['num'].replace('评论','')

            # TransmitCount
            # 文章转发数量
            TransmitCount = ''

            # Content
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@id="content"]//text()').extract()
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
            Labels = sele.xpath('//meta[@name="keywords"]/text()').extract_first()

            # RewardCount
            # 打赏次数
            RewardCount = ''

            # comments
            # 评论总字段

            comments_list = []
            comments_seles = sele.xpath('//div[@class="comment_item "]')
            for comments_sele in comments_seles:
                comments = {}
                # commentPublishTime
                # 评论时间
                # 时间格式YYYY - MM - DD
                # HH: mm:ss
                commentPublishTime = comments_sele.xpath(
                    './/div[@class="comment_time"]/text()').extract_first()
                commentPublishTime = datefilter(commentPublishTime, Crawler)
                comments['commentPublishTime'] = str(commentPublishTime)

                # commentReplyTargetType
                # 评论对象的类型x`
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
                commentAuthorID = ''
                comments['commentAuthorID'] = commentAuthorID

                # commentAuthorName
                # 评论者名称
                commentAuthorName = comments_sele.xpath(
                    './/div[@class="comment_title author"]/text()').extract_first()
                comments['commentAuthorName'] = commentAuthorName

                # commentContent
                # 评论内容
                commentContent = comments_sele.xpath(
                    './/div[@class="comment_desc con"]/text()').extract_first()
                comments['commentContent'] = commentContent

                # commentAgreeCount
                # 赞同数
                commentAgreeCount = comments_sele.xpath(
                    './/div[@class="comment_zan like_num"]/text()').extract_first()
                comments['commentAgreeCount'] = str(
                    commentAgreeCount).replace('\xa0', '')

                # commentDisagreeCount
                # 反对数
                commentDisagreeCount = ''
                comments['commentDisagreeCount'] = commentDisagreeCount

                comments_list.append(comments)

            item = Yuqing_ZakerItem({
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