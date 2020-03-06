import redis

from app_logging import logger
from database_connections import Redis
from api_plans_table import PlansAPI
from app_logging import logger


r = Redis.instance()
obj_plans = PlansAPI()


def push_token_to_redis(token, plan_id):
    """
    This method push the token to redis along with its daily limit.
    Redis is used as a caching database to make sure there is no
    delay in verifying the token.

    Parameters
    ----------
    token: str
        The token to be pushed.
    plan_id: str
        The plan_code of that token to get daily limit
    """
    try:
        daily_limit = obj_plans.get_daily_limit(plan_id=plan_id)
        r.hset("token", token, str(daily_limit[0][0]).split()[0])
        logger.info("Pushed token to redis")
    except Exception as e:
        logger.error("Cannot push to redis "+str(daily_limit))
