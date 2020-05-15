import sys

PATH = sys.path.append('proxies')  # todo 自定义proxies路径,by_yourself
from browser_driver import ChromePlayer
from proxies.main import task
from proxies.spider.proxy_model import ProxyStack
from pools.url_list import IPPool

# 解注下面三行代码，实现代理
# task()
proxy_pool1 = ProxyStack()
ip_pool1 = IPPool()
# while not proxy_pool1.get_random():
#     pass
ChromePlayer().loop_play(ip_pool1, proxy_pool1)
