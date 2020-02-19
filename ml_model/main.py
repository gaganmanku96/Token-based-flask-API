from flask import Flask, request, jsonify, g
from flask_httpauth import HTTPTokenAuth

from database_connections import Redis
from model import Model
from app_logging import logger

obj_model = Model()
r = Redis().connect()


app = Flask(__name__)
auth = HTTPTokenAuth()


def make_error(status_code, message):
    response = jsonify({
        'message': message
    })
    response.status_code = status_code
    return response


def validate_token(token):
    output = r.hget('token', token)
    if output == None:
        g.message = "Invalid Token"
        return False
    elif int(output) <= 0:
        g.message = "Daily limit exceeded"
        return False
    else:
        current_value = int(output)
        current_value -= 1
        r.hset("token", token, current_value)
        g.message = "Token is valid"
        return True


@app.route('/get_sentiment', methods=['POST'])
def predict_sentiment():
    sentence = request.get_json(force=True)
    sentence = sentence['text']
    if len(sentence) < 5:
        return make_error(400, "To short sentence for predicting something worth")
    token = request.headers.get('Authorization').split()[-1]
    if validate_token(token):
        output = obj_model.predict(sentence)
        return jsonify(output)
    else:
        return make_error(403, g.message)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5001)