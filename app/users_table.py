import psycopg2

from database_connections import Postgres
from token_generation import TokenGeneration

from app_logging import logger
from push_to_redis import push_token_to_redis


class Users:
    """
    Contains all the operations related to users like creating user,
    checking phone number if already exits or not, etc.
    """
    def __init__(self):
        """
        Initializes the connection to Postgres and initializes
        the table if not exists. 
        """
        self.__conn = Postgres.instance()
        self.__cursor = self.__conn.cursor()
        self.__initialize_table()
    
    def __initialize_table(self):
        """
        Creates the table if not exists.
        """
        query = "CREATE TABLE IF NOT EXISTS users\
                (phone_number integer PRIMARY KEY,\
                 name VARCHAR(30),\
                 plan_code VARCHAR(30),\
                 start_date VARCHAR(30),\
                 token VARCHAR(40))"
        try:
            self.__cursor.execute(query)
            self.__conn.commit()
        except Exception as e:
            print(e)

    def __validate_data(self):
        """
        Validation to check if data satisfies certain criteria
        or not.

        It is better to do these type of validations in the frontend app.
        """
        pass

    def __save_to_db(self, phone_number, name, plan_code, start_date, token):
        """
        Inserts user data into database.

        Parameters
        ----------
        phone_number: int
            phone_number is the primary key of the users table.
        name: str
            name of the person
        plan_code: str
            code of the plan that user selected.
        start_date: str
            date when the user registered
        token: str
            token that is generated for the user.

        Returns
        -------
        bool
            If data is successfully inserted than true is returned
            else false is returned
        """
        query = "INSERT INTO users(phone_number, name, plan_code, start_date, token)\
                 VALUES(%s, %s, %s, %s, %s)"
        try:
            self.__cursor.execute(query, (phone_number, name, plan_code, start_date, token))
            self.__conn.commit()
            logger.info("Inserted")
            return True
        except psycopg2.IntegrityError:
            self.__conn.rollback()
            return False
        except Exception as e:
            logger.error("Error while creating new user "+str(e))
            return False

    def new_user(self, inputs):
        """
        Registers new user
        First it is saved in the db. If it is successfully saved then
        it is pushed to Redis.

        Parameters
        ----------
        inputs: dict
            **kwgrs containing information about the user
        
        Returns
        -------
        str:
            If everything goes successfully then token is returned
            else error is returned
        """
        phone_number = inputs.get('phone_number')
        name = inputs.get('name')
        plan_code = inputs.get('plan_code')
        start_date = inputs.get('start_date')
        token = TokenGeneration().get_token()
        result = self.__save_to_db(phone_number, name, plan_code, start_date, token)
        if result:
            push_token_to_redis(token, plan_code)
            return token
        else:
            return "400-Couldn't generate token"
    
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
            self.__cursor.execute(query, (phone_number,))
            rows = self.__cursor.rowcount
            if rows>0:
                return True
            else:
                return False
        except Exception as e:
            logger.error("Couldn't verify if phone number exists "+str(e))
            return "400-Couldn't verify phone number"