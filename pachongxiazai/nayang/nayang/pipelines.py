# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#本模块代码要生效需要在settings.py中的ITEM_PIPELINES字段中进行设置

from nayang.items import NayangJobItem,XiaoshuoItem
from pymongo import MongoClient
import pymysql
class NayangPipeline(object):
    def process_item(self, item, spider):
        return item

class XiaoSQLPipeline(object):
    def open_spider(self,spider):
        '''
        爬虫启动时触发该函数，spider为触发pipeline的爬虫实例
        '''
        self.__conn=pymysql.connect(host='192.168.2.113',port=3306,db='xiaoshuo',user='root',passwd='1192002',charset='utf8')
        self.cu=self.__conn.cursor(pymysql.cursors.DictCursor)
    def process_item(self, item, spider):
        if isinstance(item,XiaoshuoItem):
            #查询分类id
            sql='select idtype from type where name=%s'
            flag=self.cu.execute(sql,(item['type_'],))
            if flag:
                type_id=self.cu.fetchone()['idtype']
            else:
                sql='insert into type (name)values(%s)'
                self.cu.execute(sql,(item['type_'],))
                self.__conn.commit()
                type_id=self.cu.lastrowid
            #查询书籍id
            sql='select idbook from book where name=%s and type_id=%s'
            flag=self.cu.execute(sql,(item['type_'],type_id))
            if flag:
                book_id=self.cu.fetchone()['idbook']
            else:
                sql='insert into book (name,author,img,type_id)values(%s,%s,%s,%s)'
                self.cu.execute(sql,(item['book_name'],item['author'],item['images'][0]['path'],type_id))
                self.__conn.commit()
                book_id=self.cu.lastrowid
            #存入数据
            sql='select * from chpter where book_id=%s and `order`=%s'
            flag=self.cu.execute(sql,(book_id,item['number']))
            if flag==0:
                sql='insert into chpter (name,content,book_id,`order`) values (%s,%s,%s,%s)'
                self.cu.execute(sql,(item['chpter_name'],item['chpter_content'],book_id,item['number']))
                self.__conn.commit()
        return item
    def close_spider(self,spider):
        self.cu.close()
        self.__conn.close()

class XiaoshuoPipeline(object):
    def open_spider(self,spider):
        '''
        爬虫启动时触发该函数，spider为触发pipeline的爬虫实例
        '''
        self.m=MongoClient()#连接数据库
        self.db=self.m.nayang#进入数据库
        self.col=self.db[spider.name]#获取数据集
    def process_item(self, item, spider):
        if isinstance(item,XiaoshuoItem):
            data=dict(item)
            if not self.col.find(data):
                self.col.insert_one(data)
        return item

class NayangJobsPipeline(object):
    def open_spider(self,spider):
        '''
        爬虫启动时触发该函数，spider为触发pipeline的爬虫实例
        '''
        self.m=MongoClient()#连接数据库
        self.db=self.m.nayang#进入数据库
        self.col=self.db[spider.name]#获取数据集
    def process_item(self, item, spider):
        '''
        当爬虫抛出一个item实例是触发该函数
        向该方法传入触发的item实例及爬虫实例
        '''
        #当传入的item为NayangJobItem类型时将其转换为字典存入mongodb
        #if isinstance(item,NayangJobItem):
            #self.col.insert_one(dict(item))
        #将item返回以待后继的pipeline进行处理
        return item
    def close_spider(self,spider):
        '''
        当爬虫关闭时触发该方法，一般可以用来进行数据库的断开操作
        '''
        self.m.close()
