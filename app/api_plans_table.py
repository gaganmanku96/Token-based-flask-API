from database_connections import Postgres
from app_logging import logger


class PlansAPI:
    """
    Contains all the operations related to users like creating user,
    checking phone number if already exits or not, etc.
    """
    def __init__(self):
        """
        Initializes the connection to Postgres and initializes
        the table if not exists. 
        """
        self._conn = Postgres.instance()
        self._cursor = self._conn.cursor()


    def check_phone_number(self, phone_number):
        """
        Checks if phone number already exists or not.
        In case the phone number exists it will return True else False.

        Returns
        -------
        bool
            If the query executes successfully.
        str
            If any error occurs while executing the query.
        """
        query = "select * from users where phone_number=%s"
        try:
            self._cursor.execute(query, (phone_number,))
            rows = self._cursor.rowcount
            if rows>0:
                return True
            else:
                return False
        except Exception as e:
            logger.error("Couldn't verify if phone number exists "+str(e))
            return "400-Couldn't verify phone number"

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
            self._cursor.execute(query)
            plans = self._cursor.fetchall()
            logger.info(str(plans))
            return plans
        except Exception as e:
            logger.error("Error while fetching plans "+str(e))

    def get_plan_validity(self, plan_id):
        """
        Fetches the validity of the plan from plans table.

        Parameters
        ----------
        plan_id: int

        Returns
        -------
        validity: list
            list containing tuple
        """
        query = "select validity from plans where plan_id=%s"
        try:
            self._cursor.execute(query, (plan_id,))
            validity = self._cursor.fetchall()
            return validity
        except Exception as e:
            logger.error("Error while fetching validity "+str(e))

    def get_daily_limit(self, plan_id):
        """
        Fetches the daily limit of the plan from plans table.

        Parameters
        ----------
        plan_id: int

        Returns
        -------
        daily_limit: list
            list containing tuple
        """
        query = "select daily_limit from plans where plan_id=%s"
        try:
            self._cursor.execute(query, (plan_id,))
            daily_limit = self._cursor.fetchall()
            logger.info("daily limit "+str(daily_limit))
            return daily_limit
        except Exception as e:
            logger.error("Error while fetching daily limit "+str(e))
