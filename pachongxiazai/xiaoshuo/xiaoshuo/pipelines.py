# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import YqxsItem,bizhiItem,tongchengItem
from pymongo import MongoClient
import pymysql
class xiaoshuoPipeline(object):
    def process_item(self, item, spider):
        return item
class S58tongchengPipeline(object):
    def process_item(self, item, spider):
        return item
class bizhiPipeline(object):
    def open_spider(self,spider):
        '''
        爬虫启动时触发该函数，spider为触发pipeline的爬虫实例
        '''
        self.m=MongoClient()#连接数据库
        self.db=self.m.xs2#进入数据库
        self.col=self.db[spider.name]#获取数据集
    def process_item(self, item, spider):
        '''
        当爬虫抛出一个item实例是触发该函数
        向该方法传入触发的item实例及爬虫实例
        '''
        #当传入的item为NayangJobItem类型时将其转换为字典存入mongodb
        if isinstance(item,bizhiItem):
            self.col.insert_one(dict(item))
        #将item返回以待后继的pipeline进行处理
        return item
    def close_spider(self,spider):
        '''
        当爬虫关闭时触发该方法，一般可以用来进行数据库的断开操作
        '''
        self.m.close()



class YqxsItemPipeline(object):
    def open_spider(self,spider):
        '''
        爬虫启动时触发该函数，spider为触发pipeline的爬虫实例
        '''
        self.m=MongoClient()#连接数据库
        self.db=self.m.xs#进入数据库
        self.col=self.db[spider.name]#获取数据集
    def process_item(self, item, spider):
        '''
        当爬虫抛出一个item实例是触发该函数
        向该方法传入触发的item实例及爬虫实例
        '''
        #当传入的item为NayangJobItem类型时将其转换为字典存入mongodb
        # if isinstance(item,YqxsItem):
        #     self.col.insert_one(dict(item))
        #将item返回以待后继的pipeline进行处理
        return item
    def close_spider(self,spider):
        '''
        当爬虫关闭时触发该方法，一般可以用来进行数据库的断开操作
        '''
        self.m.close()


class xiaoSQLPipeline(object):
    def open_spider(self,spider):
        '''
        爬虫启动时触发该函数，spider为触发pipeline的爬虫实例
        '''
        self.__conn=pymysql.connect(host='127.0.0.1',port=3306,db='tongcheng',user='root',passwd='root',charset='utf8')
        self.cu=self.__conn.cursor(pymysql.cursors.DictCursor)
    def process_item(self, item, spider):
        if isinstance(item,YqxsItem):
            #查询分类id
            sql='select * from type where name=%s'
            flag=self.cu.execute(sql,(item['type_'],))
            if flag:
                type_id=self.cu.fetchone()['idtype']
            else:
                sql='insert into type (name)values(%s)'
                self.cu.execute(sql,(item['type_'],))
                self.__conn.commit()
                type_id=self.cu.lastrowid
            #查询书籍id
            sql='select * from book where book_name=%s and anthor=%s'
            flag=self.cu.execute(sql,(item['book_name'],item['anthor']))
            if flag:
                book_id=self.cu.fetchone()['idbook']
            else:
                sql='insert into book (book_name,anthor,num_zishu,img,type_id)values(%s,%s,%s,%s,%s)'
                self.cu.execute(sql,(item['book_name'],item['anthor'],item['num_zishu'],item['images'][0]['path'],type_id))
                self.__conn.commit()
                book_id=self.cu.lastrowid
            #存入数据
            #
            # flag=self.cu.execute(sql,(book_id,item['number']))
            # if flag==0:
            #     sql='insert into book (book_name,author,img,type_id,num_zishu) values (%s,%s,%s,%s,%s)'
            #
            #     self.__conn.commit()commit
        return item
    def close_spider(self,spider):
        self.cu.close()
        self.__conn.close()
