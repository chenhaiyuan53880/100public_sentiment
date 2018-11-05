# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_YibanItem
from yuqing100.pipelines import Panduan_Yiban
from yuqing100.models import datefilter


lua1 = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementsByClassName('yiban-loading')[0].scrollIntoView(true)")
    splash:wait(2)
    return splash:html()
    end
 '''

lua2 = '''
function main(splash)
    splash:go(splash.args.url)
    splash:runjs("document.getElementsByClassName('get-mod-more js-get-mod-more-list transition')[0].click()")
    splash:wait(2)
    return splash:html()
    end
 '''


class YibanSpider(scrapy.Spider):
    name = 'Yiban_Spider'
    start_urls = [
        'http://www.yiban.cn/square/index',
        'http://www.yiban.cn/square/index/page/2'
    ]
    headers = {
        "Host": "www.yiban.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Referer":"http://www.yiban.cn/"
    }

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield Request(url, callback=self.parse_url, dont_filter=True, headers=self.headers)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'headers': self.headers, 'wait': 5},dont_filter=True)

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//ul[@class="yiban-member-list"]//h4//a/@href').extract()
        # urls = set()

        for link in links:
            link = 'http://www.yiban.cn' + link
            # if link not in db_url:
            #     urls.add(link)
            # print(link)
            yield SplashRequest(url=link,
                                callback=self.parse1,
                                # meta={'url':link},
                                args={'headers': self.headers, 'wait': 5},
                                encoding='utf-8')

    def parse1(self, response):
        sele = Selector(response)
        links = sele.xpath('//h5/a/@href').extract()
        Classification = sele.xpath('//h2/text()').extract_first()
        panduan = Panduan_Yiban()
        db_url = panduan.panduan()
        for link in links:
            if 'http://news.fzu.edu.cn' not in link:
                if link not in db_url:
                #     urls.add(link)
                #     print(link)
                    yield SplashRequest(url=link,
                                        callback=self.parse2,
                                        meta={'Classification':Classification},
                                        args={'headers': self.headers, 'wait': 5},
                                        encoding='utf-8')
    def parse2(self, response):
        sele = Selector(response)
        title = sele.xpath('//h3/span/text()').extract_first()
        if title:
            # AuthorID
            # 文章作者ID
            AuthorID = sele.xpath('//div[@class="author-name"]/a/@href').extract_first().split('user_id/',1)[1]

            # AuthorName
            # 文章作者名称
            AuthorName = sele.xpath('//div[@class="author-name"]//span/text()').extract_first()

            # ArticleTitle
            # 文章标题
            ArticleTitle = title

            # SourceArticleURL
            # 原文章链接
            SourceArticleURL = response.url

            # URL
            # 文章链接
            URL = SourceArticleURL

            # Crawler
            # 文章爬取时间
            Crawler = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # PublishTime
            # 文章发表时间
            PublishTime = sele.xpath('//ul[@class="cf"]/li[2]/span/b/text()').extract_first()
            if '小时' in PublishTime:
                PublishTime = datefilter(PublishTime, Crawler)
            elif '2017' in PublishTime:
                pass
            else:
                PublishTime = '2018-' + PublishTime
                PublishTime = PublishTime.replace('2018- ','2018-')
                PublishTime = datefilter(PublishTime,Crawler)



            # ReadCount
            # 文章阅读数量
            ReadCount = sele.xpath('//ul[@class="cf"]/li[3]/span/b/text()').extract_first().replace('阅读数：','')

            # CommentCount
            # 文章回复数量
            try:
                CommentCount = sele.xpath('//div[@class="csort-left fl"]/span/b/text()').extract_first().replace('(','').replace(')','')
            except:
                CommentCount = 0

                # TransmitCount
            # 文章转发数量
            TransmitCount = ''

            # Content
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[@class="detail-forum-text"]//text()').extract()
            for body in Contents:
                Content = Content + str(body)

            # AgreeCount
            # 赞同人数
            AgreeCount = sele.xpath('//span[@class="good-number "]/text()').extract_first()

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
            Classification = response.meta['Classification']

            # Labels
            # 文章标签
            Labels = sele.xpath('//meta[@name="keywords"]/@content').extract_first()

            # RewardCount
            # 打赏次数
            RewardCount = ''

            # comments
            # 评论总字段

            comments_list = []
            comments_seles = sele.xpath('//div[@class="cl-item"]')
            # print(len(comments_seles))
            for comments_sele in comments_seles:
                comments = {}
                # commentPublishTime
                # 评论时间
                # 时间格式YYYY - MM - DD
                # HH: mm:ss
                commentPublishTime = comments_sele.xpath('.//div[@class="fl clir-date"]/span/text()').extract_first()
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
                try:
                    commentArticleID = URL.split('article_id/',1)[1]
                except:
                    commentArticleID = URL.split('id/', 1)[1]
                comments['commentArticleID'] = commentArticleID

                # commentAuthorID
                # 评论者ID
                try:
                    commentAuthorID = comments_sele.xpath('.//div[@class="cli-right"]/a[2]/@href').extract_first().split('user_id/')[1]
                except:
                    commentAuthorID = ''
                comments['commentAuthorID'] = commentAuthorID

                # commentAuthorName
                # 评论者名称
                commentAuthorName = comments_sele.xpath('.//div[@class="cli-right"]/a[2]/text()').extract_first()
                comments['commentAuthorName'] = commentAuthorName

                # commentContent
                # 评论内容
                commentContent = comments_sele.xpath('.//div[@class="clir-text"]/p/text()').extract_first()
                comments['commentContent'] = commentContent

                # commentAgreeCount
                # 赞同数
                commentAgreeCount = ''
                comments['commentAgreeCount'] = str(
                    commentAgreeCount).replace('\xa0', '')

                # commentDisagreeCount
                # 反对数
                commentDisagreeCount = ''
                comments['commentDisagreeCount'] = commentDisagreeCount

                comments_list.append(comments)

            item = Yuqing_YibanItem({
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