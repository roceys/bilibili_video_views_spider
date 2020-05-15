import asyncio
import time
from threading import Thread
import aiohttp
from spider.proxy_model import ProxyStack
from spider.xici_ip_model import XiciQueue
import requests
from utils.logger import log


class AsyncSpider:
    """only support http proxy"""

    def __init__(self, queue, stack):
        self.queue = queue
        self.stack = stack

    sem = 20
    time_out = 10

    async def loop_send_req(self):
        while True:
            url1 = 'http://httpbin.org/get'
            url2 = self.queue.de_queue()
            proxy = 'http://' + url2
            # 信号量，控制协程数，防止爬的过快
            async with asyncio.Semaphore(AsyncSpider.sem):
                print('url', url1, 'proxy', proxy)
                # async with是异步上下文管理器
                async with aiohttp.ClientSession() as session:  # 获取session
                    try:
                        async with session.get(url1, proxy=proxy) as resp:  # 提出请求
                            html = await resp.read()  # 可直接获取bytes
                            if url2 in html.decode():
                                self.stack.en_stack(url1)
                                log.info(('in stack 1', url2))
                    except Exception as e:
                        log.debug(e)

    def main(self):
        loop = asyncio.get_event_loop()  # 获取事件循环
        tasks = [self.loop_send_req() for _ in range(AsyncSpider.sem)]  # 把所有任务放到一个列表中
        while True:
            loop.run_until_complete(asyncio.wait(tasks, timeout=AsyncSpider.time_out))  # 激活协程


class ThreadSpider:
    time_out = 8
    poll_time = 10
    sem = 5
    start_task = 0
    stop_task = 0
    stack_size = 40

    def __init__(self, queue, stack):
        self.queue = queue
        self.stack = stack

    @staticmethod
    def check_proxy(url) -> bool:
        to = 'http://httpbin.org/get'
        proxies = {
            'http': 'http://' + url,
            'https': 'https://' + url,
        }
        try:
            log.info('start connection to {}'.format(url))
            res = requests.get(to, proxies=proxies, timeout=ThreadSpider.time_out)
        except Exception as e:
            log.info('连接错误' + e.__str__())
            return False
        log.info(res.text)
        if url.split(':')[0] in res.text:
            return True
        return False

    def _main_loop(self):
        try:
            url = self.queue.de_queue()
            if self.check_proxy(url):
                self.stack.en_stack(url)
                log.info(('en stack 1 url', url))
            else:
                log.info(('invalid url', url))
        finally:
            ThreadSpider.stop_task += 1

    def main_loop(self):
        while True:
            while ThreadSpider.start_task - ThreadSpider.stop_task <= ThreadSpider.sem and self.stack.get_size() < ThreadSpider.stack_size:
                Thread(target=self._main_loop).start()
                ThreadSpider.start_task += 1
            else:
                log.info(('线程池容量', ThreadSpider.sem))
                log.info(('堆栈量', self.stack.get_size()))
                time.sleep(ThreadSpider.poll_time)


if __name__ == "__main__":
    # DEBUG:root:b'{ "origin": "39.137.107.98", \n  "url": "http://httpbin.org/get"\n}\n'
    ThreadSpider(XiciQueue, ProxyStack).main_loop()
