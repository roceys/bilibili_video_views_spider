import random
import time
import redis
from memory.conf import *
from utils.logger import log


class RedisMem:
    db = DB
    password = PASSWORD
    host = HOST
    port = PORT
    pool = redis.ConnectionPool(host=host, port=port, decode_responses=True, password=password, db=db)
    r = redis.Redis(connection_pool=pool)

    def __init__(self, floor=''):
        self.floor = floor

    def set(self, key, val, ex=None, remove_exist=False):
        """
        remove  False旧的不会被删除
        ex      过期时间(秒)
        """
        key = self.floor + key
        if remove_exist:
            self.r.delete(key)

        if type(val) == list:
            self.r.lpush(key, *val)  # [...,3,2,1]
        elif type(val) == dict:
            self.r.hmset(key, val)
        elif type(val) == set:
            self.r.sadd(key, *val)
        else:
            self.r.set(key, val)

        if ex:
            self.r.expire(key, ex)
        log.info(('set', key, val, ex))

    def get(self, key):
        key = self.floor + key
        return self.r.get(key)

    def delete(self, key):
        self.r.delete(key)


class RedisExpSet(RedisMem):
    def __init__(self, set_name: str, level=''):
        """
        :param set_name: set_name 
        """
        super(RedisExpSet, self).__init__(floor=level)
        self.key = self.floor + set_name
        self.exp = None

    def set_items(self, elems: set):
        for item in elems:
            self.r.zadd(self.key, {item: time.time()})
        log.info(('set items', self.key, elems))

    def set(self, elem, **kwargs):
        self.r.zadd(self.key, {elem: time.time()})
        log.info(('set row', elem))

    def flush(self, exp):
        res = self.r.zremrangebyscore(self.key, 0, time.time() - exp)
        log.info(('flush', self.key, 'exp', exp, 'remove count', res))
        return res

    def get_all(self):
        return self.r.zrevrange(self.key, 0, -1)

    def get_oldest(self):
        return self.r.zrevrange(self.key, -1, -1)[0]

    def get_newest(self):
        return self.r.zrevrange(self.key, 0, 0)

    def delete(self, values):
        self.r.zrem(self.key, values)

    def get_size(self):
        return self.r.zcard(self.key)

    def get_random(self, raise_err=False):
        res = self.r.zscan(self.key)[1]
        if res:
            return random.choice(res)[0]
        elif raise_err:
            raise ValueError('set is empty')
        else:
            return


if __name__ == '__main__':
    # r = RedisMem()
    e = RedisExpSet(set_name='xici:xici_proxy_queue')
    e.get_random()
