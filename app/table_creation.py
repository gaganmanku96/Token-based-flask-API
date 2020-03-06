import os
import json

import psycopg2

from database_connections import Postgres
from app_logging import logger


class CreateTables:
    def __init__(self):
        self._conn = Postgres.instance()
        self._cursor = self._conn.cursor()

        self._query_plans_table = """
                CREATE TABLE IF NOT EXISTS plans\
                (plan_id SMALLINT PRIMARY KEY,\
                 plan_name VARCHAR(15),\
                 validity VARCHAR(15),\
                 daily_limit SMALLINT,\
                 price VARCHAR(10),\
                 description VARCHAR(100))
        """

        self._query_users_table = """
                CREATE TABLE IF NOT EXISTS users\
                (user_id SERIAL PRIMARY KEY,\
                 phone_number integer NOT NULL,\
                 name VARCHAR(30),\
                 registration_date timestamp,\
                 telegram_id VARCHAR(10))
        """

        self._query_tokens_table = """
                CREATE TABLE IF NOT EXISTS tokens
                (token_id SERIAL PRIMARY KEY,
                 token_key VARCHAR(30),
                 created_at timestamp)
        """

        self._query_registrations_table = """
                CREATE TABLE IF NOT EXISTS registrations
                (user_id INTEGER,
                 plan_id SMALLINT,
                 token_id INTEGER,
                 created_at timestamp,
                 status_id SMALLINT)
        """

    def _initialize_plans(self):
        """
        Inserts the values into the plans table.
        If a plan already exits then it will be skipped.
        """
        data = self._get_plans_data()
        plans = dict(data)
        for _, plan in plans.items():
            query = "INSERT INTO plans(plan_id, plan_name, validity, daily_limit, price, description)\
                    VALUES(%s, %s, %s, %s, %s, %s) ON CONFLICT (plan_id) DO NOTHING;"

            try:
                self._cursor.execute(query, (plan['plan_id'], plan['plan_name'],
                                              plan['validity'], plan['daily_limit'],
                                              plan['price'], plan['description']))
                self._conn.commit()
            except Exception as e:
                print(e)

    def _get_plan_filename(self):
        """
        If you do not pass the file_name then plans.json will be automatically
        picked.

        This is especially helpful in production and testing environments
        with different plans to maybe test the limits.

        Returns
        -------
        file_name: str
            Name of the file containing plans.
        """
        try:
            return os.environ['plans_filename']
        except Exception:
            return "plans.json"

    def _get_plans_data(self):
        """
        Reads the plans file which is in json format and return the data.

        Returns
        -------
        data: json
            Contains all the information about plans.
        """
        data = None
        with open(self._get_plan_filename()) as f:
            data = json.load(f)
        return data

    def initialize_tables(self):
        try:
            self._cursor.execute(self._query_users_table)
            self._cursor.execute(self._query_plans_table)
            self._cursor.execute(self._query_tokens_table)
            self._cursor.execute(self._query_registrations_table)

            self._initialize_plans()
            return True
        except Exception as e:
            logger.error("Couldn't Initialize tables"+str(e))
            return False
