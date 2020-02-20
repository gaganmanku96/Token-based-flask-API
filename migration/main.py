from datetime import datetime

import schedule 

from database_connections import Redis, Postgres
from app_logging import logger




class Migrate:
    def __init__(self):
        self._r = Redis().connect()
        self._conn = Postgres().connect()
        self._cursor = self._conn.cursor()
        self._initialize_db()

    def _initialize_db(self):
        query = "CREATE TABLE IF NOT EXISTS user_logs(\
                 token VARCHAR(30) NOT NULL,\
                 used_requests INTEGER NOT NULL,\
                 date VARCHAR(12) NOT NULL)"
        self._cursor.execute(query)
        self._conn.commit()

    def _fetch_tokens_from_redis(self):
        tokens = self._r.hgetall('token')
        return tokens

    def _fetech_remaining_limit(self, token):
        remaining_daily_limit = int(self._r.hget('token', token))
        return remaining_daily_limit
    
    def _fetch_dailylimit_validity(self, plan_code):
        query = "select daily_limit, validity from plans where plan_code=%s"
        try:
            self._cursor.execute(query, (plan_code,))
            result = self._cursor.fetchall()
            daily_limit, validity = result[0][0], result[0][1]
        except Exception as e:
            logger.error("Error while fetching daily limit "+str(e))
        return daily_limit, validity
    
    def _fetch_plancode_startingdate(self, token):
        query = "select plan_code, start_date from users where token=%s"
        try:
            self._cursor.execute(query, (token,))
            result = self._cursor.fetchall()
            plan_code, starting_date = result[0][0], result[0][1]
        except Exception as e:
            logger.error("Error while fetching daily limit "+str(e))
        return plan_code, starting_date
    
    def _get_days(self, validity):
        if validity == '7 days':
            return 7
        elif validity == '30 days':
            return 30
        elif validity == '1 year':
            return 365
        else:
            logger.error("Validity not valid")
            raise ValueError("Validity not valid")
    
    def _is_expired(self, starting_date, validity):
        current_day = datetime.now().day
        starting_day = datetime.strptime(starting_date, "%Y-%m-%d").day
        validity = self._get_days(validity)
        if (starting_day + current_day) > validity:
            return False
        else:
            return True
    
    def _create_token_log(self, token, used_requests):
        date = str(datetime.now().strftime("%Y-%m-%d"))
        query = "INSERT INTO user_logs(token, used_requests, date)\
                 VALUES (%s, %s, %s)"
        try:
            self._cursor.execute(query,(token, used_requests, date))
            self._conn.commit()
        except Exception as e:
            logger.error("Error while creating log "+str(e))
            self._conn.rollback()

    def _renew_token(self, token, daily_limit):
        self._r.hset('token', token, daily_limit)

    def main(self):
        logger.info("Running Migration")

        tokens = self._fetch_tokens_from_redis()
        for token in tokens:
            token = str(token, 'utf-8')
            remaining_daily_limit = self._fetech_remaining_limit(token)
            plan_code, starting_date = self._fetch_plancode_startingdate(token)
            daily_limit, validity = self._fetch_dailylimit_validity(plan_code)

            if self._is_expired(starting_date, validity):
                pass
                # maybe save
            else:
                #  create logs here
                used_requests = daily_limit - remaining_daily_limit
                self._create_token_log(token, used_requests)
                self._renew_token(token, daily_limit)
        logger.info("Migration Completed")

if __name__ == "__main__":
    migration_obj = Migrate()
    schedule.every().day.at("00:00").do(migration_obj.main)

    while True:
        schedule.run_pending()
