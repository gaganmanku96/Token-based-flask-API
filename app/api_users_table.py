from database_connections import Postgres
from app_logging import logger


class UsersAPI:
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
