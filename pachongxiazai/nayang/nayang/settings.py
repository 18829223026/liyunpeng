# -*- coding: utf-8 -*-

# Scrapy settings for nayang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'nayang'

SPIDER_MODULES = ['nayang.spiders']
NEWSPIDER_MODULE = 'nayang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nayang (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'nayang.middlewares.NayangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'nayang.middlewares.NayangDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#设置图片存储位置
IMAGES_STORE = './images/'
# 90 天的图片失效期限
IMAGES_EXPIRES = 90
#设置缩略图
IMAGES_THUMBS = {
'small': (25, 25),
}
#设置宽度或者高度小于110的图片不下载
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110
ITEM_PIPELINES = {
     'nayang.pipelines.NayangPipeline': 300,
     'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
     'nayang.pipelines.NayangJobsPipeline':100,
     'nayang.pipelines.XiaoshuoPipeline':101,
     'nayang.pipelines.XiaoSQLPipeline':99,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# 1.(必须加)。使用scrapy_redis.duperfilter.REPDupeFilter的去重组件，在redis数据库里做去重。
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 2.（必须加）。使用了scrapy_redis的调度器，在redis里面分配请求。
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 3.（必须加）。在redis queues 允许暂停和暂停后恢复，也就是不清理redis queues
SCHEDULER_PERSIST = True
# 4.（可选项）。通过RedisPipeline将item写入key为 spider.name: items的redis的list中，供后面的分布式处理item。
# 这个已经由scrapy-redis实现了，不需要我们自己手动写代码，直接使用即可。
#ITEM_PIPELINES = {
#   'scrapy_redis.pipelines.RedisPipeline': 100
#}
#5、（必须加）。配置数据库
#REDIS_URL="redis://127.0.0.1:6379"
REDIS_HOST = "192.168.2.113"
REDIS_PORT = 6379