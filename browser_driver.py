import sys
import threading
import time
from datetime import datetime
from threading import Thread
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import settings
import url_list
from ip_pool.file_handler import get_ip_pool_list, get_last_row_number, update_line_to_eof
from selenium.webdriver.support import expected_conditions as EC

COUNT = 0
thread_lock = threading.Lock()


def set_headless():
    opt_ = Options()  # 创建参数设置对象.
    opt_.add_argument('--headless')  # 无界面化.
    opt_.add_argument('--disable-gpu')  # 配合上面的无界面化.
    # chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.
    opt_.add_argument('--window-size=100,100')  # 设置窗口大小, 窗口大小会有影响.
    opt_.add_argument('--log-level=fatal')  # 设置窗口大小, 窗口大小会有影响.
    return opt_


def get_opt():
    if settings.ACT_HEADLESS:
        opt = set_headless()
    else:
        opt = Options()
        opt.add_argument('--log-level=fatal')  # 设置窗口大小, 窗口大小会有影响.
    return opt


def start_play(ip, count):
    try:
        if settings.PLAY_ONE_VIDEO:
            url_list_ = [settings.ONE_VIDEO_ADDR]
        else:
            url_list_ = url_list.get_list()
        from selenium import webdriver
        opt = get_opt()
        browser = webdriver.Firefox(firefox_options=opt)
        opt.add_argument('–proxy-server=http://{}'.format(ip))
        a = opt
        # 地址栏输入 地址
        for url in url_list_:
            browser.get(url)
            path = '''//*[@id="bilibiliPlayer"]//button[@class='bilibili-player-iconfont bilibili-player-iconfont-start']'''
            locator = (By.XPATH, path)
            browser.switch_to.window(browser.window_handles[0])
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable(locator))
            time.sleep(settings.SLEEP_TIME)
            # 点击按钮
            su = browser.find_element_by_xpath(path)
            su.click()
            time.sleep(settings.SLEEP_TIME)
            msg = url + '已完成播放       '
            with open('log.md', 'a') as file:
                content = str(count) + msg + str(datetime.now()).split('.')[0] + '       ip地址{}'.format(ip)
                file.write(content)
                file.write('\n')
                if settings.PRINT_LOG:
                    print(content)
        browser.quit()
    except:
        sys.exit()


def one_ip_loop_play(ip):
    # 创建Chrome对象并传入设置信息.
    global COUNT
    with thread_lock:
        COUNT += 1
        _count = COUNT
    print('第{}个ip>>>>{}开始访问'.format(_count, ip))
    # 播放up主的单个视频或者所有视频
    start_play(ip, _count)
    print('第{}个ip,{}访问结束'.format(_count, ip))

    if settings.ACT_PROCESS:
        sys.exit()


def loop_ip_play():
    """循环播放"""
    # 修改ip队列
    num = get_last_row_number()
    update_line_to_eof(int(num) + settings.MAX_THREAD)  # 将日志用过的ip'过量'移至文档末尾
    ip_list = get_ip_pool_list()
    if settings.ACT_PROCESS:
        # 多线程
        iter_obj = ip_list.__iter__()
        while True:
            try:
                new_list = [iter_obj.__next__() for _ in range(settings.MAX_THREAD)]
                start_thread(new_list)
            except StopIteration:
                break
    else:
        for index, ip in enumerate(ip_list):
            # 单线程
            one_ip_loop_play(ip)


def start_thread(list_ip):
    t_list = []
    for ip in list_ip:
        t = Thread(target=one_ip_loop_play, args=(ip,))
        t.start()
        t_list.append(t)
    for t in t_list:
        t.join()


if __name__ == '__main__':
    # url0 = 'https://www.bilibili.com/video/av20379071/'
    # start_play(url0)
    loop_ip_play()
