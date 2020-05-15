from threading import Thread

from spider.ip_verify import ThreadSpider
from spider.proxy_model import ProxyStack
from spider.xici_ip_model import XiciQueue

t1 = ThreadSpider(XiciQueue, ProxyStack).main_loop
t2 = XiciQueue().loop_en_queue

Thread(target=t1).start()
Thread(target=t2).start()
