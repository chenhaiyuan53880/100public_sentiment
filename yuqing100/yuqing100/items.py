# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Yuqing_banyuetanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    AuthorID = scrapy.Field()
    AuthorName = scrapy.Field()
    ArticleTitle = scrapy.Field()
    SourceArticleURL = scrapy.Field()
    URL = scrapy.Field()
    PublishTime = scrapy.Field()
    Crawler = scrapy.Field()
    ReadCount = scrapy.Field()
    CommentCount = scrapy.Field()
    TransmitCount = scrapy.Field()
    Content = scrapy.Field()
    comments = scrapy.Field()
    AgreeCount = scrapy.Field()
    DisagreeCount = scrapy.Field()
    AskCount = scrapy.Field()
    ParticipateCount = scrapy.Field()
    CollectionCount = scrapy.Field()
    Classification = scrapy.Field()
    Labels = scrapy.Field()
    Type = scrapy.Field()
    RewardCount = scrapy.Field()

class Yuqing_sansijiaoyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    AuthorID = scrapy.Field()
    AuthorName = scrapy.Field()
    ArticleTitle = scrapy.Field()
    SourceArticleURL = scrapy.Field()
    URL = scrapy.Field()
    PublishTime = scrapy.Field()
    Crawler = scrapy.Field()
    ReadCount = scrapy.Field()
    CommentCount = scrapy.Field()
    TransmitCount = scrapy.Field()
    Content = scrapy.Field()
    comments = scrapy.Field()
    AgreeCount = scrapy.Field()
    DisagreeCount = scrapy.Field()
    AskCount = scrapy.Field()
    ParticipateCount = scrapy.Field()
    CollectionCount = scrapy.Field()
    Classification = scrapy.Field()
    Labels = scrapy.Field()
    Type = scrapy.Field()
    RewardCount = scrapy.Field()

class Yuqing_nanfrwzkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    AuthorID = scrapy.Field()
    AuthorName = scrapy.Field()
    ArticleTitle = scrapy.Field()
    SourceArticleURL = scrapy.Field()
    URL = scrapy.Field()
    PublishTime = scrapy.Field()
    Crawler = scrapy.Field()
    ReadCount = scrapy.Field()
    CommentCount = scrapy.Field()
    TransmitCount = scrapy.Field()
    Content = scrapy.Field()
    comments = scrapy.Field()
    AgreeCount = scrapy.Field()
    DisagreeCount = scrapy.Field()
    AskCount = scrapy.Field()
    ParticipateCount = scrapy.Field()
    CollectionCount = scrapy.Field()
    Classification = scrapy.Field()
    Labels = scrapy.Field()
    Type = scrapy.Field()
    RewardCount = scrapy.Field()

class Yuqing_lianhezaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    AuthorID = scrapy.Field()
    AuthorName = scrapy.Field()
    ArticleTitle = scrapy.Field()
    SourceArticleURL = scrapy.Field()
    URL = scrapy.Field()
    PublishTime = scrapy.Field()
    Crawler = scrapy.Field()
    ReadCount = scrapy.Field()
    CommentCount = scrapy.Field()
    TransmitCount = scrapy.Field()
    Content = scrapy.Field()
    comments = scrapy.Field()
    AgreeCount = scrapy.Field()
    DisagreeCount = scrapy.Field()
    AskCount = scrapy.Field()
    ParticipateCount = scrapy.Field()
    CollectionCount = scrapy.Field()
    Classification = scrapy.Field()
    Labels = scrapy.Field()
    Type = scrapy.Field()
    RewardCount = scrapy.Field()


class Yuqing_heimawangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    AuthorID = scrapy.Field()
    AuthorName = scrapy.Field()
    ArticleTitle = scrapy.Field()
    SourceArticleURL = scrapy.Field()
    URL = scrapy.Field()
    PublishTime = scrapy.Field()
    Crawler = scrapy.Field()
    ReadCount = scrapy.Field()
    CommentCount = scrapy.Field()
    TransmitCount = scrapy.Field()
    Content = scrapy.Field()
    comments = scrapy.Field()
    AgreeCount = scrapy.Field()
    DisagreeCount = scrapy.Field()
    AskCount = scrapy.Field()
    ParticipateCount = scrapy.Field()
    CollectionCount = scrapy.Field()
    Classification = scrapy.Field()
    Labels = scrapy.Field()
    Type = scrapy.Field()
    RewardCount = scrapy.Field()

class Kepu_tupian(scrapy.Item):
    Title = scrapy.Field()
    PublishTime = scrapy.Field()
    Content = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()


