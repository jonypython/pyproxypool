import redis
from random import choice
from proxypool.error import PoolEmptyError

MAX_SCORE = 100
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'foobared'
REDIS_KEY = 'proxies'


class RedisClient(object):

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: redis 地址
        :param port: redis 端口
        :param password: redis 密码
        """

        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理， 设置分数
        :param proxy: 代理
        :param score: 分数
        :return:
        """

        if not self.db.zscore(REDIS_KEY, proxy):
            self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        获取随机代理
        :return:
        """

        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)

        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，分数为0时 则删除代理
        :param proxy:
        :return:
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > 0:
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy:
        :return:
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理设置为 MAX_SCORE
        :param proxy:
        :return:
        """

        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取 数量
        :return:
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取 所有的代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, 0, MAX_SCORE)
