import time

from flask import Flask, request, jsonify

from users_table import Users
from plans_table import Plans
from app_logging import logger

# time.sleep(5)

plan_obj = Plans()
user_obj = Users()

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
        token = user_obj.new_user(inputs)
        res['token'] = token
        return jsonify(res)
    except Exception as e:
        logger.error("Error in JSON recieved "+str(e))


@app.route('/check_phone_number/<phone_number>', methods=['GET'])
def check_phone_number(phone_number):
    res = user_obj.check_phone_number(phone_number)
    if res:
        return make_error(400, "phone number exists")
    else:
        return make_error(200,"phone number doesn't exist")


@app.route('/get_plans', methods=['GET'])
def get_plans():
    print("trying to fetch plans")
    logger.info("trying to fetch plans")
    result = plan_obj.get_plans()
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8000)
