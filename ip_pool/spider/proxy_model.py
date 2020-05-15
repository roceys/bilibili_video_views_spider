from threading import RLock

from memory.redis_memory import RedisExpSet


class ProxyStack:
    key = 'prox:stack'
    mem_set = RedisExpSet(key)

    @staticmethod
    def en_stack(url):
        ProxyStack.mem_set.set(url)

    @staticmethod
    def de_stack():
        lock = RLock()
        lock.acquire()
        val = ProxyStack.mem_set.get_newest()[0]
        ProxyStack.mem_set.delete(val)
        lock.release()
        return val

    @staticmethod
    def get_size():
        return ProxyStack.mem_set.get_size()

    def pop(self):
        return self.de_stack()
