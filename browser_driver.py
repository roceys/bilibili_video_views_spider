import time
from threading import Thread
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from conf import *
from selenium import webdriver

from spider.proxy_model import ProxyStack
from utils.logger import log


class ChromePlayer:
    task_start = 0
    task_over = 0

    def __init__(self, head_less=ACT_HEADLESS):
        opt = Options()
        opt.add_argument('--window-size=250,600')  # 窗口大小会有影响.
        opt.add_argument('--log-level=3')
        if head_less:
            opt.add_argument('--headless')  # 无界面化.
            opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
        self.opt = opt
        self.proxy_pool = None
        self.ip_pool = None

    def start_play(self, ip, duration=PLAY_DURATION, wait_for=WAIT_TIME, proxy=ACT_PROXY):
        """
        :param proxy: 启用代理
        :param ip: 播放地址
        :param duration: 播放持续时间
        :param wait_for: 页面载入超时时间
        :return:
        """
        try:
            if proxy:
                assert self.proxy_pool, 'please set proxy pool'
                self.opt.add_argument('--proxy-server=%s' % self.proxy_pool.pop())
            with webdriver.Chrome(chrome_options=self.opt) as browser:
                # 地址栏输入 地址
                browser.get(ip)
                browser.switch_to.window(browser.window_handles[0])
                path = '''//*[@id="bilibiliPlayer"]//button[@class='bilibili-player-iconfont bilibili-player-iconfont-start']'''
                WebDriverWait(browser, wait_for).until(lambda arg: browser.find_element_by_xpath(path))
                su = browser.find_element_by_xpath(path)
                su.click()
                time.sleep(duration)

        except Exception as e:
            log.error(('播放失败', e))
            exit(0)
        finally:
            ChromePlayer.task_over += 1

    def loop_play(self, ip_pool, proxy_pool=None, max_thread=MAX_THREAD, multi=MULTI_THREAD, multi_poll=MULTI_POll):
        """循环播放"""
        if proxy_pool:
            self.proxy_pool = proxy_pool
        self.ip_pool = ip_pool
        c = ChromePlayer
        while True:
            if multi:
                # 多线程
                while c.task_start - c.task_over < max_thread:
                    ip = ip_pool.pop()
                    Thread(target=self.start_play, args=(ip,)).start()
                    ChromePlayer.task_start += 1
                else:
                    time.sleep(multi_poll)
            else:
                self.start_play(ip_pool.pop())


if __name__ == '__main__':
    proxy_pool = ProxyStack()
    ip = proxy_pool.pop()
    ChromePlayer().loop_play()
