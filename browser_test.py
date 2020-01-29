from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import settings


def set_headless():
    opt_ = Options()  # 创建参数设置对象.
    opt_.add_argument('--headless')  # 无界面化.
    opt_.add_argument('--disable-gpu')  # 配合上面的无界面化.
    # chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.
    opt_.add_argument('--window-size=100,100')  # 设置窗口大小, 窗口大小会有影响.
    opt_.add_argument('--log-level=3')  # 设置窗口大小, 窗口大小会有影响.
    return opt_


def get_opt():
    if settings.ACT_HEADLESS:
        opt = set_headless()
    else:
        opt = Options()
        opt.add_argument('--log-level=fatal')  # 设置窗口大小, 窗口大小会有影响.
    return opt


opt = get_opt()
browser = webdriver.Chrome(chrome_options=opt)
opt.add_argument('–proxy-server=https://{}'.format(
    '144.123.68.25'
))
a = opt
# 地址栏输入 地址

browser.get(settings.ONE_VIDEO_ADDR)
