from threading import RLock

from memory.redis_memory import RedisExpSet

lock = RLock()


class ProxyStack:
    key = 'prox:stack'
    mem_set = RedisExpSet(key)

    @staticmethod
    def en_stack(url):
        ProxyStack.mem_set.set(url)

    @staticmethod
    def de_stack():
        lock.acquire()
        try:
            val = ProxyStack.mem_set.get_newest()
            assert val, 'stack is empty'
            val = val[0]
            ProxyStack.mem_set.delete(val)
        finally:
            lock.release()
        return val

    @staticmethod
    def get_size():
        return ProxyStack.mem_set.get_size()

    def pop(self, delete=False):
        if delete is True:
            return self.de_stack()
        else:
            return self.get_random()

    @staticmethod
    def get_random():
        return ProxyStack.mem_set.get_random()
