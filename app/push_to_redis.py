import redis

from app_logging import logger
from database_connections import Redis
from plans_table import Plans
from app_logging import logger

r = Redis.instance()


def push_token_to_redis(token, plan_code):
    try:
        daily_limit = Plans().get_daily_limit(plan_code=plan_code)
        r.hset("token", token, str(daily_limit[0][0]).split()[0])
        logger.info("Pushed token to redis")
    except Exception as e:
        logger.error("Cannot push to redis "+str(e))
