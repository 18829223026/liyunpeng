# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .items import TongchengItem,LuntanItem
from scrapy.http import Request

class S58tongchengPipeline(object):

    def open_spider(self,spider):
        '''
        爬虫启动时触发该函数，spider为触发pipeline的爬虫实例
        '''
        self.__conn=pymysql.connect(host='127.0.0.1',port=3306,db='ershouche',user='root',passwd='root',charset='utf8')
        self.cu=self.__conn.cursor(pymysql.cursors.DictCursor)
    def process_item(self, item, spider):
        if isinstance(item,TongchengItem):
            #查询分类id
            # sql='select * from cartype where car_type=%s'
            # flag=self.cu.execute(sql,(item['car_type'],))
            # if flag:
            #     id_car_type=self.cu.fetchone()['idytpe']
            # else:
            #     sql='insert into cartype (car_type)values(%s)'
            #     self.cu.execute(sql,(item['car_type']))
            #     self.__conn.commit()
            #     id_car_type=self.cu.lastrowid
            # sql = 'select * from guige where guige=%s'
            # flag = self.cu.execute(sql, (item['guige'],))
            # if flag:
            #     idguige = self.cu.fetchone()['idguige']
            # else:
            #     sql = 'insert into guige (guige)values(%s)'
            #     self.cu.execute(sql, (item['guige'],))
            #     self.__conn.commit()
            #     idguige = self.cu.lastrowid
            #查询书籍id
            sql='select * from rshouche1 where url_=%s'
            flag=self.cu.execute(sql,(item['url_']))
            if flag:
                id=self.cu.fetchone()['id']
            else:
                sql='insert into rshouche1 (car_name,price,lucheng,where_,guige,addr,url_)values(%s,%s,%s,%s,%s,%s,%s)'
                self.cu.execute(sql,(item['car_name'],item['price'],item['lucheng'],item['where_'],item['guige'],item['addr'],item['url_']))
                self.__conn.commit()
                id=self.cu.lastrowid
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

class LuntanPipeline(object):

    def open_spider(self,spider):
        self.__conn=pymysql.connect(host='127.0.0.1',port=3306,db='ershouche',user='root',passwd='root',charset='utf8')
        self.cu=self.__conn.cursor(pymysql.cursors.DictCursor)
    def process_item(self, item, spider):
        if isinstance(item,LuntanItem):

            sql='select * from luntan1 where type_name=%s'
            flag=self.cu.execute(sql,(item['type_name']))
            if flag:
                id=self.cu.fetchone()['id']
            else:
                sql='insert into luntan1 (anthor,clinck,huifu,type_name)values(%s,%s,%s,%s)'
                self.cu.execute(sql,(item['anthor'],item['clinck'],item['huifu'],item['type_name']))
                self.__conn.commit()

        return item
    def close_spider(self,spider):
        self.cu.close()
        self.__conn.close()
