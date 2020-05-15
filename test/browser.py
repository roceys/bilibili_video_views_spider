import random
import time
from threading import RLock
from unittest import TestCase
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os

os.chdir('../')


class WebTest(TestCase):
    def test_driver(self):
        ops = Options()
        # ops.add_argument('--headless')
        # ops.add_argument('--disable-dev-shm-usage')
        # ops.add_argument('--disable-gpu')
        # ops.add_argument('--user-agent=%s' % ua)
        # ops.add_argument('--no-sandbox')
        # ops.add_argument('--proxy-server=http://%s' % proxy)
        # driver = webdriver.Chrome(chrome_options=ops)
        with webdriver.Chrome(chrome_options=ops) as driver:
            driver.get("http://httpbin.org/get")
            time.sleep(10)

    def test_class_attr(self):
        class A:
            a = 0

        def f1():
            time.sleep(random.uniform(0, 3))
            A.a += 1

        from threading import Thread
        l1 = []
        for i in range(100000):
            t = Thread(target=f1)
            t.start()
            l1.append(t)
        for t in l1:
            t.join()
        print(A.a)

