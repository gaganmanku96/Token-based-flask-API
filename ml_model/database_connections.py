import os

import redis


class Redis:
    def __init__(self):
        pass

    def _get_redis_host(self):
        try:
            return os.environ['REDIS_HOST']
        except Exception:
            return "localhost"

    def _get_redis_port(self):
        try:
            return os.environ['REDIS_PORT']
        except Exception:
            return 6377

    def _get_redis_db(self):
        try:
            return os.environ['REDIS_DB']
        except Exception:
            return 0

    def connect(self):
        try:
            pool = redis.ConnectionPool(host=self._get_redis_host(),
                                        port=self._get_redis_port(),
                                        db=self._get_redis_db())
            r = redis.Redis(connection_pool=pool)
            return r
        except Exception:
            exit(0)
