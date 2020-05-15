import os
import re
import time
from threading import RLock
from memory.redis_memory import RedisExpSet
from utils.logger import log


class LogQueue:
    re_path = "'set row', '(.*?)'"
    key = 'xici:xici_proxy_queue'
    poll_heart_beat = 4
    queue_exp = 10 * 60
    queue_size = 100
    mem_set = RedisExpSet(key)
    lock = RLock()

    def __init__(self, filename):
        self.filename = filename
        self.proxy = None
        self.file = open(self.filename, 'r', encoding='utf-8')

    def _get_1page_url(self):
        res_list = []
        while True:
            content = self.file.readline()
            res = re.findall(LogQueue.re_path, content)
            if res:
                res_list.append(res[0])
            if len(res_list) >= 10:
                return res_list

    def loop_en_queue(self):
        X = LogQueue
        while True:
            res = self._get_1page_url()
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
        L = LogQueue
        L.lock.acquire()
        try:
            res = L.mem_set.get_oldest()
            L.mem_set.delete(res)
        finally:
            L.lock.release()
        return res


if __name__ == '__main__':
    os.chdir('../')
    # LogQueue('log/2020-05-14.log').loop_en_queue()
    LogQueue('log/2020-05-14.log').de_queue()
