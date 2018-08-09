from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1

        attrs['__CrawlFuncCount__'] = count
        return type.__new__(mcs, name, bases, attrs)


class CrawlerProxy(object, metaclass=ProxyMetaclass):

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取代理 --> ', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count:
        :return:
        """
        start_url = 'http://www.66ip.cn/{}.html'

        urls = [start_url.format(page) for page in range(1, page_count + 1)]

        for url in urls:
            print('Crawling --> ', urls)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_xici(self, page_count=4):
        """
        获取 西刺代理
        :return:
        """

        start_url = 'http://www.xicidaili.com/nn/{}'

        urls = [start_url.format(page) for page in range(1, page_count + 1)]

        for url in urls:
            print('Crawling --> ', urls)
            html = get_page(url)
            if html:
                doc = pq(html)
                tr = doc('#ip_list tr').items()
                for td in tr:
                    ip = td.find('td:nth-of-type(2)').text()
                    port = td.find('td:nth-of-type(3)').text()
                    if len(ip) > 0:
                        yield ':'.join([ip, port])
