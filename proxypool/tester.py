import asyncio
import aiohttp
from proxypool.db import RedisClient
import time
import sys

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError

from proxypool.setting import *

TEST_URL = 'http://www.baidu.com'


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """

        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')

                real_proxy = 'http://' + proxy
                print('正在验证 --> ', real_proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('验证成功 -->', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('验证失败 Code 不合法-->', proxy)

            except (ClientError, aiohttp.client_exceptions.ClientConnectionError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('验证失败 -->', proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print("验证程序启动")
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy=proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(3)
        except Exception as e:
            print('测试中发生了错误 --> ', e.args)
