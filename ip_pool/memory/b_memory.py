from memory.redis_memory import RedisExpSet


class BMemSet(RedisExpSet):
    def pop(self, delete: bool = True):
        """一个栈模型，弹出后删除，或放栈底"""
        res = self.r.zrange(self.key, 0, 0)[0]
        if not delete:
            last_score = self.r.zrange(self.key, -1, -1, withscores=True)[1]
            self.r.zadd(self.key, {res: last_score + 1})
        return res


if __name__ == '__main__':
    b = BMemSet(set_name='xici:xici_proxy_set')
    aa = b.pop()
    bb = 1
