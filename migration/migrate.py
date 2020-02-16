from datetime import datetime

import schedule 

from database_connections import Redis, Postgres
from app_logging import logger


class Migrate:
    def __init__(self):
        self.__r = Redis().connect()
        self.__conn = Postgres().connect()
        self.__cursor = self.__conn.cursor()
        self.__initialize_db()

    def __initialize_db(self):
        query = "CREATE TABLE IF NOT EXISTS user_logs(\
                 token VARCHAR(30) NOT NULL,\
                 used_requests INTEGER NOT NULL,\
                 date VARCHAR(12) NOT NULL)"
        self.__cursor.execute(query)
        self.__conn.commit()

    def __fetch_tokens_from_redis(self):
        tokens = self.__r.hgetall('token')
        return tokens

    def __fetech_remaining_limit(self, token):
        remaining_daily_limit = int(self.__r.hget('token', token))
        return remaining_daily_limit
    
    def __fetch_dailylimit_validity(self, plan_code):
        query = "select daily_limit, validity from plans where plan_code=%s"
        try:
            self.__cursor.execute(query, (plan_code,))
            result = self.__cursor.fetchall()
            daily_limit, validity = result[0][0], result[0][1]
        except Exception as e:
            logger.error("Error while fetching daily limit "+str(e))
        return daily_limit, validity
    
    def __fetch_plancode_startingdate(self, token):
        query = "select plan_code, start_date from users where token=%s"
        try:
            self.__cursor.execute(query, (token,))
            result = self.__cursor.fetchall()
            plan_code, starting_date = result[0][0], result[0][1]
        except Exception as e:
            logger.error("Error while fetching daily limit "+str(e))
        return plan_code, starting_date
    
    def __get_days(self, validity):
        if validity == '7 days':
            return 7
        elif validity == '30 days':
            return 30
        elif validity == '1 year':
            return 365
        else:
            logger.error("Validity not valid")
            raise ValueError("Validity not valid")
    
    def __is_expired(self, starting_date, validity):
        current_day = datetime.now().day
        starting_day = datetime.strptime(starting_date, "%Y-%m-%d").day
        validity = self.__get_days(validity)
        if (starting_day + current_day) > validity:
            return False
        else:
            return True
    
    def __create_token_log(self, token, used_requests):
        date = str(datetime.now().strftime("%Y-%m-%d"))
        query = "INSERT INTO user_logs(token, used_requests, date)\
                 VALUES (%s, %s, %s)"
        try:
            self.__cursor.execute(query,(token, used_requests, date))
            self.__conn.commit()
        except Exception as e:
            logger.error("Error while creating log "+str(e))
            self.__conn.rollback()

    def __renew_token(self, token, daily_limit):
        self.__r.hset('token', token, daily_limit)

    def main(self):
        tokens = self.__fetch_tokens_from_redis()
        for token in tokens:
            token = str(token, 'utf-8')
            remaining_daily_limit = self.__fetech_remaining_limit(token)
            plan_code, starting_date = self.__fetch_plancode_startingdate(token)
            daily_limit, validity = self.__fetch_dailylimit_validity(plan_code)

            if self.__is_expired(starting_date, validity):
                pass
                # maybe save
            else:
                #  create logs here
                used_requests = daily_limit - remaining_daily_limit
                self.__create_token_log(token, used_requests)
                self.__renew_token(token, daily_limit)

if __name__ == "__main__":
    migration_obj = Migrate()
    schedule.every().day.at("00:00").do(migration_obj.main) 
