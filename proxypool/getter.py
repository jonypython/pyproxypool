from proxypool.db import RedisClient
from proxypool.crawler import CrawlerProxy

POOL_UPPER_THRESHOLD = 300


class Getter:
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = CrawlerProxy()

    def is_over_threshold(self):
        if self.redis.count() > POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('*****获取器开始执行*****')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback=callback)
                for proxy in proxies:
                    self.redis.add(proxy)

