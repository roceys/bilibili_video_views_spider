from threading import Thread

from spider.ip_verify import ThreadSpider
from spider.log_ip_model import LogQueue
from spider.proxy_model import ProxyStack
from spider.xici_ip_model import XiciQueue

en_stack = ThreadSpider(LogQueue, ProxyStack).main_loop
en_queue = LogQueue('log/2020-05-14.log').loop_en_queue


def task():
    Thread(target=en_stack).start(), Thread(target=en_queue).start()
