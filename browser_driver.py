import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import settings
import url_list
from ip_pool.csv_helper import get_ip_pool_list


def set_headless():
    global chrome_opt
    chrome_opt.add_argument('--headless')  # 无界面化.
    chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
    chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.


chrome_opt = Options()  # 创建参数设置对象.
if settings.ACT_HEADLESS:
    set_headless()

# 创建Chrome对象并传入设置信息.
browser = webdriver.Chrome(chrome_options=chrome_opt)


def start_play(url, ip):
    # 地址栏输入 地址
    browser.get(url)
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])
    # 点击按钮
    path = '//*[@id="bilibiliPlayer"]//video'
    su = browser.find_element_by_xpath(path)
    su.click()
    time.sleep(settings.SLEEP_TIME)
    msg = url + '已完成播放       '
    with open('log.md', 'a') as file:
        file.write('\n')
        file.write(msg + str(datetime.now()).split('.')[0] + '       ip地址{}'.format(ip))


def one_ip_loop_play(ip):
    chrome_opt.add_argument('–proxy-server=http://{}'.format(ip))
    a_list = url_list.get_list()
    for url in a_list:
        start_play(url, ip)


def loop_ip_play():
    ip_list = get_ip_pool_list()
    for ip in ip_list:
        one_ip_loop_play(ip)
    browser.quit()


if __name__ == '__main__':
    # url0 = 'https://www.bilibili.com/video/av20379071/'
    # start_play(url0)
    loop_ip_play()
