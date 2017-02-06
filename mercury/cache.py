import redis
import json
from .settings import *
import threading

class Redis:
    class __Redis:
        def __init__(self):
            pass

        def __str__(self):
            return repr(self)

    instance = None
    pool = None

    def __init__(self):
        if not Redis.instance:
            Redis.instance = Redis.__Redis()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_redis(self):
        if Redis.pool is None:
            Redis.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        return redis.StrictRedis(connection_pool=Redis.pool, decode_responses=True, charset='utf8')

lock = threading.Lock()

def cache(*argument):
    def decorate(func):
        redis = Redis()
        r = redis.get_redis()
        def wrapper(*args):
            key = ':'.join(str(x) for x in (argument + args))
            with lock:
                value = r.get(key)
                if value:
                    return json.loads(value)
                else:
                    obj = func(*args)
                    if obj:
                        value = json.dumps(obj)
                        r.set(key, value)
                    return obj
        return wrapper
    return decorate
