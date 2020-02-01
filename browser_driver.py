import sys
import threading
import time
from datetime import datetime
from threading import Thread

import fake_useragent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import settings
import url_list
from ip_pool.file_handler import get_ip_pool_list, get_last_row_number, update_line_to_eof
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


#get直接返回，不再等待界面加载完成
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
COUNT = 0
thread_lock = threading.Lock()


def set_headless(opt_):

    opt_.add_argument('--headless')  # 无界面化.
    opt_.add_argument('--disable-gpu')  # 配合上面的无界面化.
    return opt_


def get_opt():
    opt_ = Options()  # 创建参数设置对象.
    opt_.add_argument('--window-size=250,600')  # 设置窗口大小, 窗口大小会有影响.
    opt_.add_argument('--log-level=3')  # 设置窗口大小, 窗口大小会有影响.
    ua = fake_useragent.UserAgent().random
    opt_.add_argument(f'user-agent={ua}')
    prefs = {"profile.managed_default_content_settings.images": 2}
    opt_.add_experimental_option("prefs", prefs)

    if settings.ACT_HEADLESS:
        set_headless(opt_)

    return opt_


def start_play(ip, count):
    try:
        if settings.PLAY_ONE_VIDEO:
            url_list_ = [settings.ONE_VIDEO_ADDR]
        else:
            url_list_ = url_list.get_list()
        opt = get_opt()
        opt.add_argument('--proxy-server=http://%s' % ip)

        with webdriver.Chrome(chrome_options=opt) as browser:
            # 地址栏输入 地址
            for url in url_list_:

                # browser.get('http://httpbin.org/get')
                browser.get(url)
                browser.switch_to.window(browser.window_handles[0])

                path = '''//*[@id="bilibiliPlayer"]//button[@class='bilibili-player-iconfont bilibili-player-iconfont-start']'''
                try:
                    WebDriverWait(browser, settings.WAIT_TIME).until(lambda browser: browser.find_element_by_xpath(path))
                    # 点击按钮
                    su = browser.find_element_by_xpath(path)
                    browser.delete_all_cookies()
                    su.click()
                except:
                    print('No.{}加载缓慢,切换中....'.format(str(count)+'--'+ip))
                    continue
                time.sleep(settings.PLAY_DURATION)
                msg = url + '已完成播放       '
                with open('log.md', 'a') as file:
                    content = str(count) + msg + str(datetime.now()).split('.')[0] + '       ip地址{}'.format(ip)
                    file.write('\n')
                    file.write(content)
                    if settings.PRINT_LOG:
                        print(content)

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
    # num = get_last_row_number()
    # update_line_to_eof(int(num) + settings.MAX_THREAD)  # 将日志用过的ip'过量'移至文档末尾
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
