import os
import json

from database_connections import Postgres
from app_logging import logger


class Plans:
    """
    Contains all the operations related to plans like fetching validity,
    daily limit, etc.
    """
    def __init__(self):
        """
        Initializes connection to Postgres and also creates tables
        for plans and inserts all the plans available.
        """
        self.__conn = Postgres.instance()
        self.__cursor = self.__conn.cursor()
        self.__initialize_table()
        self.__initialize_plans()

    def __initialize_table(self):
        """
        Creates the table if not exists.
        The query to create table should be modified in accordance
        with the plans.json file.
        """
        query = "CREATE TABLE IF NOT EXISTS plans\
                (plan_code VARCHAR(15) PRIMARY KEY,\
                 plan_name VARCHAR(15),\
                 validity VARCHAR(15),\
                 daily_limit integer,\
                 price VARCHAR(10),\
                 description VARCHAR(100))"
        try:
            self.__cursor.execute(query)
            self.__conn.commit()
        except Exception as e:
            print(e)

    def __initialize_plans(self):
        """
        Inserts the values into the plans table.
        If a plan already exits then it will be skipped.
        """
        data = self.__get_plans_data()
        plans = dict(data)
        for _, plan in plans.items():
            query = "INSERT INTO plans(plan_code, plan_name, validity, daily_limit, price, description)\
                    VALUES(%s, %s, %s, %s, %s, %s) ON CONFLICT (plan_code) DO NOTHING;"

            try:
                self.__cursor.execute(query, (plan['plan_code'], plan['plan_name'],
                                              plan['validity'], plan['daily_limit'],
                                              plan['price'], plan['description']))
                self.__conn.commit()
            except Exception as e:
                print(e)

    def __get_plan_filename(self):
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

    def __get_plans_data(self):
        """
        Reads the plans file which is in json format and return the data.

        Returns
        -------
        data: json
            Contains all the information about plans.
        """
        data = None
        with open(self.__get_plan_filename()) as f:
            data = json.load(f)
        return data

    def __validate_data(self):
        """
        Validation to check if the data satisfies certain criteria
        like valid name, etc.

        It is better to do these type of validations in the frontend.
        """
        pass

    def get_plans(self):
        """
        Fetches the plans from the plans table.

        Returns
        -------
        plans: list
            list containing tuple
        """
        logger.info("trying to fetch plans")
        query = "select * from plans"
        try:
            self.__cursor.execute(query)
            plans = self.__cursor.fetchall()
            logger.info(str(plans))
            return plans
        except Exception as e:
            logger.error("Error while fetching plans "+str(e))

    def get_plan_validity(self, plan_code):
        """
        Fetches the validity of the plan from plans table.

        Returns
        -------
        validity: list
            list containing tuple
        """
        query = "select validity from plans where plan_code=%s"
        try:
            self.__cursor.execute(query, (plan_code,))
            validity = self.__cursor.fetchall()
            return validity
        except Exception as e:
            logger.error("Error while fetching validity "+str(e))

    def get_daily_limit(self, plan_code):
        """
        Fetches the daily limit of the plan from plans table.

        Returns
        -------
        daily_limit: list
            list containing tuple
        """
        query = "select daily_limit from plans where plan_code=%s"
        try:
            self.__cursor.execute(query, (plan_code,))
            daily_limit = self.__cursor.fetchall()
            return daily_limit
        except Exception as e:
            logger.error("Error while fetching daily limit "+str(e))
