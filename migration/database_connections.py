import os

import psycopg2
import redis


from app_logging import logger
   

class Postgres:
    def __init__(self):
        pass

    def _get_username(self):
        try:
            return os.environ['POSTGRES_USERNAME']
        except:
            return "postgres"

    def _get_password(self):
        try:
            return os.environ['POSTGRES_PASSWORD']
        except:
            return "password"
    
    def _get_port(self):
        try:
            return os.environ['POSTGRES_PORT']
        except:
            return 5432
    
    # def __get_database(self):
    #     return os.environ['POSTGRES_DATABASE']
    
    def _get_host(self):
        try:
            return os.environ['POSTGRES_HOST']
        except:
            return "postgres"

    def connect(self):
        conn = psycopg2.connect(
            user=self._get_username(),
            password=self._get_password(),
            host=self._get_host(),
            port=self._get_port()
            )
        return conn


class Redis:
    def __init__(self):
        pass

    def _get_redis_host(self):
        try:
            return os.environ['REDIS_HOST']
        except Exception:
            logger.warning("Redis Host not found in env file. Using default - localhost")
            return "localhost"

    def _get_redis_port(self):
        try:
            return os.environ['REDIS_PORT']
        except Exception:
            logger.warning("Redis Port not found in env file. Using default - 6379")
            return 6377

    def _get_redis_db(self):
        try:
            return os.environ['REDIS_DB']
        except Exception:
            logger.warning("Redis DB not found in env file. Using default - 0")
            return 0

    def connect(self):
        try:
            pool = redis.ConnectionPool(host=self._get_redis_host(),
                                        port=self._get_redis_port(),
                                        db=self._get_redis_db())
            r = redis.Redis(connection_pool=pool)
            logger.info("Connected to Redis")
            return r
        except Exception as e:
            logger.error("Couldn't connect to Redis. "+str(e)+" Exiting")
            exit(0)
