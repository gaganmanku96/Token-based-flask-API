import time

from flask import Flask, request, jsonify

from action_create_user import CreateUser
from api_plans_table import PlansAPI
from api_users_table import UsersAPI
from table_creation import CreateTables
from app_logging import logger


obj_plans_api = PlansAPI()
obj_users_api = UsersAPI()
obj_user = CreateUser()
obj_initialize_tables = CreateTables()

app = Flask(__name__)


def make_error(status_code, message):
    response = jsonify({
        'message': message
    })
    response.status_code = status_code
    return response


@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        inputs = request.get_json(force=True)
        res = {}
        token = obj_user.create(inputs)
        res['token'] = token
        return jsonify(res)
    except Exception as e:
        logger.error("Error in JSON recieved "+str(e))
        return make_error(400, "Error in JSON recieved")


@app.route('/check_phone_number/<phone_number>', methods=['GET'])
def check_phone_number(phone_number):
    res = obj_users_api.check_phone_number(phone_number)
    if res:
        return make_error(400, "phone number exists")
    else:
        return make_error(200,"phone number doesn't exist")


@app.route('/get_plans', methods=['GET'])
def get_plans():
    print("trying to fetch plans")
    logger.info("trying to fetch plans")
    result = obj_plans_api.get_plans()
    return jsonify(result)


if __name__ == '__main__':
    if obj_initialize_tables.initialize_tables():
        app.run(host='0.0.0.0',
                port=8000)
    else:
        logger.error("Error creating tables")
        exit(0)