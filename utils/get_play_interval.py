"""获取播放间隔时间"""
import json
import time
from selenium import webdriver
from browser_driver import click_play_button, get_opt, add_log
from utils import get_bilibili_play_times

url = 'https://www.bilibili.com/video/av20379071/'
opt = get_opt(None)
cookies = [{'domain': '.bilibili.com', 'expiry': 1583246896.613479, 'httpOnly': False, 'name': 'bili_jct', 'path': '/',
            'secure': False, 'value': '83475ada400aec84062a3e7f9d9263ce'},
           {'domain': '.bilibili.com', 'expiry': 1583246896.613396, 'httpOnly': True, 'name': 'SESSDATA', 'path': '/',
            'secure': False, 'value': 'f7538e09%2C1583246896%2C81269e21'},
           {'domain': '.bilibili.com', 'expiry': 1583246896.613014, 'httpOnly': False, 'name': 'DedeUserID',
            'path': '/', 'secure': False, 'value': '10241912'},
           {'domain': '.bilibili.com', 'expiry': 2177452799.687886, 'httpOnly': False, 'name': 'LIVE_BUVID',
            'path': '/', 'secure': False, 'value': 'AUTO6915806548736374'},
           {'domain': '.bilibili.com', 'httpOnly': False, 'name': 'sid', 'path': '/', 'secure': False,
            'value': '4o5ko5hc'},
           {'domain': '.bilibili.com', 'expiry': 1675262871.717854, 'httpOnly': False, 'name': 'buvid3', 'path': '/',
            'secure': False, 'value': '4EFAC617-BDE6-4AF3-9E85-40AB925E9278155803infoc'},
           {'domain': '.bilibili.com', 'expiry': 1583246896.613256, 'httpOnly': False, 'name': 'DedeUserID__ckMd5',
            'path': '/', 'secure': False, 'value': '8547f0ad511547f0'},
           {'domain': '.bilibili.com', 'expiry': 1612190871, 'httpOnly': False, 'name': '_uuid', 'path': '/',
            'secure': False, 'value': '9C15BD51-3F49-CC2C-B784-2F746FB25BC871598infoc'},
           {'domain': '.bilibili.com', 'expiry': 1612190898, 'httpOnly': False, 'name': 'CURRENT_FNVAL', 'path': '/',
            'secure': False, 'value': '16'}]
with webdriver.Chrome(chrome_options=opt) as browser:
    # 地址栏输入 地址
    while True:
        # browser.get('http://httpbin.org/get')
        browser.get(url)
        [browser.add_cookie(dict_) for dict_ in cookies]
        browser.switch_to.window(browser.window_handles[0])
        path = '''//*[@id="bilibiliPlayer"]//button[@class='bilibili-player-iconfont bilibili-player-iconfont-start']'''
        click_play_button(browser, path)
        time.sleep(30)
        times = get_bilibili_play_times(url)
        add_log('0', '127.0.0.1', url, times)

