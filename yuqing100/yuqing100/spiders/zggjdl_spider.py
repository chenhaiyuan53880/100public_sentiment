# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
# from yuqing100.items import Yuqing_JRTTItem
# from yuqing100.pipelines import Panduan_JRTT


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


class ZggjdlSpider(scrapy.Spider):
    name = 'Zggjdl_Spider'
    allowed_domains = ['www.dili360.com']
    start_urls = [
        'http://www.dili360.com/bbs/column/6541.htm'
    ]
    headers = {
        "Host": "www.dili360.com"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                args={'headers': self.headers, 'wait': 2},
                                encoding='utf-8')

    def parse(self, response):
        sele = Selector(response)
        lis = sele.xpath('//ul[@class="article-list"]//li')
        # urls = set()
        # panduan = Panduan_JRTT()
        # db_url = panduan.panduan()
        # for link in links:
        #     link_ = 'https://www.toutiao.com' + link
        #     if link_ not in db_url:
        #         urls.add(link_)
        #     else:
        #         print(link_, '--重复')
        for li in lis:
            url = li.xpath('.//h3/a/@href').extract_first()
            url = 'http://www.dili360.com' + url
            author = li.xpath('.//p[@class="tips"]/a/text()').extract_first()
            publishtime = li.xpath('.//p[@class="tips"]/text()').extract()[1].replace('\xa0\n','').replace(' ','')
            commentcount = li.xpath('.//div[@class="icon icon-comment"]/text()').extract_first()
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                meta={'author':author,'publishtime':publishtime,'commentcount':commentcount},
                                args={
                                    'headers': self.headers,
                                    'wait': 5},
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
            AuthorName = response.meta['author']

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
            PublishTime = response.meta['publishtime']
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
                '//section//text()').extract()
            for body in Contents:
                Content = Content + str(body)

            # AgreeCount
            # 赞同人数
            AgreeCount = sele.xpath(
                '//li[@class="icon icon-heart"]/text()').extract_first()

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
            Labels = sele.xpath(
                '//meta[@name="keywords"]//@content').extract_first()

            # RewardCount
            # 打赏次数
            RewardCount = ''

            # comments
            # 评论总字段
            comments_list = []
            comments_sele_lists = sele.xpath('//ul[@class="content"]//li')

            # CommentCount
            # 文章回复数量
            CommentCount = response.meta['commentcount']


            for comments_sele_list in comments_sele_lists:
                comments = {}
                # commentPublishTime
                # 评论时间
                # 时间格式YYYY - MM - DD
                # HH: mm:ss
                commentPublishTime = comments_sele_list.xpath(
                    './/div[@class="control"]/span/text()').extract_first()
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

                commentAuthorID = ''
                comments['commentAuthorID'] = commentAuthorID

                # commentAuthorName
                # 评论者名称
                commentAuthorName = comments_sele_list.xpath(
                    './/h3/text()').extract_first()
                comments['commentAuthorName'] = commentAuthorName

                # commentContent
                # 评论内容
                commentContent = comments_sele_list.xpath(
                    './/ul[@class="tags"]/li/text()').extract_first()
                comments['commentContent'] = commentContent

                # commentAgreeCount
                # 赞同数
                commentAgreeCount = comments_sele_list.xpath(
                    './/div[@class="part-one"]/text()').extract_first()
                comments['commentAgreeCount'] = str(
                    commentAgreeCount).replace('赞', '').replace('(', '').replace(')', '')

                # commentDisagreeCount
                # 反对数
                commentDisagreeCount = ''
                comments['commentDisagreeCount'] = str(
                    commentDisagreeCount).replace('\xa0', '')

                comments_list.append(comments)
            item = {
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
            }

            # yield item
            print(item)