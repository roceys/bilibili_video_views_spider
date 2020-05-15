import re
import time
from threading import RLock
import fake_useragent
import requests
from requests.exceptions import ProxyError

from memory.redis_memory import RedisExpSet
from spider.proxy_model import ProxyStack
from utils.logger import log


class XiciQueue:
    url = 'https://www.xicidaili.com/nn/{}.html'
    re_str = r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>'
    url_page_count = 0
    key = 'xici:xici_proxy_queue'
    poll_heart_beat = 4
    queue_exp = 10 * 60
    queue_size = 100
    mem_set = RedisExpSet(key)
    lock = RLock()

    def __init__(self):
        self.proxies = None

    def _get_1page_html(self, page):
        url = self.url.format(page)
        headers = {'User-Agent': fake_useragent.UserAgent().random}
        try:
            log.info(('start get 1 page', url))
            res = requests.get(url,
                               headers=headers,
                               timeout=5,
                               proxies=self.proxies
                               )
            if not res.status_code == 200:
                self._new_proxy()
            res.encoding = 'utf-8'
            html = res.text
            return self._parse_html(html)
        except ProxyError as e:
            log.error(('proxy err', e))
            self._new_proxy()
            return []
        except Exception as e:
            log.error(e)
            return []

    def _new_proxy(self):
        ip = ProxyStack().get_random()
        self.proxies = {
            'http': 'http://' + ip,
            'https': 'https://' + ip,
        }
        log.warning(('set new proxy', ip))

    @staticmethod
    def _parse_html(html):
        pattern = re.compile(XiciQueue.re_str, re.S)
        result = pattern.findall(html)
        return [tup[0] + ':' + tup[1] for tup in result]

    def loop_en_queue(self):
        X = XiciQueue
        while True:
            X.url_page_count += 1
            res = self._get_1page_html(X.url_page_count)
            for item in res:
                size = len(X.mem_set.get_all())
                while size >= X.queue_size:
                    X.mem_set.flush(X.queue_exp)
                    size = len(X.mem_set.get_all())
                    log.debug(
                        'queue_size over {},sleeping for poll_time {}'.format(X.queue_size,
                                                                              X.poll_heart_beat))
                    time.sleep(X.poll_heart_beat)
                X.mem_set.set(item)

    @staticmethod
    def de_queue():
        XiciQueue.lock.acquire()
        try:
            res = XiciQueue.mem_set.get_oldest()
            XiciQueue.mem_set.delete(res)
        finally:
            XiciQueue.lock.release()
        return res


if __name__ == "__main__":
    x1 = XiciQueue()
    x1.loop_en_queue()
