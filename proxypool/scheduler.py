import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.setting import *


class Scheduler(object):

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时检测代理
        :param cycle:
        :return:
        """

        tester = Tester()

        while True:
            print('定时测试器 [开启]')
            tester.run()
            time.sleep(cycle)

    def schedul_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理数据
        :param cycle:
        :return:
        """

        getter = Getter()

        while True:
            print('定时获取代理 [开启]')
            getter.run()
            time.sleep(cycle)

    def schedul_api(self):
        """
        开启 api
        :return:
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedul_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedul_api)
            api_process.start()


if __name__ == '__main__':
    schedul = Scheduler()
    schedul.run()
