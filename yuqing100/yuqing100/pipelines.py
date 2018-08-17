# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import requests
from sqlalchemy.orm import sessionmaker
from yuqing100.models import Repository_Huxiuwang,Repository_Cankaoxiaoxi,Repository_JRTT,Repository_kepuchina,Repository_banyuetan,Repository_heimawang, Repository_sansijiaoyu, Repository_nanfrwzk, Repository_lianhezaobao, engine
from yuqing100.items import Yuqing_HuxiuwangItem,Yuqing_CankaoxiaoxiItem,Yuqing_JRTTItem,Yuqing_banyuetanItem,Yuqing_heimawangItem, Yuqing_sansijiaoyuItem, Yuqing_nanfrwzkItem, Yuqing_lianhezaobaoItem, Kepu_tupian
from yuqing100.settings import IMAGES_STORE

class Yuqing100Pipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Yuqing_banyuetanItem):
            self.session.add(Repository_banyuetan(**item))
            return item
        elif isinstance(item, Yuqing_sansijiaoyuItem):
            self.session.add(Repository_sansijiaoyu(**item))
            return item
        elif isinstance(item, Yuqing_nanfrwzkItem):
            self.session.add(Repository_nanfrwzk(**item))
            return item
        elif isinstance(item, Yuqing_lianhezaobaoItem):
            self.session.add(Repository_lianhezaobao(**item))
            return item
        elif isinstance(item, Yuqing_heimawangItem):
            self.session.add(Repository_heimawang(**item))
            return item
        elif isinstance(item, Yuqing_JRTTItem):
            self.session.add(Repository_JRTT(**item))
            return item
        elif isinstance(item, Yuqing_CankaoxiaoxiItem):
            self.session.add(Repository_Cankaoxiaoxi(**item))
            return item
        elif isinstance(item, Yuqing_HuxiuwangItem):
            self.session.add(Repository_Huxiuwang(**item))
            return item
        elif isinstance(item, Kepu_tupian):

            fold_name = "".join(item['Title'])
            images = []
            # 所有图片放在一个文件夹下
            dir_path = '{}'.format(IMAGES_STORE)
            if not os.path.exists(dir_path) and len(item['img_url']) != 0:
                os.mkdir(dir_path)
            for jpg_url in item['img_url']:
                file_name = jpg_url.replace('./','')
                jpg_url = item['url'].split('/t201')[0] + '/' + file_name
                file_path1 = '{}//{}'.format(dir_path, fold_name)
                file_path2 = '{}//{}//{}'.format(dir_path, fold_name,file_name)
                images.append(file_path2)
                if not os.path.exists(file_path1) :
                    os.mkdir(file_path1)
                with open('{}'.format(file_path2), 'wb') as f:
                    req = requests.get(jpg_url)
                    print(jpg_url)
                    f.write(req.content)
            if len(images) > 0:
                img_paths = ''
                for image in images:
                    img_paths = image + ',' + img_paths
                item['img_path'] = img_paths
            else:
                item['img_path'] = ''

            if len(item['img_url']) > 0:
                img_urls = ''
                for image in item['img_url']:
                    img_urls = image + ',' + img_urls
                item['img_url'] = img_urls
            else:
                item['img_url'] = ''
            item['Content'] = item['Content'].replace('src="./','src="' + '{}//{}'.format(dir_path, fold_name) +'//')
            self.session.add(Repository_kepuchina(**item))
            return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()


class Panduan_banyuetan(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_banyuetan.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls


class Panduan_sansijiaoyu(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_sansijiaoyu.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls


class Panduan_nanfrwzk(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_nanfrwzk.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls


class Panduan_lianhezaobao(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_lianhezaobao.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_heimawang(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_heimawang.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_JRTT(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_JRTT.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Cankaoxiaoxi(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Cankaoxiaoxi.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Huxiuwang(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Huxiuwang.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

if __name__ == '__main__':
    panduan = Panduan_JRTT()
    if 'https://www.toutiao.com/group/65883611957475415121/' in panduan.panduan():
        print('Ture')
