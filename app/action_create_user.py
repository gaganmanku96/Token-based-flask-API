from datetime import datetime

from app_logging import logger
from database_connections import Postgres
from token_generation import TokenGeneration
from push_to_redis import push_token_to_redis


class CreateUser:
    def __init__(self):
        self._conn = Postgres.instance()
        self._cursor = self._conn.cursor()
        self._user_creation_query = """
            INSERT INTO users(name, phone_number, registration_date)
            VALUES (%s, %s, %s)
            RETURNING user_id
        """
        self._token_creation_query = """
            INSERT INTO tokens(token_key)
            VALUES (%s)
            RETURNING token_id
        """
        self._registration_query = """
            INSERT INTO registrations(user_id, plan_id, token_id, created_at, status_id)
            VALUES(%s, %s, %s, %s, %s)
        """

    def create(self, inputs):
        phone_number = inputs.get('phone_number')
        logger.info("Phone number"+str(phone_number))
        name = inputs.get('name')
        plan_id = int(inputs.get('plan_id'))
        created_at = str(datetime.utcnow())
        token = TokenGeneration().get_token()
        try:
            self._cursor.execute(self._user_creation_query, (name, phone_number, created_at))
            user_id = self._cursor.fetchone()[0]

            self._cursor.execute(self._token_creation_query, (token,))
            token_id = self._cursor.fetchone()[0]

            self._cursor.execute(self._registration_query, (user_id, plan_id, token_id, created_at, 1))

            push_token_to_redis(token, plan_id)

            self._conn.commit()
            return token
        except Exception as e:
            logger.error("Cannot create user "+str(e))
            self._conn.rollback()
            return
