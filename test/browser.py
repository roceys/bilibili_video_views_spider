import random
import time
from threading import RLock
from unittest import TestCase

import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os

from spider.proxy_model import ProxyStack

os.chdir('../')


class WebTest(TestCase):
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
