# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
from scrapy import Selector
from scrapy_splash import SplashRequest
from yuqing100.items import Yuqing_HuxiuwangItem
from yuqing100.pipelines import Panduan_Huxiuwang


lua1 = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(5)
    splash:runjs("document.getElementsByClassName('get-mod-more transition js-comment-get-more')[0].click()")
    splash:wait(5)
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


class HuxiuwangSpider(scrapy.Spider):
    name = 'Huxiuwang_Spider'
    start_urls = [
        'https://www.huxiu.com/'
    ]
    headers = {
        "Host": "www.huxiu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Referer":"https://www.huxiu.com/"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_url, dont_filter=True, headers=self.headers)

    def parse_url(self, response):
        url = response.url
        yield SplashRequest(url, endpoint='execute', args={'lua_source': lua2, 'headers': self.headers, 'wait': 2},
                            cache_args=['lua_source'])

    def parse(self, response):
        sele = Selector(response)
        links = sele.xpath('//h2/a/@href').extract()
        urls = set()
        panduan = Panduan_Huxiuwang()
        db_url = panduan.panduan()
        for link in links:
            link = 'https://www.huxiu.com' + link
            if link not in db_url:
                urls.add(link)
        for url in urls:
            yield SplashRequest(url=url,
                                callback=self.parse1,
                                # meta={'url':link},
                                args={'lua_source': lua1, 'headers': self.headers, 'wait': 2},
                                encoding='utf-8',cache_args=['lua_source'])

    def parse1(self, response):
        sele = Selector(response)
        title = sele.xpath('//title/text()').extract_first()
        if title:
            # AuthorID
            # 文章作者ID
            AuthorID = sele.xpath('//div[@class="author-name"]/a/@href').extract_first().replace('/member/','').replace('.html','')

            # AuthorName
            # 文章作者名称
            AuthorName = sele.xpath('//meta[@name="author"]/@content').extract_first()

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
            PublishTime = sele.xpath('//span[contains(@class,"article-time")]/text()').extract_first()
            # if '2018' not in PublishTime:
            #     PublishTime = sele.xpath(
            #         '/html/body/div/div[2]/div[2]/div[1]/div[1]/span[3]/text()').extract_first()
            # Crawler
            # 文章爬取时间
            Crawler = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # ReadCount
            # 文章阅读数量
            ReadCount = ''

            # CommentCount
            # 文章回复数量
            CommentCount = sele.xpath('//span[contains(@class,"article-pl")]/text()').extract_first().replace('评论','')

            # TransmitCount
            # 文章转发数量
            TransmitCount = ''

            # Content
            # 文章正文内容
            Content = ''
            Contents = sele.xpath(
                '//div[contains(@class,"article-content-wrap")]//p/text()').extract()
            for body in Contents:
                Content = Content + str(body)

            # AgreeCount
            # 赞同人数
            AgreeCount = sele.xpath('//div[@class="Qr-code"]//span[@class="num"]/text()').extract_first()

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
            CollectionCount = sele.xpath('//span[contains(@class,"article-share")]/text()').extract_first().replace('收藏','')

            # Classification
            # 文章分类
            Classification = sele.xpath('//div[@class="column-link-box"]/a/text()').extract_first()

            # Labels
            # 文章标签
            Labels = sele.xpath('//meta[@name="keywords"]/@content').extract_first()

            # RewardCount
            # 打赏次数
            RewardCount = ''

            # comments
            # 评论总字段

            comments_list = []
            comments_seles = sele.xpath('//div[@id="g_pid"]')
            print(len(comments_seles))
            for comments_sele in comments_seles:
                comments = {}
                # commentPublishTime
                # 评论时间
                # 时间格式YYYY - MM - DD
                # HH: mm:ss
                commentPublishTime = comments_sele.xpath('.//span[contains(@class, "comment-yh-time")]/text()').extract_first()
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
                commentArticleID = URL.split('article/')[1].replace('.html', '')
                comments['commentArticleID'] = commentArticleID

                # commentAuthorID
                # 评论者ID
                commentAuthorID = comments_sele.xpath('.//span[contains(@class, "author-comment-name")]/a/@href').extract()[0].split('/member/')[1].replace('.html', '')
                comments['commentAuthorID'] = commentAuthorID

                # commentAuthorName
                # 评论者名称
                commentAuthorName = comments_sele.xpath('.//span[contains(@class, "author-comment-name")]/a/text()').extract_first()
                comments['commentAuthorName'] = commentAuthorName

                # commentContent
                # 评论内容
                commentContent = comments_sele.xpath('.//div[@class="pl-content pl-yh-content"]/div[@class="pull-left "]/text()').extract_first()
                comments['commentContent'] = commentContent

                # commentAgreeCount
                # 赞同数
                commentAgreeCount = comments_sele.xpath('.//div[@class="dropdown pull-right pl-yh-zan"]/span/text()').extract_first()
                comments['commentAgreeCount'] = str(
                    commentAgreeCount).replace('\xa0', '')

                # commentDisagreeCount
                # 反对数
                commentDisagreeCount = ''
                comments['commentDisagreeCount'] = commentDisagreeCount

                comments_list.append(comments)

            item = Yuqing_HuxiuwangItem({
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

