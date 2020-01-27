import time
from datetime import datetime
from threading import Thread
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import settings
import url_list
from ip_pool.csv_helper import get_ip_pool_list
from selenium.webdriver.support import expected_conditions as EC


def set_headless():
    global chrome_opt
    chrome_opt.add_argument('--headless')  # 无界面化.
    chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
    chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.


chrome_opt = Options()  # 创建参数设置对象.
if settings.ACT_HEADLESS:
    set_headless()


def start_play(browser, url, ip):
    # 地址栏输入 地址
    browser.get(url)

    # path = '//*[@id="bilibiliPlayer"]//video'
    path = '''//*[@id="bilibiliPlayer"]//button[@class='bilibili-player-iconfont bilibili-player-iconfont-start']'''
    locator = (By.XPATH, path)
    browser.switch_to.window(browser.window_handles[0])
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(locator))
    time.sleep(1)
    # 点击按钮
    su = browser.find_element_by_xpath(path)
    su.click()
    time.sleep(settings.SLEEP_TIME)
    msg = url + '已完成播放       '
    with open('log.md', 'a') as file:
        file.write('\n')
        file.write(msg + str(datetime.now()).split('.')[0] + '       ip地址{}'.format(ip))


def one_ip_loop_play(ip):
    # 创建Chrome对象并传入设置信息.
    browser = webdriver.Chrome(chrome_options=chrome_opt)
    chrome_opt.add_argument('–proxy-server=http://{}'.format(ip))
    # 播放up主的单个视频或者所有视频
    if settings.PLAY_ONE_VIDEO:
        start_play(browser,settings.ONE_VIDEO_ADDR,ip)
    else:
        a_list = url_list.get_list()
        for url in a_list:
            start_play(browser, url, ip)


def loop_ip_play():
    ip_list = get_ip_pool_list()
    for index, ip in enumerate(ip_list):
        try:
            print('第{}个ip开始访问'.format(index + 1))
            # 多线程
            if settings.ACT_PROCESS:
                run_multy_process(ip)
            else:
                # 单线程
                one_ip_loop_play(ip)
            print('第{}个ip访问结束'.format(index + 1))
        except Exception as e:
            print(e)
            continue


def run_multy_process(ip):
    t = Thread(target=one_ip_loop_play, args=(ip,))
    t.daemon = True
    time.sleep(settings.THREAD_DELTA)
    t.start()


if __name__ == '__main__':
    # url0 = 'https://www.bilibili.com/video/av20379071/'
    # start_play(url0)
    loop_ip_play()
