# -*- coding: utf-8 -*-
import scrapy

from ..items import LuntanItem
class LuntanSpider(scrapy.Spider):
    name = 'luntan'
    allowed_domains = ['bbs.renrenche.com']
    start_urls = ['https://bbs.renrenche.com/forum.php?mod=forumdisplay&fid=51']
    def parse(self, rp):
        links = rp.css('.s::attr("href")').extract()  # 获
            # 取页面所有二手车链接
        for x in links:
                # 利用response对象的urljoin方法补全url1
            url = rp.urljoin(x)
            meta = {'url_': url}
            yield scrapy.Request(url=url, callback=self.next2,meta=meta)

        next_ = rp.css('.nxt::attr("href")').extract()
        if next_:
            next_ = rp.urljoin(next_[1])
                # print(next_,'++++++++++++++++++++++++++++++++')
            yield scrapy.Request(url=next_, callback=self.parse)

    def next2(self, rp):
        item = LuntanItem()
        item['type_name'] = rp.css('#thread_subject::text').extract_first()
        item['clinck'] = rp.css('.xi1::text').extract()[0]   #点击
        item['huifu'] = rp.css('.xi1::text').extract()[1]    #回复
        item['anthor'] = rp.css('.xw1::text').extract()[1]   #作者
        yield item