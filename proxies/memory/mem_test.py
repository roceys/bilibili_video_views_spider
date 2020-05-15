import time
from unittest import TestCase
from memory.redis_memory import RedisExpSet, RedisMem
from utils.logger import log


class MemTst(TestCase):
    def test_mock_zset(self):
        e = RedisExpSet(set_name='alice', level='fxh:')
        for i in range(1000, 0, -1):
            e.set_items({str(i)})
            log.debug('setItem' + str(i))
            time.sleep(0.5)

    def test_set_item(self):
        r = RedisMem()
        r.set('alice', {'d': 'MyHonor', 'e': 'LordAlice', 'f': 'myLord'}, ex=10)

    def test_flush(self):
        e = RedisExpSet(set_name='alice', level='fxh:')
        e.flush(20)
