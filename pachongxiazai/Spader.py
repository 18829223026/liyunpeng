import redis


class Urls(object):
    # 爬虫url管理器
    def __init__(self, name, host='127.0.0.1', port='6379'):
        self.redis = redis.Redis(host=host, port=port)
        self.spider_name = name

    def add_urls(self, *args):
        for x in args:
            if not self.redis.sismember(self.spider_name + '_old', x):
                self.redis.sadd(self.spider_name + '_new', x)
        return True

    def get_url(self):
        url = self.redis.spop(self.spider_name + '_new')
        if url == None:
            return None
        self.redis.sadd(self.spider_name + '_old', url)
        return url.decode('utf8')

    def back_url(self, url):
        self.redis.smove(self.spider_name + '_old', self.spider_name + '_new', url)
        return url

    def __len__(self):
        return self.redis.scard(self.spider_name + '_new')
