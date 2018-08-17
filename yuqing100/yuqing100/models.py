from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('mysql://test:test@192.168.10.114:3306/crawler_100?charset=utf8')
Base = declarative_base()

class Repository_banyuetan(Base):
    __tablename__ = 'last9997'
    id = Column(Integer, primary_key=True)
    AuthorID = Column(String(255))
    AuthorName = Column(String(255))
    ArticleTitle = Column(String(255))
    SourceArticleURL = Column(String(255))
    URL = Column(String(255))
    PublishTime = Column(String(255))
    Crawler = Column(String(255))
    ReadCount = Column(String(255))
    CommentCount = Column(String(255))
    TransmitCount = Column(String(255))
    Content = Column(Text())
    comments = Column(Text())
    AgreeCount = Column(String(255))
    DisagreeCount = Column(String(255))
    AskCount = Column(String(255))
    ParticipateCount = Column(String(255))
    CollectionCount = Column(String(255))
    Classification = Column(String(255))
    Labels = Column(String(255))
    Type = Column(String(255))
    RewardCount = Column(String(255))

class Repository_sansijiaoyu(Base):
    __tablename__ = 'last9996'
    id = Column(Integer, primary_key=True)
    AuthorID = Column(String(255))
    AuthorName = Column(String(255))
    ArticleTitle = Column(String(255))
    SourceArticleURL = Column(String(255))
    URL = Column(String(255))
    PublishTime = Column(String(255))
    Crawler = Column(String(255))
    ReadCount = Column(String(255))
    CommentCount = Column(String(255))
    TransmitCount = Column(String(255))
    Content = Column(Text())
    comments = Column(Text())
    AgreeCount = Column(String(255))
    DisagreeCount = Column(String(255))
    AskCount = Column(String(255))
    ParticipateCount = Column(String(255))
    CollectionCount = Column(String(255))
    Classification = Column(String(255))
    Labels = Column(String(255))
    Type = Column(String(255))
    RewardCount = Column(String(255))

class Repository_nanfrwzk(Base):
    __tablename__ = 'last9995'
    id = Column(Integer, primary_key=True)
    AuthorID = Column(String(255))
    AuthorName = Column(String(255))
    ArticleTitle = Column(String(255))
    SourceArticleURL = Column(String(255))
    URL = Column(String(255))
    PublishTime = Column(String(255))
    Crawler = Column(String(255))
    ReadCount = Column(String(255))
    CommentCount = Column(String(255))
    TransmitCount = Column(String(255))
    Content = Column(Text())
    comments = Column(Text())
    AgreeCount = Column(String(255))
    DisagreeCount = Column(String(255))
    AskCount = Column(String(255))
    ParticipateCount = Column(String(255))
    CollectionCount = Column(String(255))
    Classification = Column(String(255))
    Labels = Column(String(255))
    Type = Column(String(255))
    RewardCount = Column(String(255))

class Repository_lianhezaobao(Base):
    __tablename__ = 'last9994'
    id = Column(Integer, primary_key=True)
    AuthorID = Column(String(255))
    AuthorName = Column(String(255))
    ArticleTitle = Column(String(255))
    SourceArticleURL = Column(String(255))
    URL = Column(String(255))
    PublishTime = Column(String(255))
    Crawler = Column(String(255))
    ReadCount = Column(String(255))
    CommentCount = Column(String(255))
    TransmitCount = Column(String(255))
    Content = Column(Text())
    comments = Column(Text())
    AgreeCount = Column(String(255))
    DisagreeCount = Column(String(255))
    AskCount = Column(String(255))
    ParticipateCount = Column(String(255))
    CollectionCount = Column(String(255))
    Classification = Column(String(255))
    Labels = Column(String(255))
    Type = Column(String(255))
    RewardCount = Column(String(255))

class Repository_heimawang(Base):
    __tablename__ = 'last9993'
    id = Column(Integer, primary_key=True)
    AuthorID = Column(String(255))
    AuthorName = Column(String(255))
    ArticleTitle = Column(String(255))
    SourceArticleURL = Column(String(255))
    URL = Column(String(255))
    PublishTime = Column(String(255))
    Crawler = Column(String(255))
    ReadCount = Column(String(255))
    CommentCount = Column(String(255))
    TransmitCount = Column(String(255))
    Content = Column(Text())
    comments = Column(Text())
    AgreeCount = Column(String(255))
    DisagreeCount = Column(String(255))
    AskCount = Column(String(255))
    ParticipateCount = Column(String(255))
    CollectionCount = Column(String(255))
    Classification = Column(String(255))
    Labels = Column(String(255))
    Type = Column(String(255))
    RewardCount = Column(String(255))

class Repository_JRTT(Base):
    __tablename__ = 'last9992'
    id = Column(Integer, primary_key=True)
    AuthorID = Column(String(255))
    AuthorName = Column(String(255))
    ArticleTitle = Column(String(255))
    SourceArticleURL = Column(String(255))
    URL = Column(String(255))
    PublishTime = Column(String(255))
    Crawler = Column(String(255))
    ReadCount = Column(String(255))
    CommentCount = Column(String(255))
    TransmitCount = Column(String(255))
    Content = Column(Text())
    comments = Column(Text())
    AgreeCount = Column(String(255))
    DisagreeCount = Column(String(255))
    AskCount = Column(String(255))
    ParticipateCount = Column(String(255))
    CollectionCount = Column(String(255))
    Classification = Column(String(255))
    Labels = Column(String(255))
    Type = Column(String(255))
    RewardCount = Column(String(255))

class Repository_kepuchina(Base):
    __tablename__ = 'kepuchina_tuwen'
    id = Column(Integer, primary_key=True)
    Title = Column(String(255))
    PublishTime = Column(String(255))
    Content = Column(Text())
    url = Column(String(255))
    img_url = Column(String(255))
    img_path = Column(String(255))

class Repository_Cankaoxiaoxi(Base):
    __tablename__ = 'last9991'
    id = Column(Integer, primary_key=True)
    AuthorID = Column(String(255))
    AuthorName = Column(String(255))
    ArticleTitle = Column(String(255))
    SourceArticleURL = Column(String(255))
    URL = Column(String(255))
    PublishTime = Column(String(255))
    Crawler = Column(String(255))
    ReadCount = Column(String(255))
    CommentCount = Column(String(255))
    TransmitCount = Column(String(255))
    Content = Column(Text())
    comments = Column(Text())
    AgreeCount = Column(String(255))
    DisagreeCount = Column(String(255))
    AskCount = Column(String(255))
    ParticipateCount = Column(String(255))
    CollectionCount = Column(String(255))
    Classification = Column(String(255))
    Labels = Column(String(255))
    Type = Column(String(255))
    RewardCount = Column(String(255))

class Repository_Huxiuwang(Base):
    __tablename__ = 'last9990'
    id = Column(Integer, primary_key=True)
    AuthorID = Column(String(255))
    AuthorName = Column(String(255))
    ArticleTitle = Column(String(255))
    SourceArticleURL = Column(String(255))
    URL = Column(String(255))
    PublishTime = Column(String(255))
    Crawler = Column(String(255))
    ReadCount = Column(String(255))
    CommentCount = Column(String(255))
    TransmitCount = Column(String(255))
    Content = Column(Text())
    comments = Column(Text())
    AgreeCount = Column(String(255))
    DisagreeCount = Column(String(255))
    AskCount = Column(String(255))
    ParticipateCount = Column(String(255))
    CollectionCount = Column(String(255))
    Classification = Column(String(255))
    Labels = Column(String(255))
    Type = Column(String(255))
    RewardCount = Column(String(255))

if __name__ == '__main__':
    Base.metadata.create_all(engine)

