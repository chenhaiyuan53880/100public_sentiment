# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import requests
from sqlalchemy.orm import sessionmaker
from yuqing100.models import Repository_Zywxyjs,Repository_Zggcdlsw,Repository_Yiban,Repository_Zgshkxw,Repository_Meituan,Repository_Guoke,Repository_Gcdyw,Repository_Chuanyeban,Repository_Sihai,Repository_Lieyun,Repository_Af,Repository_Hxdsb,Repository_Dgb,Repository_Zgrb,Repository_Qiushi,Repository_Zaker,Repository_Zgwmw,Repository_Zgwhbshi,Repository_Zhongguolishi,Repository_Zgdzgblt,Repository_Douban,Repository_Danjianyanjiu,Repository_Huxiuwang,Repository_Cankaoxiaoxi,Repository_JRTT,Repository_kepuchina,Repository_banyuetan,Repository_heimawang, Repository_sansijiaoyu, Repository_nanfrwzk, Repository_lianhezaobao, engine
from yuqing100.items import Yuqing_ZywxyjsItem,Yuqing_ZggcdlswItem,Yuqing_YibanItem,Yuqing_ZgshkxwItem,Yuqing_MeituanItem,Yuqing_GuokeItem,Yuqing_GcdywItem,Yuqing_ChuanyebanItem,Yuqing_SihaiItem,Yuqing_LieyunItem,Yuqing_AfItem,Yuqing_HxdsbItem,Yuqing_DgbItem,Yuqing_ZgrbItem,Yuqing_QiushiItem,Yuqing_ZakerItem,Yuqing_ZgwmwItem,Yuqing_ZgwhbItem,Yuqing_ZhongguolishiItem,Yuqing_ZgdzgbltItem,Yuqing_DoubanItem,Yuqing_DanjianyanjiuItem,Yuqing_HuxiuwangItem,Yuqing_CankaoxiaoxiItem,Yuqing_JRTTItem,Yuqing_banyuetanItem,Yuqing_heimawangItem, Yuqing_sansijiaoyuItem, Yuqing_nanfrwzkItem, Yuqing_lianhezaobaoItem, Kepu_tupian
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
        elif isinstance(item, Yuqing_DanjianyanjiuItem):
            self.session.add(Repository_Danjianyanjiu(**item))
            return item
        elif isinstance(item, Yuqing_DoubanItem):
            self.session.add(Repository_Douban(**item))
            return item
        elif isinstance(item, Yuqing_ZgdzgbltItem):
            self.session.add(Repository_Zgdzgblt(**item))
            return item
        elif isinstance(item, Yuqing_ZhongguolishiItem):
            self.session.add(Repository_Zhongguolishi(**item))
            return item
        elif isinstance(item, Yuqing_ZgwhbItem):
            self.session.add(Repository_Zgwhbshi(**item))
            return item
        elif isinstance(item, Yuqing_ZgwmwItem):
            self.session.add(Repository_Zgwmw(**item))
            return item
        elif isinstance(item, Yuqing_ZakerItem):
            self.session.add(Repository_Zaker(**item))
            return item
        elif isinstance(item, Yuqing_QiushiItem):
            self.session.add(Repository_Qiushi(**item))
            return item
        elif isinstance(item, Yuqing_ZgrbItem):
            self.session.add(Repository_Zgrb(**item))
            return item
        elif isinstance(item, Yuqing_DgbItem):
            self.session.add(Repository_Dgb(**item))
            return item
        elif isinstance(item, Yuqing_HxdsbItem):
            self.session.add(Repository_Hxdsb(**item))
            return item
        elif isinstance(item, Yuqing_AfItem):
            self.session.add(Repository_Af(**item))
            return item
        elif isinstance(item, Yuqing_LieyunItem):
            self.session.add(Repository_Lieyun(**item))
            return item
        elif isinstance(item, Yuqing_SihaiItem):
            self.session.add(Repository_Sihai(**item))
            return item
        elif isinstance(item, Yuqing_ChuanyebanItem):
            self.session.add(Repository_Chuanyeban(**item))
            return item
        elif isinstance(item, Yuqing_GcdywItem):
            self.session.add(Repository_Gcdyw(**item))
            return item
        elif isinstance(item, Yuqing_GuokeItem):
            self.session.add(Repository_Guoke(**item))
            return item
        elif isinstance(item, Yuqing_ZgshkxwItem):
            self.session.add(Repository_Zgshkxw(**item))
            return item
        elif isinstance(item, Yuqing_YibanItem):
            self.session.add(Repository_Yiban(**item))
            return item
        elif isinstance(item, Yuqing_ZggcdlswItem):
            self.session.add(Repository_Zggcdlsw(**item))
            return item
        elif isinstance(item, Yuqing_ZywxyjsItem):
            self.session.add(Repository_Zywxyjs(**item))
            return item
        elif isinstance(item, Yuqing_MeituanItem):
            self.session.add(Repository_Meituan(**item))
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

class Panduan_Danjianyanjiu(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Danjianyanjiu.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Douban(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Douban.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zgdzgblt(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Douban.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zhongguolishi(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Zhongguolishi.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zgwhbshi(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Zgwhbshi.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zgwmw(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Zgwmw.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zaker(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Zaker.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Qiushi(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Qiushi.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zgrb(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Zgrb.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Dgb(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Dgb.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Hxdsb(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Hxdsb.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Af(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Af.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Lieyun(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Lieyun.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Sihai(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Sihai.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Chuanyeban(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Chuanyeban.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Gcdyw(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Gcdyw.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Guoke(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Guoke.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zgshkxw(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Zgshkxw.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Yiban(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Yiban.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zggcdlsw(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Zggcdlsw.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Zywxyjs(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Zywxyjs.URL).all()
        db_urls = []
        for db_url in url_list:
            db_url_ = db_url[0]
            db_urls.append(db_url_)
        session.commit()
        session.close()
        return db_urls

class Panduan_Meituan(object):
    def panduan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_list = session.query(Repository_Meituan.URL).all()
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
