import asyncio
import time
from unittest import TestCase
import aiohttp
import requests
from utils.logger import log
from xici_stack import XiciQueue


class ProxyTest(TestCase):
    a = 1

    def setUp(self) -> None:
        ...

    def test_proxy(self):
        url = '117.88.176.42:3000'

        to = 'http://httpbin.org/get'
        time_out = 8
        proxies = {
            'http': 'http://' + url,
            'https': 'https://' + url,
        }
        res = requests.get(to, proxies=proxies, timeout=time_out)
        print(url.split(':')[0] in res.text)
        print(res.text)

    def test_a(self):
        ProxyTest.a += 1
        print(self.a)
        print(ProxyTest.a)

    @staticmethod
    def test_asnic():
        def f1():
            print(998)
            time.sleep(1)
            print(998)
            time.sleep(1)
            print(998)
            time.sleep(1)

        async def hello():
            print("Hello world!")
            await f1()
            print("Hello again!")

        loop = asyncio.get_event_loop()
        tasks = [hello(), hello()]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    def test_yield1(self):
        def num():
            yield 1
            yield 2
            yield 3
            yield 4

        c = num()
        while True:
            print(c.send(None))
            time.sleep(1)

    def test_yield2(self):
        def num():
            a = yield 1
            while True:
                a = yield a

        c = num()

        print(c.send(None))
        time.sleep(4)
        print(c.send(10))

    def test_yield3(self):
        def a():
            next_val = yield print('start!')
            while True:
                next_val += 1
                next_val = yield next_val

        def b(gen):
            gen.send(None)
            bb = 0
            for i in range(5):
                bb = gen.send(bb)
                print(bb)
                time.sleep(1.5)

        b(a())

    def test_yiled4(self):
        def generator_1(titles):
            yield titles

        def generator_2(titles):
            yield from titles

        titles = ['Python', 'Java', 'C++']

        a = generator_1(titles)
        print(a.send(None))

        b = generator_2(titles)
        print(b.send(None))
        print(b.send(None))
        print(b.send(None))

    def test_yiled5(self):
        def generator_1():
            total = 0
            while True:
                x = yield
                print('加', x)
                if not x:
                    break
                total += x
            return total

        def generator_2():  # 委托生成器
            while True:
                total = yield from generator_1()  # 子生成器
                print('加和总数是:', total)

        def main():  # 调用方
            # g1 = generator_1()
            # g1.send(None)
            # g1.send(2)
            # g1.send(3)
            # g1.send(None)
            g2 = generator_2()
            g2.send(None)
            g2.send(2)
            g2.send(3)
            g2.send(None)

        main()

    def test_yield6(self):
        # 使用同步方式编写异步功能
        import time
        import asyncio
        async def f2():
            await asyncio.wait_for(asyncio.coroutine(time.sleep)(5), 10)

        async def f1():
            await f2()

        async def taskIO_1():
            print('开始运行IO任务1...')
            await f1()
            print('IO任务1已完成')
            return taskIO_1.__name__

        async def taskIO_2():
            print('开始运行IO任务2...')
            await asyncio.sleep(5)
            print('IO任务2已完成')
            return taskIO_2.__name__

        async def main():  # 调用方
            tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
            done, pending = await asyncio.wait(tasks)  # 子生成器
            for r in done:  # done和pending都是一个任务，所以返回结果需要逐个调用result()
                print('协程无序返回值：' + r.result())

        start = time.time()
        loop = asyncio.get_event_loop()  # 创建一个事件循环对象loop
        try:
            loop.run_until_complete(main())  # 完成事件循环，直到最后一个任务结束
        finally:
            loop.close()  # 结束事件循环
        print('所有IO任务总耗时%.5f秒' % float(time.time() - start))

    def test_async_connection(self):
        from lxml import etree
        urls = [
            'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16488',
            'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16583',
            # 省略后面8个url...
        ]
        titles = []
        sem = asyncio.Semaphore(10)  # 信号量，控制协程数，防止爬的过快
        '''
        提交请求获取AAAI网页,并解析HTML获取title
        '''

        async def get_title(url):
            async with sem:
                # async with是异步上下文管理器
                async with aiohttp.ClientSession() as session:  # 获取session
                    async with session.request('GET', url) as resp:  # 提出请求
                        # html_unicode = await resp.text()
                        # html = bytes(bytearray(html_unicode, encoding='utf-8'))
                        html = await resp.read()  # 可直接获取bytes
                        title = etree.HTML(html).xpath('//*[@id="title"]/text()')
                        log.debug(''.join(title))

        def main():
            loop = asyncio.get_event_loop()  # 获取事件循环
            tasks = [get_title(url) for url in urls]  # 把所有任务放到一个列表中
            loop.run_until_complete(asyncio.wait(tasks))  # 激活协程
            loop.close()  # 关闭事件循环

        start = time.time()
        main()  # 调用方
        log.debug('总耗时：%.5f秒' % float(time.time() - start))

    @staticmethod
    def test_async_request():
        sem = asyncio.Semaphore(10)  # 信号量，控制协程数，防止爬的过快

        async def send_req(url, proxy=None):
            async with sem:
                print(url, proxy)
                # async with是异步上下文管理器
                async with aiohttp.ClientSession() as session:  # 获取session
                    try:
                        async with session.get(url, proxy=proxy) as resp:  # 提出请求
                            html = await resp.read()  # 可直接获取bytes
                    except:
                        html = ''
                    finally:
                        log.debug(html)

        def get_tasks():
            tasks = []
            urls = ['121.40.66.129:808', '110.249.176.26:8060', '27.188.64.70:8060', '39.137.69.6:8080']
            for url in urls:
                proxies = 'http://' + url
                func = send_req('http://httpbin.org/get', proxies)
                tasks.append(func)
            return tasks

        def main():
            loop = asyncio.get_event_loop()  # 获取事件循环
            tasks = get_tasks()  # 把所有任务放到一个列表中
            loop.run_until_complete(asyncio.wait(tasks))  # 激活协程
            loop.close()  # 关闭事件循环

        start = time.time()
        main()  # 调用方
        log.debug('总耗时：%.5f秒' % float(time.time() - start))

    def test_en_queue(self):
        x = XiciQueue()
        x.loop_en_queue()
